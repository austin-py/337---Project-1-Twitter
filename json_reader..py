import json
import random

def load_tweets():
    print('default reading gg2013.json')
    with open('data/gg2013.json') as tweets_file:
        tweets = json.load(tweets_file)
    return tweets

def load_tweets(filename):
    path = 'data/' + filename
    print('Reading {}'.format(filename))
    with open(path) as tweets_file:
        tweets = json.load(tweets_file)
    print('Finish reading {}'.format(filename))
    return tweets

if __name__ == '__main__':
    tweets = load_tweets('gg2015.json')
    # demo print
    print(type(tweets))
    print('text' in tweets)
    print(type(tweets[0]))
    print('text' in tweets[0])
    print(tweets[0])
    print()

    tweets = load_tweets('gg2013.json')
    # demo print
    print(tweets[0])