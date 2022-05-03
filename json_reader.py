import json
import numpy as np
import matplotlib.pyplot as plt

import host_parser


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
    path = 'data/' + output_name + '_text.txt'
    f = open(path, 'w')
    tweets = load_tweets(output_name + '.json')
    counter = 0
    for t in tweets:
        if(len(t['text']) > 130):
            counter = counter + 1
            continue
        replaced = t['text'].replace('\n', ' ')
        f.write('sent_' + str(counter) + ':\n')
        f.write(replaced + '\n')
        counter = counter + 1
    f.close()

def save_host_tweets(output_name):
    path = 'data/' + output_name + '_host.txt'
    f = open(path, 'w')
    tweets = load_tweets(output_name + '.json')

    host_tweets_length_list = []

    for t in tweets:
        if not host_parser.has_host(t['text']):
            continue
        #replace \n with whitespace
        replaced = t['text'].replace('\n', ' ')
        # ignore tweets more than 130 length
        if(len(replaced) > 130):
            continue
        f.write(replaced + '\n')

    f.close()


if __name__ == '__main__':
    #save_host_tweets('gg2015')
    tweets = load_tweets('gg2015.json')
    host_tweets_length_list = []
    total_length = 0
    for t in tweets:
        if not host_parser.has_host(t['text']):
            continue
        host_tweets_length_list.append(len(t['text']))

    vals, counts = np.unique(host_tweets_length_list, return_counts=True)
    maxVal = np.max(vals)
    print(maxVal)
    bin_ranges = range(0, 200, 10)
    plt.hist(host_tweets_length_list, bins=bin_ranges, edgecolor='black')
    plt.show()
    # save_tweets('gg2013')
    # tweets = load_tweets()
    # tweets_length_list = []
    # total_length = 0
    # for t in tweets:
    #     tweets_length_list.append(len(t['text']))
    #
    # vals, counts = np.unique(tweets_length_list, return_counts=True)
    # maxVal = np.max(vals)
    # print(maxVal)
    # bin_ranges = range(0, 200, 5)
    # plt.hist(tweets_length_list, bins=bin_ranges, edgecolor='black')
    # plt.show()
    #mod length:ModeResult(mode=array([125]), count=array([2323]))
    #median length: 89.0
    #averge length: 89.8
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
