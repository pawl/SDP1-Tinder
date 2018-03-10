from django.test import TestCase, Client
from app.models import UserProfile, SwipeAction, Event
from app.api.handlers import SwipeActionOnUser, UserProfileList
from app.serializers import UserProfileSerializer

from utils import create_user_profile, create_event
from rest_framework.test import APIRequestFactory


class SwipeActionTestCase(TestCase):

    def test_swipe_action_updates_user_profile(self):
        """
        UserProfile num_right_swipes and num_left_swipes are updated when swiped.
        """
        print('*' * 100)
        users = [create_user_profile() for i in range(3)]
        self.assertEqual(UserProfile.objects.count(), 3)

        events = [create_event() for i in range(3)]
        self.assertEqual(Event.objects.count(), 3)
        self.assertTrue(Event.objects.filter(is_active=True).count() > 0)

        # factory = APIRequestFactory()
        # request = factory.post('/api/swipe/user/%i/right/' % (current_user_pk))
        # view = SwipeActionOnUser.as_view()
        # response = view(request)
        c = Client()

        # make swipe POST requests
        user_pks = [user.pk for user in users]
        c.post('/api/swipe/user/%i/right/' % (user_pks[0]))
        c.post('/api/swipe/user/%i/left/' % (user_pks[1]))
        users = UserProfile.objects.all()

    for i, user in enumerate(users):
            print(i, 'USER NUMBER', user.pk)
            if user.pk == user_pks[0]:
                expected_right_swipes = 1
                expected_left_swipes = 0
            elif user.pk == user_pks[1]:
                expected_right_swipes = 0
                expected_left_swipes = 1
            else:
                expected_right_swipes = 0
                expected_left_swipes = 0
            self.assertEqual(user.num_right_swipes, expected_right_swipes)
            self.assertEqual(user.num_left_swipes, expected_left_swipes)
