import oauth2
import constants
import urllib.parse as urlparse
from consumer import consumer
import json

class Utlities:
    @classmethod
    def get_request_token(cls):
        # create a consumer, which uses consumer_key and consumer_secret to identify twitter app uniquely
        client = oauth2.Client(consumer)  # consumer client
        # use the client to perform a request for request token
        response, content = client.request(constants.REQUEST_TOKEN_URL, method='POST')  # POST oauth/request_token
        if response.status != 200:
            print("An error occured while fetching request token !!")
        # get the request token parsing the query string returned
        return dict(urlparse.parse_qsl(content.decode('utf-8')))  # dictionary (list of tuples)

    @classmethod
    def get_User_Verifier(cls, request_token):
        # ask the twitter user to authorize twitter app and give the pin code
        print("Go to the following site in browser (as we don't have web application)")
        print(cls.returnAuthURL(request_token))
        user_verifier = input("Enter the user PIN >>>")  # 4748838
        return user_verifier


    @classmethod
    def returnAuthURL(cls, request_token):
        return "{}?oauth_token={}".format(constants.AUTHORIZATION_URL,
                                         request_token['oauth_token'])  # GET oauth/authorize

    @classmethod
    def get_access_token(cls, request_token, user_verifier):
        # creates a token object which contains the request token and verifier
        token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(user_verifier)
        client = oauth2.Client(consumer, token)
        response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
        return dict(urlparse.parse_qsl(content.decode('utf-8')))

    @classmethod
    def search_tweet(cls, oauth_token, oauth_token_secret, qs_params):
        # created an authorized access token object and use this to perform Twitter API calls on behalf of Twitter user
        authorized_token = oauth2.Token(oauth_token, oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)
        # make twitter API calls
        res_url = 'https://api.twitter.com/1.1/search/tweets.json?q={}+filter:images'.format(qs_params)
        response, content = authorized_client.request(res_url, 'GET')
        if response['status'] != '200':
            print('An error occured while searching twitter !!')
        return json.loads(content.decode('utf-8'))  # string to json (python dictionary) {'statuses':list {}}