from django.conf.urls import url

from .views import FacebookAPIView

urlpatterns = [
    url(r'^facebook/$', FacebookAPIView.as_view(), name='facebook')
]
