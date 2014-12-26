__author__ = 'suhas'
import requests
import json
ACCESS_TOKEN = ''

def get_likes_http():
    base_url = 'https://graph.facebook.com/me'

    # Get 10 likes for 10 friends
    fields = 'id,name,friends.limit(10).fields(likes.limit(10))'

    url = '%s?fields=%s&access_token=%s' % (base_url,fields,ACCESS_TOKEN)
    print url

    result = requests.get(url).json()
    print json.dumps(result, indent=1)


def main():
    print "Facebook Mining"
    get_likes_http()


if __name__ == '__main__':
    main()
