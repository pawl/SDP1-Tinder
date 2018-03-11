from django.contrib import admin

from app.models.models import Image, SwipeAction


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'num_votes',
        'num_right_swipes',
        'num_left_swipes',
        'num_views',
    )


admin.site.register(Image, ImageAdmin)
admin.site.register(SwipeAction)
