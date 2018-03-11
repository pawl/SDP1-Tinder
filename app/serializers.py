from rest_framework import serializers

from app.models import Image, SwipeAction


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'num_right_swipes',
            'num_left_swipes',
            'num_votes',
            'num_views',
            'file',
        )


class SwipeActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwipeAction
        fields = (
            'on_image',
            'is_right',
            'is_vote',
        )
