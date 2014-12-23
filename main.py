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
    return common_trends_set

def get_trend_details(first_trend):
    q = first_trend
    count = 100
    search_results = twitter_api.search.tweets(q=q, count=count)
    statuses = search_results['statuses']

    for _ in range(5):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e:
            break

        # construct a dict if next_results exist, this is cursoring aka pagination for twitter streams

        twitter_dict = dict([kv.split("=") for kv in next_results[1:].split("&")])
        search_results = twitter_api.search.tweets(**twitter_dict)
        statuses += search_results['statuses']

    #print json.dumps(statuses[0], indent=1)
    return statuses

def get_tweet_contents(status_details):
    status_text = [status['text']
                   for status in status_details]

    screen_name = [user_mention['screen_name']
                   for status in status_details
                   for user_mention in status['entities']['user_mentions']]

    hashtags = [hash_text['text']
                for status in status_details
                for hash_text in status['entities']['hashtags']]

    words = [word
             for text in status_text
             for word in text.split()]

    #print json.dumps(status_text[0:5], indent=1)
    #print json.dumps(screen_name[0:5], indent=1)
    #print json.dumps(hashtags[0:5], indent=1)
    #print json.dumps(words[0:5], indent=1)

    return (status_text, screen_name, hashtags, words)

def show_top_details(words, screen_name, hashtags):
    from collections import Counter
    from prettytable import PrettyTable

    for label, data in (('Words', words),('Screen Name', screen_name), ('Hashtags', hashtags)):
        pt = PrettyTable(field_names=[label, 'Count'])
        c = Counter(data)
        [pt.add_row(kv) for kv in c.most_common()[:10]]
        pt.align['label'], pt.align['Count'] = 'l', 'r'
        print pt


def main():
    print "Authenticating with Twitter"
    print

    # get trends based on yahoo where on earth ID and compute common trending items
    common_trends_set = get_localized_trends()

    print "number of common trends are ", len(common_trends_set)
    print "common trends are"
    for trends in common_trends_set:
        print trends

    # retrieve first common trend
    for first_trend in common_trends_set:
        break
    print "first common trend is ", first_trend

    # get tweet details for first trend
    status_details = get_trend_details(first_trend)

    # extract tweet details like text, screen name and hashtags
    (status_text, screen_name, hashtags, words) = get_tweet_contents(status_details)

    # display top 10 tweet details
    show_top_details(words, screen_name, hashtags)

if __name__ == '__main__':
    main()
