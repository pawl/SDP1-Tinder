from django.conf.urls import patterns, url
from app.api import handlers

urlpatterns = patterns(
    '',
    url(r'^users/$', handlers.UserProfileList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>\d+)/$', handlers.UserProfileDetail.as_view(), name='user-detail'),
    url(r'^swipes/$', handlers.SwipeActionDetail.as_view(), name='swipe-action-list'),
    url(r'^swipes/(?P<pk>\d+)/$', handlers.SwipeActionDetail.as_view(), name='swipe-action-detail'),
    url(r'^swipe/user/(?P<uid>\d+)/right/$', handlers.SwipeActionOnUser.as_view(), {'is_right': True, 'is_vote': False}, name='swipe-right'),
    url(r'^swipe/user/(?P<uid>\d+)/left/$', handlers.SwipeActionOnUser.as_view(), {'is_right': False, 'is_vote': False}, name='swipe-left'),
    url(r'^vote/user/(?P<uid>\d+)/$', handlers.SwipeActionOnUser.as_view(), {'is_right': False, 'is_vote': True}, name='vote'),
    url(r'^stats/swipes/percentage/$', handlers.UserSwipeStats.as_view(), {'is_percentage': True}, name='swipe-stats'),
    url(r'^stats/swipes/$', handlers.UserSwipeStats.as_view(), name='swipe-stats'),
    url(r'^stats/votes/$', handlers.UserVoteStats.as_view(), name='vote-stats'),
)
