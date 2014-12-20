__author__ = 'suhas'
import twitter


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

def authenticate_twitter():
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth=auth)
    print twitter_api


def main():
    print "Authenticating with Twitter"
    authenticate_twitter()

if __name__ == '__main__':
    main()
