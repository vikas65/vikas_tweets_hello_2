from users import Users
from database import Database
from login_utilities import Utlities

email_id = input('Enter ur email id >>>')
Database.initialise(database='vikasdb', user='vikas', password='vikas123', host='localhost')
user = Users.read_from_db(email_id)

if user is None:
    request_token = Utlities.get_request_token()
    user_verifier = Utlities.get_User_Verifier(request_token)
    access_token = Utlities.get_access_token(request_token, user_verifier)
    user = Users.register_user(email_id, access_token['oauth_token'], access_token['oauth_token_secret'])

tweets = Utlities.search_tweet(user.oauth_token, user.oauth_token_secret)
l1 = tweets['statuses']
for i,l2 in enumerate(l1):
    tweet = l2['text']
    print("Tweet number >>> {} and tweet is {}".format(i, tweet))











