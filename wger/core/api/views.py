"""Views for core apps."""

# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import viewsets, generics, response, status
from rest_framework.decorators import detail_route
from rest_framework import viewsets
from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit)
from wger.core.api.serializers import (
    UsernameSerializer,
    LanguageSerializer,
    DaysOfWeekSerializer,
    LicenseSerializer,
    RepetitionUnitSerializer,
    WeightUnitSerializer,
    UserCreationSerializer,
    SocialAuthSerializer,
    UserSerializer,
    LoginSerializer,
    UserprofileSerializer
)
from wger.utils.permissions import (UpdateOnlyPermission,
                                    WgerPermission,
                                    CreateUserApiPermission
                                    )
from social_django.utils import load_backend, load_strategy
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
# from rest_framework.permissions import AllowAny
from .utils import gen_token


class SocialAuthView(generics.ListCreateAPIView):
    """View to enable social login and signup."""

    queryset = User.objects.all()
    serializer_class = SocialAuthSerializer

    def create(self, request, *args, **kwargs):
        """Post action for either login or signup."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        authenticated_user = request.user if not request.user.is_anonymous \
            else None
        provider = serializer.data.get('provider')
        strategy = load_strategy(request)
        try:
            backend = load_backend(
                strategy=strategy, name=provider, redirect_uri=None)
        except MissingBackend:
            return Response({"error": "Provider invalid or not supported"},
                            status=status.HTTP_400_BAD_REQUEST)
        if isinstance(backend, BaseOAuth1):
            token = {
                'oauth_token': serializer.data.get('access_token'),
                'oauth_token_secret': serializer.data.get(
                    'access_token_secret')
            }
        elif isinstance(backend, BaseOAuth2):
            token = serializer.data.get('access_token')
        try:
            user = backend.do_auth(token, user=authenticated_user)
        except BaseException as e:
            return Response(
                {
                    "error": "Invalid credentials",
                    "details": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_active:
            user.is_verified = True
            user.save()
            serializer = UserSerializer(user)
            serializer.instance = user

            if serializer.data['username']:
                user_logingin = User.objects.get(
                    username=serializer.data['username'])

            elif serializer.data['email']:
                user_logingin = User.objects.get(
                    email=serializer.data['email'])

            auth_token = gen_token(user_logingin)['token']

            return Response({
                'email': serializer.data['email'],
                'username': serializer.data['username'],
                "status": 200,
                'token': auth_token,
            }, status=status.HTTP_200_OK)


class LoginView(generics.CreateAPIView):
    """User login view."""

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request):
        """Login action."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'username' in request.data \
                and request.data['username'].strip() != "":
            user = User.objects.get(username=serializer.data['username'])

        if 'email' in request.data and request.data['email'].strip() != "":
            user = User.objects.get(email=serializer.data['email'])

        token = gen_token(user)['token']

        response_data = {
            'email': user.email,
            'username': user.username,
            'status': 200,
            'token': token,
        }

        return response.Response(response_data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """API endpoint for workout objects."""

    is_private = True
    serializer_class = UserprofileSerializer
    permission_classes = (WgerPermission, UpdateOnlyPermission)
    ordering_fields = '__all__'

    def get_queryset(self):
        """Only allow access to appropriate objects."""
        return UserProfile.objects.filter(user=self.request.user)

    def get_owner_objects(self):
        """Return objects to check for ownership permission."""
        return [(User, 'user')]

    @detail_route()
    def username(self, request, pk):
        """Return the username."""
        user = self.get_object().user
        return Response(UsernameSerializer(user).data)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for workout objects."""

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name')


class DaysOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for workout objects."""

    queryset = DaysOfWeek.objects.all()
    serializer_class = DaysOfWeekSerializer
    ordering_fields = '__all__'
    filter_fields = ('day_of_week', )


class LicenseViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for workout objects."""

    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    ordering_fields = '__all__'
    filter_fields = ('full_name',
                     'short_name',
                     'url')


class RepetitionUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for repetition units objects."""

    queryset = RepetitionUnit.objects.all()
    serializer_class = RepetitionUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class WeightUnitViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for weight units objects."""

    queryset = WeightUnit.objects.all()
    serializer_class = WeightUnitSerializer
    ordering_fields = '__all__'
    filter_fields = ('name', )


class UserCreationViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for creation of new users
    '''
    is_private = True
    serializer_class = UserCreationSerializer
    permission_classes = (CreateUserApiPermission,)
    queryset = User.objects.all()

    def username_present(self, username):
        if User.objects.filter(username=username).exists():
            return True

        return False

    def create(self, request):
        """Create User via api."""

        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        if self.username_present(serializer.data['username']):
            return Response({
                "message": "A user with the provided credentials exists"
            }, 409)

        user = User()
        user.username = serializer.data['username']
        user.email = serializer.data['email']
        user.set_password(data['password'])
        user.save()

        user_profile = UserProfile.objects.get(user=user)
        user_profile.created_by = request.user.username
        user_profile.save()

        return Response({
            "username": user.username,
            "email": user.email,
            "message": "User was successfully created"
        }, 201)
