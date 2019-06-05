from django.core.management.base import BaseCommand
from wger.core.models import UserProfile


class Command(BaseCommand):
    '''
    Command to list all the users created by a certain user via REST API
    '''

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)

    def handle(self, **options):
        '''
        Check whether the current the consumer can create users
        '''
        username = options.get("username", None)

        if username:
            try:
                users = UserProfile.objects.all().filter(created_by=username)
                if len(users) < 1:
                    return 'No users created by {} yet.'.format(username)

                elif len(users) > 0:
                    print('The users created by {} are: '.format(username))
                    for user in users:
                        print('\t' + user.user.username)
            except:
                print('{} is not yet a registered user.'.format(username))
        else:
            print('No username provided as an arguement.')
