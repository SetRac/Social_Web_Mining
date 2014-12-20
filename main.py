__author__ = 'suhas'
import twitter
import json


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

# Authenticate into twitter app

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

def get_localized_trends():
    WORLD_WOE = 1
    US_WOE = 23424977

    world_trends = twitter_api.trends.place(_id=WORLD_WOE)
    #print "world trends are"
    #print json.dumps(world_trends, indent=1)

    us_trends = twitter_api.trends.place(_id=US_WOE)
    #print "US trends are"
    #print json.dumps(us_trends, indent=1)

    world_trends_set = set([trend['name'] for trend in world_trends[0]['trends']])
    us_trends_set = set([trend['name'] for trend in us_trends[0]['trends']])

    common_trends_set = world_trends_set.intersection(us_trends_set)
    print "common trends are"
    print common_trends_set

def main():
    print "Authenticating with Twitter"

    print
    # get trends based on yahoo where on earth ID and compute common trending items
    get_localized_trends()

if __name__ == '__main__':
    main()
