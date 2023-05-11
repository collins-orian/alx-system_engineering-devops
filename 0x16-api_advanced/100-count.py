#!/usr/bin/python3
'''A module containing functions for working with the Reddit API.
'''

import requests


def count_words(subreddit, word_list, after=None, counts={}):
    """
    Recursively queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given keywords.

    Parameters:
    subreddit (str): The name of the subreddit to search.
    word_list (list): A list of strings representing the keywords to search for.
    after (str): A token representing the last post seen in a previous request. Used for pagination.
    counts (dict): A dictionary containing the counts of each keyword found so far. Used for aggregation across multiple requests.

    Returns:
    None
    """

    # Base case: invalid subreddit or no more posts to fetch
    if not subreddit:
        return

    # Construct the URL for the API request, including pagination if applicable
    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100&after={after}"

    # Set a user-agent header to avoid being blocked by Reddit's anti-bot measures
    headers = {
        'Accept': 'application/json',
        'User-Agent': ' '.join([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/97.0.4692.71',
            'Safari/537.36',
            'Edg/97.0.1072.62'
        ])
    }

    # Send the API request and check for errors
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error: Invalid subreddit or API request failed")
        return

    # Extract the post data from the API response
    data = response.json()["data"]
    posts = data["children"]

    # Parse the titles of each post and count the occurrences of each keyword
    for post in posts:
        title = post["data"]["title"].lower()
        words = title.split()
        for word in words:
            # Normalize the word by removing punctuation and converting to lowercase
            word = word.strip("!.?,;:\"'`_")
            word = word.lower()
            # Check if the word is a valid keyword
            if word in word_list:
                # Increment the count of this keyword in the dictionary
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1

    # Recursively call the function with pagination if more posts are available
    if data["after"]:
        count_words(subreddit, word_list, after=data["after"], counts=counts)
    else:
        # Sort the counts dictionary by descending count, then ascending keyword
        sorted_counts = sorted(
            counts.items(), key=lambda x: (-x[1], x[0].lower()))
        # Print the counts in the desired format
        for word, count in sorted_counts:
            print(f"{word}: {count}")
