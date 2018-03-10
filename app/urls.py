from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'stats/$', views.StatsView.as_view(), name='stats'),
)
