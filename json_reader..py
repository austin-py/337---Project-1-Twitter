import json
import random

def load_tweets():
    with open('data/gg2013.json') as tweets_file:
        tweets = json.load(tweets_file)
    return tweets


if __name__ == '__main__':
    tweets = load_tweets()
    # demo print
    print(type(tweets))
    print('text' in tweets)
    for i in range(10):
        print(tweets[i])