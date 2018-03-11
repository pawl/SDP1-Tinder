from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import SwipeAction


@receiver(post_save, sender=SwipeAction)
def update_image_num_swipes(sender, instance, created=False, **kwargs):
    swipe_instance = instance
    if created:
        if not swipe_instance.is_valid:
            if swipe_instance.is_vote:
                swipe_instance.on_image.num_right_swipes += 1
                swipe_instance.on_image.num_votes += 1
            else:
                if swipe_instance.is_right:
                    swipe_instance.on_image.num_right_swipes += 1
                else:
                    swipe_instance.on_image.num_left_swipes += 1
            swipe_instance.on_image.save()
            swipe_instance.is_valid = True
            swipe_instance.save()
