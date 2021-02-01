import os
import tweepy as tw

from dotenv import load_dotenv
load_dotenv()


def twitter_authentication():

  auth = tw.OAuthHandler(consumer_key = os.environ.get('TWITTER_API_CONSUMER_KEY'),
                         consumer_secret = os.environ.get('TWITTER_API_CONSUMER_SECRET'))
  
  auth.set_access_token(os.environ.get('TWITTER_API_ACCESS_TOKEN'),
                        os.environ.get('TWITTER_API_ACCESS_SECRET'))
  
  api = tw.API(auth, wait_on_rate_limit=True)
  
  return api


def validate_user(user):
  api = twitter_authentication()
  try:
    api.get_user(user)
    result = True
  except:
    result = False
    
  return result