from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.models.helpers import AlphaRegexValidator, get_image_filename


class UserProfile(models.Model):
    CATEGORIES = (
        ('S', _('Slave')),
        ('O', _('Other')),
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default=CATEGORIES[0][0],
    )

    first_name = models.CharField(
        max_length=30,
        validators=[AlphaRegexValidator],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[AlphaRegexValidator],
        blank=True,
    )

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
        ('O', _('Other')),
        ('N', _('I prefer not to disclose')),
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[0][0]
    )

    age = models.SmallIntegerField(default=19)

    num_right_swipes = models.SmallIntegerField(default=0)
    num_left_swipes = models.SmallIntegerField(default=0)
    num_votes = models.SmallIntegerField(default=0)
    num_views = models.SmallIntegerField(default=0)

    IMAGE_FOLDER = 'profile-pictures/'
    picture = models.ImageField(
        blank=True,
        upload_to=get_image_filename,
        help_text="Picture will be recropped to match portrait (4x3) dimensions.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        full_name = u'%s %s' % (
            self.first_name.encode('utf-8'),
            self.last_name.encode('utf-8')
        )
        return full_name.strip()

    def get_num_right_swipes(self, event=None):
        if event:
            right_swipes = SwipeAction.objects.filter(
                on_user=self,
                is_right=True,
                is_vote=False,
                event=event,
            ).count()
        else:
            right_swipes = self.num_right_swipes
        return right_swipes

    def get_num_left_swipes(self, event=None):
        if event:
            left_swipes = SwipeAction.objects.filter(
                on_user=self,
                is_right=False,
                is_vote=False,
                event=event,
            ).count()
        else:
            left_swipes = self.num_left_swipes
        return left_swipes

    def get_num_total_swipes(self, event=None):
        if event:
            return SwipeAction.objects.filter(on_user=self, is_vote=False, event=event).count()
        else:
            return self.num_right_swipes + self.num_left_swipes

    def get_num_votes(self, event=None):
        if event:
            return SwipeAction.objects.filter(on_user=self, is_vote=True, event=event).count()
        else:
            return self.num_votes

    def get_pct_right_swipes(self, event=None):
        total_swipes = self.get_num_total_swipes(event=event)
        right_swipes = self.get_num_right_swipes(event=event)
        try:
            return right_swipes / float(total_swipes) * 100
        except:
            return None

    class Meta:
        app_label = 'app'
        ordering = ('category', 'last_name', 'updated_at', )

    def __unicode__(self):
        try:
            print(type(self.full_name()))
            print(self.full_name())
            self.full_name()
            # return 'yo'
            return self.full_name().decode('utf-8')
        except:
            return 'yo'
        # return self.full_name().encode('ascii', 'ignore').decode('ascii')


class SwipeAction(models.Model):
    on_user = models.ForeignKey('UserProfile')
    is_right = models.BooleanField(default=False)
    is_vote = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    event = models.ForeignKey('Event')
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


class Event(models.Model):
    participants = models.ManyToManyField(
        'UserProfile',
        blank=True,
        related_name='events',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        app_label = 'app'
        ordering = ('updated_at', )

    def get_num_participants(self):
        return self.participants.count()

    def __unicode__(self):
        return '%s (%i participants)' % (self.name, self.get_num_participants())
