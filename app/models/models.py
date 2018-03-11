from django.db import models

from app.models.helpers import AlphaRegexValidator, get_image_filename


class Image(models.Model):
    name = models.TextField()

    num_right_swipes = models.SmallIntegerField(default=0)
    num_left_swipes = models.SmallIntegerField(default=0)
    num_votes = models.SmallIntegerField(default=0)
    num_views = models.SmallIntegerField(default=0)

    IMAGE_FOLDER = 'images/'
    file = models.ImageField(
        blank=True,
        upload_to=get_image_filename,
        help_text="Picture will be recropped to match portrait (4x3) dimensions.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'app'
        ordering = ('name', 'updated_at', )

    def __unicode__(self):
        return self.name


class SwipeAction(models.Model):
    on_image = models.ForeignKey('Image')
    is_right = models.BooleanField(default=False)
    is_vote = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_valid = models.BooleanField(default=False)

    class Meta:
        app_label = 'app'
        ordering = ('updated_at', )

    def get_swipe_str(self):
        if self.is_right is None:
            swipe_str = '?'
        elif self.is_right:
            swipe_str = 'Right'
        else:
            swipe_str = 'Left'
        return swipe_str

    def __unicode__(self):
        return 'Swiped %s on %s' % (self.get_swipe_str(), self.updated_at)
