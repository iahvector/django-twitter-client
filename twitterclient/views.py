from django.shortcuts import render, redirect
from django.conf import settings
from requests_oauthlib import OAuth1Session

user_time_line_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
twitter_consumer_key = settings.TWITTER_CONSUMER_KEY
twitter_secret_Key = settings.TWITTER_CONSUMER_SECRET


def index(request):
    context = {}
    if 'user_id' in request.session:
        context = {
            'user_id': request.session['user_id'],
            'user_name': request.session['user_name'],
            'screen_name': request.session['user_screen_name'],
            'image': request.session['user_profile_image_url']
        }

        oauth_token = request.session['oauth_token']
        oauth_token_secret = request.session['oauth_token_secret']

        oauth = OAuth1Session(twitter_consumer_key,
                              client_secret=twitter_secret_Key,
                              resource_owner_key=oauth_token,
                              resource_owner_secret=oauth_token_secret)

        # get count from request params
        time_line_response = oauth.get(user_time_line_url,
                                       params={'user_id': context['user_id'],
                                               'count': 5,
                                               'trim_user': True})
        time_line = time_line_response.json()
        context['time_line'] = time_line

    return render(request, 'index.html', context=context)


def sign_out(request):
    request.session.flush()
    return redirect('index')
