import hashlib
import hmac
import json
from urllib.parse import urljoin

import requests


class FacebookAPI:
    base_endpoint = 'https://graph.facebook.com'
    access_token = None

    def __init__(self, access_token):
        self.access_token = access_token

    def batch(self, data):
        return requests.post(
            self.base_endpoint,
            data={
                'access_token': self.access_token,
                'batch': json.dumps(data)
            }
        )

    def get(self, endpoint):
        return requests.get(
            urljoin(self.base_endpoint, endpoint),
            params={'access_token': self.access_token},
        )

    def post(self, endpoint, data={}):
        return requests.post(
            urljoin(self.base_endpoint, endpoint),
            params={'access_token': self.access_token},
            data=data
        )

    def get_psid(self, user_ids):
        appsecret_proof = hmac.new(
            b'623650c19c945d6ec5e84179cbff32fd',
            self.access_token.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return requests.post(
            urljoin(self.base_endpoint, '/pages_id_mapping'),
            data={
                'user_ids': ','.join(user_ids),
                'appsecret_proof': appsecret_proof,
                'access_token': self.access_token
            }
        )
