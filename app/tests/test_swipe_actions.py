from django.test import TestCase, Client
from app.models import Image, SwipeAction
from app.api.handlers import SwipeActionOnImage, ImageList
from app.serializers import ImageSerializer

from .utils import create_image
from rest_framework.test import APIRequestFactory


class SwipeActionTestCase(TestCase):

    def test_swipe_action_updates_image(self):
        """
        Image num_right_swipes and num_left_swipes are updated when swiped.
        """
        print(('*' * 100))
        images = [create_image() for i in range(3)]
        self.assertEqual(Image.objects.count(), 3)

        # factory = APIRequestFactory()
        # request = factory.post('/api/swipe/image/%i/right/' % (current_image_pk))
        # view = SwipeActionOnImage.as_view()
        # response = view(request)
        c = Client()

        # make swipe POST requests
        image_pks = [image.pk for image in images]
        c.post('/api/swipe/image/%i/right/' % (image_pks[0]))
        c.post('/api/swipe/image/%i/left/' % (image_pks[1]))
        images = Image.objects.all()

    for i, image in enumerate(images):
            print((i, 'IMAGE NUMBER', image.pk))
            if image.pk == image_pks[0]:
                expected_right_swipes = 1
                expected_left_swipes = 0
            elif image.pk == image_pks[1]:
                expected_right_swipes = 0
                expected_left_swipes = 1
            else:
                expected_right_swipes = 0
                expected_left_swipes = 0
            self.assertEqual(image.num_right_swipes, expected_right_swipes)
            self.assertEqual(image.num_left_swipes, expected_left_swipes)
