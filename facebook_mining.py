__author__ = 'suhas'
import requests
import facebook
import json
from prettytable import PrettyTable
from collections import Counter

ACCESS_TOKEN = ''

def print_json(ob):
    print json.dumps(ob, indent=1)

def int_format(n):
    return "{:,}".format(n)

def get_likes_http():
    base_url = 'https://graph.facebook.com/me'

    # Get 10 likes for 10 friends
    fields = 'id,name,friends.limit(10).fields(likes.limit(10))'

    url = '%s?fields=%s&access_token=%s' % (base_url,fields,ACCESS_TOKEN)
    print url

    result = requests.get(url).json()
    print json.dumps(result, indent=1)

def connect_facebook_graph_api():
    return facebook.GraphAPI(ACCESS_TOKEN)

def get_my_fb_details(FB):

    # get my details
    print_json(FB.get_object('me'))

    # get my friends details
    print_json(FB.get_connections('me', 'friends'))

    # get facebook search details for Web Mining
    print_json(FB.request("search", {'q': 'Web Mining', 'type': 'page'}))

def compare_fanpage_likes(FB):

    # comparing likes between pepsi and coke fan pages
    pepsi_id = '56381779049'  # 'PepsiUS' can be used instead of numeric id
    coke_id = '40796308305'   # 'CocaCola' can be used instead of numeric id

    #print "Pepsi likes", int_format(FB.get_object(pepsi_id)['likes'])
    #print "Coke likes", int_format(FB.get_object(coke_id)['likes'])

def get_friends_likes(FB):
    friends = FB.get_connections('me', 'friends')['data']
    #print_json(friends)

    # construct a dict of friend names and corresponding likes
    likes = {friend['name']:FB.get_connections(friend['id'],"likes")['data'] for friend in friends}
    #print_json(likes)
    return likes

def get_popular_friend_likes(FB, likes):
    friends_likes = Counter([like['name']
                             for friend in likes
                             for like in likes[friend]
                             if like.get('name')])

    pt = PrettyTable(field_names=['Topic', 'Frequency'])
    pt.align['Topic'], pt.align['Frequency'] = 'l', 'r'
    [pt.add_row(like_count) for like_count in friends_likes.most_common(10)]
    print "Top 10 like topic among friends are"
    print pt

    # get top 10 category
    friends_likes_category = Counter([like['category']
                             for friend in likes
                             for like in likes[friend]
                             if like.get('name')])

    pt = PrettyTable(field_names=['Category', 'Frequency'])
    pt.align['Category'], pt.align['Frequency'] = 'l', 'r'
    [pt.add_row(like_count) for like_count in friends_likes_category.most_common(10)]
    print "Top 10 like category among friends are"
    print pt


def main():
    print "Facebook Mining"

    # do a http request for graph api
    #get_likes_http()

    # do graph api query using python facebook-sdk
    FB = connect_facebook_graph_api()

    # basic graph_api queries, get one's details
    #get_my_fb_details(FB)

    # comparing likes between fan pages
    compare_fanpage_likes(FB)

    # get all friends likes
    likes = get_friends_likes(FB)

    # calculate most popular like among friends
    get_popular_friend_likes(FB, likes)
if __name__ == '__main__':
    main()
