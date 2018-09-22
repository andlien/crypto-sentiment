import pickle

import praw
import yaml
import urllib.request, json
from os import listdir
import redditCredentials

from Post import Post

'https://graphs2.coinmarketcap.com/currencies/bitcoin/'

PUSHSHIFT_URL = 'http://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=asc&sort_type=created_utc&size=1000'
PUSHSHIFT_AFTER_PARAM = '&after={}'


def pushshiftUrl(subreddit, after_id=''):
    url = PUSHSHIFT_URL.format(subreddit)
    if after_id == '':
        return url
    return url + PUSHSHIFT_AFTER_PARAM.format(after_id)


def getJson(url):
    with urllib.request.urlopen(url) as res:
        data = json.loads(res.read().decode(encoding='utf-8'))
    return data


if __name__ == '__main__':

    reddit = praw.Reddit(client_id=redditCredentials.client_id,
                         client_secret=redditCredentials.client_secret,
                         user_agent='PRAW')

    with open('crypto_subreddits.yaml', 'r', encoding='utf8') as f:
        subreddits = yaml.load(f)

    for currencySymbol in subreddits.keys():
        if '%s.pkl' % currencySymbol in listdir('text/'):
            print("Ignored", currencySymbol)
            continue
        print("Downloading {}-news from Reddit".format(subreddits[currencySymbol]["cmc_name"]))

        posts = set()
        for sr in subreddits[currencySymbol]['subreddits']:
            print("Subreddit:", sr)
            url = pushshiftUrl(sr)
            jsonResponse = getJson(url)['data']

            while len(jsonResponse) != 0:
                print("After:", jsonResponse[0]['id'])
                allIds = ['t3_' + submission['id'] for submission in jsonResponse]
                for subresult in reddit.info(allIds):
                    posts.add(Post(subresult))
                url = pushshiftUrl(sr, int(subresult.created_utc))
                jsonResponse = getJson(url)['data']
        print('Downloaded {} posts about {}'.format(len(posts), subreddits[currencySymbol]['cmc_name']))



        with open('text/%s.pkl' % currencySymbol, 'wb') as f:
            pickle.dump(posts, f)
