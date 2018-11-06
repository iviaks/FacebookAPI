import csv
import json
import re

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (FacebookLabel, FacebookPage, FacebookUser,
                     FacebookUserLabel)
from .utils import FacebookAPI


class FacebookAPIView(APIView):
    def _process_label(self, label, access_token):
        if FacebookLabel.objects.filter(title=label).exists():
            return FacebookLabel.objects.filter(title=label).first().label_id

        fb_api = FacebookAPI(access_token)

        response = fb_api.post('me/custom_labels', {'name': label})

        json_response = response.json()

        if response.status_code == 200:
            obj, _ = FacebookLabel.objects.get_or_create(
                label_id=json_response.get('id'),
                title=label
            )
            return obj
        else:
            error_title = json_response.get('error').get('error_user_title')

            if error_title == 'Custom Label Is Duplicated':
                response = fb_api.get('me/custom_labels?fields=name')

                labels = [
                    _label
                    for _label in response.json().get('data')
                    if _label.get('name') == label
                ]

                if labels:
                    obj, _ = FacebookLabel.objects.get_or_create(
                        label_id=labels[0].get('id'),
                        title=labels[0].get('name')
                    )
                    return obj

            raise TypeError(json.dumps(json_response))

    def post(self, request):
        data = request.data
        format_ = data.get('format', 'json')

        if (
            not data.get('page_id') or
            not FacebookPage.objects.filter(
                original_id=data.get('page_id')
            ).exists()
        ):
            return Response('Page does not exists', 400)

        if not data.get('label'):
            return Response('Label is undefined', 400)

        users = data.get('users', [])

        page = FacebookPage.objects.filter(
            original_id=data.get('page_id')).first()

        fb_api = FacebookAPI(page.access_token)

        json_response = fb_api.batch(
            [
                {
                    'method': 'GET',
                    'relative_url': uuid
                }
                for uuid in users
            ]
        ).json()

        available_users = []
        unavailable_users = []

        for user in json_response:
            if re.search(r'Object with ID \'(\d+)\'', user.get('body')):
                unavailable_users.append(
                    re.search(
                        r'Object with ID \'(\d+)\'',
                        user.get('body')
                    ).groups()[0]
                )
            else:
                available_users.append(json.loads(user.get('body')).get('id'))

        if available_users:
            try:
                label = self._process_label(
                    data.get('label'), page.access_token
                )
            except TypeError as error:
                return Response(json.loads(str(error)), 400)

            fb_api.batch(
                [
                    {
                        'method': 'POST',
                        'relative_url': '{}/label'.format(label.label_id),
                        'body': 'user={}'.format(uuid)
                    }
                    for uuid in available_users
                ]
            )

            for uuid in available_users:
                database_user, _ = FacebookUser.objects.get_or_create(
                    psid=uuid
                )

                FacebookUserLabel.objects.get_or_create(
                    owner=database_user,
                    page=page,
                    label=label,
                )

        if format_ == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users.csv"'

            writer = csv.writer(response)
            writer.writerow(['UserID'])

            for user in unavailable_users:
                writer.writerow([user])

            return response
        else:
            return Response({
                'users': unavailable_users
            })
