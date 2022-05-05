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
        if (len(t['text']) > 130):
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
        # replace \n with whitespace
        replaced = t['text'].replace('\n', ' ')
        # ignore tweets more than 130 length
        if (len(replaced) > 130):
            continue
        f.write(replaced + '\n')

    f.close()


def main():
    pass


if __name__ == '__main__':
    save_host_tweets('gg2015')
