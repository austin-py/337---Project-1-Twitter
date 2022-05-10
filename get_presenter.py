from json_reader import *
from award_time import *
from classes import *
import re
import pandas as pd
import numpy as np
from nltk.metrics import edit_distance
from english_words import english_words_lower_alpha_set

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

def present_data(tweets):
    present_tweets = []
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        if 'present' in t:
            words = t.split()
            index = find_present(words)
            prefix = ' '.join(words[0:(index + 2)])
            if prefix not in tweet_set:
                present_tweets.append(tweet)
                tweet_set.add(prefix)

    return present_tweets

def get_l_r_time(time_award):
    left_time = (time_award - 150)*1000
    right_time = (time_award + 90)*1000
    return left_time, right_time

def present_related(t, time, name_words, left_time, right_time):
    '''
    Input:
        - Take a text and an award
    Output:
        - Return True if text is related to the award, False otherwise
    '''
    t_lower = t.lower()
    present_word = ['present', 'announce']

    '''
    if 'present' not in t_lower:
        return False
    '''

    time = int(time)
    if time > left_time and time < right_time:
        return True

    include = 0.0
    for w in name_words:
        if w in t_lower:
            include = include + 1.0
    if include / len(name_words) >= 0.9:
        return True

    return False

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

def find_present(words):
    """
    Input:
        - Take a list of words
    Output:
        - return the index of first word that contains present, return -1 otherwise
    """
    for i in range(len(words)):
        if 'present' in words[i] or 'Present' in words[i]:
            return i

    return -1


def find_presenter(tweets, award, time_award):
    """
    Input:
        - Take a list of tweets and an award
    Output:
        - Return a sorted dictionary by value where keys are potential presenter of the award and value is the number of occurences in tweets
    """

    possible_presenters = {}
    max_back = 6
    name_words = clean_award_name(award.name)
    left_time, right_time = get_l_r_time(time_award)

    for tweet in tweets:
        text = tweet['text']
        if present_related(text,tweet['timestamp_ms'], name_words, left_time, right_time):
            sentences = re.split("\?|\!|;", text)
            for sentence in sentences:
                if 'present' in sentence.lower():
                    find_presenter_in_sentence(sentence, max_back, possible_presenters)

    sorted_presenters = sort_dict(possible_presenters)
    return sorted_presenters


def find_presenter_in_sentence(sentence, max_back, possible_presenters):
    """
    Input:
        - Take a sentence, an amount of words to skip, and a dictionary of current possible presenters
    Output:
        - Add to the dictionary all the possible presenters found in the sentence
    """
    sentence = re.sub("\.|\?|\!|\'|\"|\(|\)|\[|\]|,|-|@|:", ' ', sentence)
    passive_voice_word = ['was', 'were', 'is', 'are']
    words = sentence.split()
    present_index = find_present(words)
    if words[present_index] == 'presented' and words[present_index-1] in passive_voice_word:
        for i in range(max_back):
            j = present_index + i + 1
            curr = ''
            while j < len(words):
                if (j - present_index) > 9:
                    break
                if j == present_index + i + 1:
                    curr = curr + words[j]
                else:
                    curr =  curr + " " + words[j]
                if curr in possible_presenters.keys():
                    possible_presenters[curr] = possible_presenters[curr] + 1
                else:
                    possible_presenters[curr] = 1
                j = j + 1
    else:
        for i in range(max_back):
            j = present_index - i - 1
            curr = ''
            while j >= 0:
                if (present_index - j) > 9:
                    break
                if j == present_index - i - 1:
                    curr = words[j] + curr
                else:
                    curr = words[j] + " " + curr
                if curr in possible_presenters.keys():
                    possible_presenters[curr] = possible_presenters[curr] + 1
                else:
                    possible_presenters[curr] = 1
                j = j-1



def presenter_from_dict(answer, max_count = 30, max_word = 3):
    """
    Input:
        - a sorted dictionary of possible presenter with occurence. max number of key to look through and max amount of match return
    Output:
        - Return the a list of best possible matches to presenter. (look for name and the return strings should not contains any stop words)
    """
    stop_words = ['a', 'the', 'and', 'of', 'as', 'to', 'at', 'in', 'on', 'is', 'are', 'was', 'were',
                  'there', 'this', 'that', 'had', 'have'
                  'awards', 'golden', 'globes']
    res =[]
    i = 0
    j = 0
    for k in answer.keys():
        if i >= max_count and j >= 1: break
        if j >= max_word: break
        if '#' in k:
            continue
        if not is_all_cap(k):
            continue
        if len(k.split()) <=3:
            if len(k.split()) == 1:
                if k.lower() not in english_words_lower_alpha_set and len(k) > 6 and k not in stop_words:
                    res.append(k)
                    j = j+1
                continue
            contain_stop_word = False
            words = k.lower().split()
            for w in stop_words:
                if w in words:
                    contain_stop_word = True
            for w in words:
                if len(w) < 3:
                    contain_stop_word = True
            if not contain_stop_word:
                j = j + 1
                res.append(k)
        i = i+1

    res2 = sorted(res, key=len, reverse = True)
    res = res2
    presenter = []
    for s in res:
        add = True
        for s2 in res:
            if s != s2 and s in s2:
                # for tomorrow: split to words, count words in english for both. if s2 has more then replace s2 with s.
                add = False
        if add:
            presenter.append(s.lower())
        if len(presenter) > 1:
            break



    return presenter

def is_all_cap(t):
    t_lower = t.lower().split()
    t_norm = t.split()
    for i in range(len(t_lower)):
        if t_lower[i][0] == t_norm[i][0]:
            return False
    return True


def main():
    award_names = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    time_award = load_tweets('time_award_2015.json')

    tweets = load_tweets('gg2015_clean.json')

    present_tweets = present_data(tweets)

    presenters = {}
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i+1
        time_happen = int(time_award[name])
        answer = find_presenter(present_tweets, award, time_happen)
        presenter = presenter_from_dict(answer)
        presenters[name] = presenter
        print(name + ": " + str(presenter))

    with open("presenters_2015.json", "w") as outfile:
        json.dump(presenters, outfile)


if __name__ == "__main__":
    main()
