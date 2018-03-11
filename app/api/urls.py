from django.conf.urls import patterns, url
from app.api import handlers

urlpatterns = patterns(
    '',
    url(r'^images/$', handlers.ImageList.as_view(), name='image-list'),
    url(r'^images/(?P<pk>\d+)/$', handlers.ImageDetail.as_view(), name='image-detail'),
    url(r'^swipes/$', handlers.SwipeActionDetail.as_view(), name='swipe-action-list'),
    url(r'^swipes/(?P<pk>\d+)/$', handlers.SwipeActionDetail.as_view(), name='swipe-action-detail'),
    url(r'^swipe/image/(?P<uid>\d+)/right/$', handlers.SwipeActionOnImage.as_view(), {'is_right': True, 'is_vote': False}, name='swipe-right'),
    url(r'^swipe/image/(?P<uid>\d+)/left/$', handlers.SwipeActionOnImage.as_view(), {'is_right': False, 'is_vote': False}, name='swipe-left'),
    url(r'^vote/image/(?P<uid>\d+)/$', handlers.SwipeActionOnImage.as_view(), {'is_right': False, 'is_vote': True}, name='vote'),
    url(r'^stats/swipes/percentage/$', handlers.ImageSwipeStats.as_view(), {'is_percentage': True}, name='swipe-stats'),
    url(r'^stats/swipes/$', handlers.ImageSwipeStats.as_view(), name='swipe-stats'),
    url(r'^stats/votes/$', handlers.ImageVoteStats.as_view(), name='vote-stats'),
)
