from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^auth/signin$', views.signIn, name='signIn'),
    url(r'^auth/twitter_callback$', views.twitter_callback,
        name='twitter_callback'),
    url(r'^time_line$', views.user_time_line, name='user_time_line')
]
