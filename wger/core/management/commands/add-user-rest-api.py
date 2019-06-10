from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    Command for helping to create new users via REST API
    '''

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)

    def handle(self, **options):
        '''
        Checks if user is able to create other users
        '''
        username = options.get("username", None)
        if username:
            try:
                userObject = User.objects.get(username=username)
                user = UserProfile.objects.get(user=userObject)
                if user.create_user_via_api:
                    return ('{} is able to create users via API'
                            .format(userObject.username))
                elif not user.create_user_via_api:
                    user.create_user_via_api = True
                    user.save()
                    return ('{}, you are now allowed to create users via the API'
                            .format(userObject.username))
            except:
                print('{} is not yet a registered user.'.format(username))
        else:
            print('No username provided as an argument.')
