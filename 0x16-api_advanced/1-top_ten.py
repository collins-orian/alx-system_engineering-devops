#!/usr/bin/python3
"""
Function that queries the Reddit API and prints
the top ten hot posts of a subreddit
"""
import requests
import sys


def top_ten(subreddit):
    """ Queries to Reddit API """
    user_agent = 'Mozilla/5.0'

    headers = {
        'User-Agent': user_agent
    }

    params = {
        'limit': 10
    }

    reddit_url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    response = requests.get(reddit_url,
                       headers=headers,
                       params=params,
                       allow_redirects=False)
    if response.status_code != 200:
        print(None)
        return
    dict = response.json()
    hot_posts = dict['data']['children']
    if len(hot_posts) is 0:
        print(None)
    else:
        for post in hot_posts:
            print(post['data']['title'])
