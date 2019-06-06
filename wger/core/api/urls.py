"""urls for core api created features."""

from rest_framework.urls import url
from django.urls import include
from rest_framework import routers

from .views import SocialAuthView, LoginView

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^auth-login/$', SocialAuthView.as_view()),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^user-login/$', LoginView.as_view()),
]
