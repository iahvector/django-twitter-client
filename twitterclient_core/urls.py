from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signIn, name='signIn'),
    url(r'^twitter_callback$', views.twitter_callback, name='twitter_callback'),
]
