import requests
from flask import Flask, render_template, session, redirect, request, url_for, g
from login_utilities import Utlities
from users import Users
from database import Database
import json

app = Flask(__name__)
app.secret_key = '1234'
Database.initialise(database='vikasdb', user='vikas', password='vikas123', host='localhost')


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = Users.read_from_db(session['screen_name'])


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('user_profile'))
    request_token = Utlities.get_request_token()
    session['request_token'] = request_token

    return redirect(Utlities.returnAuthURL(request_token))


@app.route('/logout')
def twitter_logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def auth_twitter():
    user_verifier = request.args.get('oauth_verifier')
    access_token = Utlities.get_access_token(session['request_token'], user_verifier)
    user = Users.read_from_db(access_token['screen_name'])

    if user is None:
        user = Users(None,access_token['screen_name'], access_token['oauth_token'],access_token['oauth_token_secret'])
        user.save_to_db()

    session['screen_name'] = user.screen_name
    return redirect(url_for('user_profile'))


@app.route('/profile')
def user_profile():
    return render_template('profile.html', user=g.user)


@app.route('/search')
def user_search():
    tweets = Utlities.search_tweet(g.user.oauth_token, g.user.oauth_token_secret, request.args.get('q'))
    l1 = tweets['statuses']
    tweets_text = list()
    for i, l2 in enumerate(l1):
        tweet = {'tweet': l2['text'],'label': 'neutral'}
        tweets_text.append(tweet)

    for t1 in tweets_text:
        r = requests.post('http://text-processing.com/api/sentiment/',data={'text': t1['tweet']})
        json_response = r.json()
        label = json_response['label']
        t1['label'] = label
    print('here 1')
    return render_template('search.html', content=tweets_text)


app.run(port=4996)   #GET http://127.0.0.1:4995 HTTP/1.1         GET URI PROTOCOL