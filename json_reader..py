import json
import random

def load_tweets():
    with open('data/gg2013.json') as tweets_file:
        tweets = json.load(tweets_file)
    return tweets

def load_tweets(filename):
    path = 'data/' + filename
    with open(path) as tweets_file:
        tweets = json.load(tweets_file)
    return tweets

if __name__ == '__main__':
    print('load gg2015.json')
    tweets = load_tweets('gg2015.json')
    # demo print
    print(type(tweets))
    print('text' in tweets)
    print(type(tweets[0]))
    print('text' in tweets[0])
    print(tweets[0])

    print('load gg2013.json')
    tweets = load_tweets('gg2013.json')
    # demo print
    print(type(tweets))
    print('text' in tweets)
    print(type(tweets[0]))
    print('text' in tweets[0])
    print(tweets[0])