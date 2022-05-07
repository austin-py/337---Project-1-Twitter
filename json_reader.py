import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

def clean_and_save(input_file, output_file):
    new_tweets = load_tweets(input_file)
    print(len(new_tweets))
    temp = []
    collection = set()
    for t in new_tweets:
        content = t['text']
        if content not in collection:
            collection.add(content)
            temp.append(t)

    new_tweets = pd.DataFrame(temp)
    print(len(new_tweets))
    new_tweets.to_json('data/' + output_file, orient='records')

def main():
    pass


if __name__ == '__main__':
    clean_and_save('gg2013.json', 'gg2013_clean.json')
    clean_and_save('gg2015.json', 'gg2015_clean.json')
