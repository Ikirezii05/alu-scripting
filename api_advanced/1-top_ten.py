import requests

def recurse(subreddit, hot_list=[], after=None):
    """
    Recursively queries the Reddit API and returns a list of titles of all hot articles for a given subreddit.
    
    :param subreddit: The subreddit to query.
    :param hot_list: A list to store the titles of hot articles.
    :param after: The "after" parameter for pagination.
    :return: A list of titles of hot articles or None if the subreddit is invalid.
    """
    url = f'https://www.reddit.com/r/{subreddit}/hot.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    params = {'after': after, 'limit': 100}  # Fetch up to 100 posts per request for efficiency

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get('data')
    if not data:
        return None

    children = data.get('children')
    if not children:
        return hot_list

    for child in children:
        hot_list.append(child['data']['title'])

    after = data.get('after')
    if not after:
        return hot_list

    return recurse(subreddit, hot_list, after)

# Example usage:
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        result = recurse(sys.argv[1])
        if result is not None:
            print(len(result))
        else:
            print("None")
