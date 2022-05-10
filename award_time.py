from json_reader import *
import re
import pandas as pd
import numpy as np

def sort_dict(dictionary):
    """
    Input:
        - Take a dictionary
    Output:
        - A sorted dictionary by value
    """
    sorted_keys = sorted(dictionary, key=dictionary.get, reverse = True)
    sorted_dict = {}
    for k in sorted_keys:
        sorted_dict[k] = dictionary[k]
    return sorted_dict

def relevant_data(tweets):
    relevant_tweets = []
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        if 'best' in t or 'award' in t:
            words = t.split()
            prefix = ''
            if len(words) < 4:
                prefix = ' '.join(words[0:4])
            if len(words) < 8:
                prefix = ' '.join(words[0:7])
            if len(words) > 12:
                prefix = ' '.join(words[0:10])
            if prefix not in tweet_set:
                relevant_tweets.append(tweet)
                tweet_set.add(prefix)

    return relevant_tweets

def clean_award_name(name):
    # clean award name into tokens of important words
    name = name.lower()
    stop_words = ['a', 'an', 'the', 'and', 'of', 'as', 'to', 'at', 'in', 'on', 'is', 'are', 'was', 'were', 'by', 'or',
                  'for',
                  'original', 'film', 'performance', 'motion', 'picture', 'award', 'role']
    name = re.sub("\.|\?|\!|\'|\"|\(|\)|\[|\]|,|-", ' ', name)
    name_words = []
    for w in name.split():
        if w not in stop_words:
            name_words.append(w)
    return name_words

def award_related(t, name_words):
    t_lower = t.lower()

    include = 0.0
    for w in name_words:
        if w in t_lower:
            include = include + 1.0
    if include/len(name_words) >= 0.8:
      return True

    return False

def find_time(d):
    keys = list(d.keys())
    l = []
    for i in range(10):
      if i >= len(keys):
        break
      curr = keys[i].timestamp()
      if i > 0:
        curr = np.mean(l)
      if abs(curr - keys[i].timestamp()) > 3000/(i+1):
        continue
      for j in range(d[keys[i]]):
        l.append(keys[i].timestamp())
    if len(l) > 0:
        return np.mean(l)
    else: return 0

def get_time(year):
    tweets = load_tweets('gg' + year + '_clean.json')
    tweets = relevant_data(tweets)
    length = len(tweets)
    skip_step = int(length/20000 + 1)
    print(skip_step)
    award_names = ['cecil b. demille award', 'best motion picture - drama',
                   'best performance by an actress in a motion picture - drama',
                   'best performance by an actor in a motion picture - drama',
                   'best motion picture - comedy or musical',
                   'best performance by an actress in a motion picture - comedy or musical',
                   'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film',
                   'best foreign language film',
                   'best performance by an actress in a supporting role in a motion picture',
                   'best performance by an actor in a supporting role in a motion picture',
                   'best director - motion picture', 'best screenplay - motion picture',
                   'best original score - motion picture', 'best original song - motion picture',
                   'best television series - drama', 'best performance by an actress in a television series - drama',
                   'best performance by an actor in a television series - drama',
                   'best television series - comedy or musical',
                   'best performance by an actress in a television series - comedy or musical',
                   'best performance by an actor in a television series - comedy or musical',
                   'best mini-series or motion picture made for television',
                   'best performance by an actress in a mini-series or motion picture made for television',
                   'best performance by an actor in a mini-series or motion picture made for television',
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    time_award = {}
    for award in award_names:
        d = {}
        name_words = clean_award_name(award)

        for i in range(0, len(tweets), skip_step):
            t = tweets[i]
            if award_related(t['text'], name_words):
                time = pd.Timestamp(int(t['timestamp_ms']), unit = 'ms')
                sec = time.second - time.second % 10
                time = time.replace(second=sec)
                if time in d:
                    d[time] = d[time] + 1
                else:
                    d[time] = 1
        d = sort_dict(d)
        time = int(find_time(d))
        time_award[award] = time



    time_award = sort_dict(time_award)
    with open("data/time_award_" + year + ".json", "w") as outfile:
        json.dump(time_award, outfile)


def main():
    get_time('2013')
    get_time('2015')


if __name__ == '__main__':
    main()