from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from random import randint

from app.tests.utils import create_event, create_user_profile
from app.models import UserProfile, Event

from loremipsum import get_sentence, get_paragraph


class Command(BaseCommand):
    args = 'numEvents numUsers [--reset]'
    help = 'Create events and users using lorem ipsum generator'

    option_list = BaseCommand.option_list + (
        make_option(
            '--reset',
            action='store_true',
            dest='reset',
            default=False,
            help='Delete all events and users before generating new ones.',
        ),
    )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Usage: {0}'.format(self.args))

        if options['reset']:
            UserProfile.objects.all().delete()
            Event.objects.all().delete()

        try:
            numEvents = int(args[0])
            numUsers = int(args[1])
            for i in range(numEvents):
                create_event()
            for i in range(numUsers):
                create_user_profile()
        except ValueError:
            raise CommandError('Usage: you must pass a valid number.')
        except Exception, e:
            print(e)
            raise CommandError('A vague error occured while generating notes')

        self.stdout.write('Successfully generated {0} events and {1} users'.format(numUsers, numEvents))
