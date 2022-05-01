import json
import random

def load_tweets(filename=None):
    if not filename:
        filename = 'gg2013.json'
    path = 'data/' + filename
    print('Reading {}'.format(filename))
    with open(path) as tweets_file:
        tweets = json.load(tweets_file)
    print('Finish reading {}'.format(filename))
    return tweets

def save_tweets(output_name):
    path = 'data/' + output_name
    f = open(path, 'w')
    tweets = load_tweets('gg2013.json')
    for t in tweets:
        f.write(t['text'] + '\n')
    f.close()


if __name__ == '__main__':
    save_tweets('gg2013_text.txt')
    #tweets = load_tweets('gg2015.json')
    # demo print
    # print(type(tweets))
    # print('text' in tweets)
    # print(type(tweets[0]))
    # print('text' in tweets[0])
    # print(tweets[0])
    # print('Total tweets: {}'.format(len(tweets)))
    # unique_user_ids = list()
    # print(tweets[0]['user'])
    # print(tweets[0]['user']['id'])
