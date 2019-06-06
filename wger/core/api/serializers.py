"""Serializers for core apllications."""

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

from rest_framework import serializers
from django.contrib.auth.models import User
from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit,
)
from django.contrib.auth import authenticate


class UserprofileSerializer(serializers.ModelSerializer):
    """Workout session serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = UserProfile
        fields = '__all__'


class UsernameSerializer(serializers.Serializer):
    """Serializer to extract the username."""

    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    """Language serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = Language
        fields = '__all__'


class DaysOfWeekSerializer(serializers.ModelSerializer):
    """DaysOfWeek serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = DaysOfWeek
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    """License serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = License
        fields = '__all__'


class RepetitionUnitSerializer(serializers.ModelSerializer):
    """Repetition unit serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = RepetitionUnit
        fields = '__all__'


class WeightUnitSerializer(serializers.ModelSerializer):
    """Weight unit serializer."""

    class Meta:
        """meta class specify fields and model."""

        model = WeightUnit
        fields = '__all__'


class SocialAuthSerializer(serializers.ModelSerializer):
    """Serializer for social authentication."""

    provider = serializers.CharField(
        max_length=30,
        allow_blank=True
    )
    access_token = serializers.CharField(
        max_length=255,
        allow_blank=True
    )
    access_token_secret = serializers.CharField(
        max_length=255,
        allow_blank=True,
        default=""
    )

    class Meta:
        """Meta class for social auth serialize."""

        model = User
        fields = ("provider", "access_token", "access_token_secret")

    def validate(self, data):
        """Method to validate provider and access token."""
        # provider_list = ['google-oauth2', 'twitter', 'facebook']
        provider = data.get('provider', None)
        access_token = data.get('access_token', None)
        access_token_secret = data.get('access_token_secret', None)
        if not provider:
            raise serializers.ValidationError(
                'A provider is required for Social Login'
            )

        if not access_token:
            raise serializers.ValidationError(
                'An access token is required for Social Login'
            )

        if provider == 'twitter' and not access_token_secret:
            raise serializers.ValidationError(
                'An access token secret is required for Twitter Login'
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user creations."""

    class Meta:
        """Specify model and fiels."""

        model = User
        fields = ("username", "email", "password")


class LoginSerializer(serializers.Serializer):
    """Login serializer for api."""

    email = serializers.EmailField(
        max_length=255, allow_blank=True,
        required=False)
    username = serializers.CharField(
        max_length=255, allow_blank=True,
        required=False)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        """Validate user data on login."""
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if not email and not username:
            raise serializers.ValidationError(
                'either your email or username is required to log in'
            )

        if not password:
            raise serializers.ValidationError(
                'Password is required to log in.'
            )

        if email:
            email_user = User.objects.get(email=email)
            username = email_user.username

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'User with provided email/username and password was not found'
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
        }

    class Meta:
        """User model and fields."""

        model = User
        fields = ('email', 'username', 'password')


class UserCreationSerializer(serializers.ModelSerializer):
    '''
    Create User Serializer
    '''
    username = serializers.CharField(max_length=255, min_length=4)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, min_length=6,
                                     write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email:
            raise serializers.ValidationError(
                'Username and email is required.'
            )

        if not password:
            raise serializers.ValidationError(
                'Password is required.'
            )
        data = {
            'username': username,
            'email': email,
            'password': password,
        }

        return data
