import os

from django.conf import settings
from django.core.management.base import BaseCommand

from app.models import Image


class Command(BaseCommand):
    help = 'Create images based on the media directory'

    def handle(self, *args, **options):
        Image.objects.all().delete()

        num_images = 0

        # Get all files from the MEDIA_ROOT, recursively
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        if media_root is not None:
            images_root = os.path.join(media_root, 'images')
            for relative_root, dirs, files in os.walk(images_root):
                for file_ in files:
                    # Compute the relative file path to the media directory, so it can be compared to the values from the db
                    relative_file = os.path.join(os.path.relpath(relative_root, media_root), file_)
                    Image.objects.create(name=file_, file=relative_file)
                    num_images += 1

        self.stdout.write('Successfully generated {0} images'.format(num_images))
