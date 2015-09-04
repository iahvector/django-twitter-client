from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from requests_oauthlib import OAuth1Session
from django.core.urlresolvers import reverse

request_token_url = 'https://api.twitter.com/oauth/request_token'
base_authorization_url = 'https://api.twitter.com/oauth/authenticate'
access_token_url = 'https://api.twitter.com/oauth/access_token'
verify_account_url = 'https://api.twitter.com/1.1/account\
/verify_credentials.json'
user_time_line_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
twitter_consumer_key = settings.TWITTER_CONSUMER_KEY
twitter_secret_Key = settings.TWITTER_CONSUMER_SECRET


def index(request):
    return render(request, 'core/index.html')


def signIn(request):
    callback_url = request.build_absolute_uri(reverse('twitter_callback'))

    oauth = OAuth1Session(twitter_consumer_key,
                          client_secret=twitter_secret_Key,
                          callback_uri=callback_url)
    response = oauth.fetch_request_token(request_token_url)

    request.session['oauth_token'] = response.get('oauth_token')
    request.session['oauth_token_secret'] = response.get(
        'oauth_token_secret')

    authorization_url = oauth.authorization_url(base_authorization_url)

    return redirect(authorization_url)


def twitter_callback(request):
    oauth_token = request.session['oauth_token']
    oauth_token_secret = request.session['oauth_token_secret']

    # check if oauth_token & oauth_token_secret exist
    # else redirect to restart the sign in process

    oauth = OAuth1Session(twitter_consumer_key,
                          client_secret=twitter_secret_Key,
                          resource_owner_key=oauth_token,
                          resource_owner_secret=oauth_token_secret)

    redirect_response = request.build_absolute_uri(request.get_full_path())
    oauth_response = oauth.parse_authorization_response(redirect_response)
    oauth_response.get('oauth_verifier')
    oauth_tokens = oauth.fetch_access_token(access_token_url)
    request.session['oauth_token'] = oauth_tokens.get('oauth_token')
    request.session['oauth_token_secret'] = oauth_tokens.get(
        'oauth_token_secret')

    verify_account_response = oauth.get(verify_account_url)

    user = verify_account_response.json()

    request.session['user_id'] = user['id_str']
    request.session['user_name'] = user['name']
    request.session['user_screen_name'] = user['screen_name']
    request.session['user_profile_image_url'] = user['profile_image_url']

    return JsonResponse(user, safe=False)


def user_time_line(request):
    oauth_token = request.session['oauth_token']
    oauth_token_secret = request.session['oauth_token_secret']
    user_id = request = request.session['user_id']

    # Check oauth_token, oauth_token_secret & user_id

    oauth = OAuth1Session(twitter_consumer_key,
                          client_secret=twitter_secret_Key,
                          resource_owner_key=oauth_token,
                          resource_owner_secret=oauth_token_secret)

    # get count from request params
    time_line_response = oauth.get(user_time_line_url,
                                   params={'user_id': user_id,
                                           'count': 5,
                                           'trim_user': True})
    time_line = time_line_response.json()

    return JsonResponse(time_line, safe=False)
