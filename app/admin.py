from django.contrib import admin

from app.models.models import UserProfile, Event, SwipeAction


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'num_votes',
        'num_right_swipes',
        'num_left_swipes',
        'num_views',
        'age',
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_active',
        'get_num_participants',
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(SwipeAction)
