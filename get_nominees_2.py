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

def nominate_data(tweets):
    nominate_tweets = []
    nominate_related_words = ['nominat', 'nominees',  'win', 'won', 'lost', 'lose']
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        t_split = t.split()
        if any([(word in t) for word in nominate_related_words]):
            words = t.split()
            index = find_nominate(words)
            prefix = ' '.join(words[0:(index + 2)])
            if prefix not in tweet_set:
                nominate_tweets.append(tweet)
                tweet_set.add(prefix)

    return nominate_tweets

def get_l_r_time(time_award):
    left_time = (time_award - 120)*1000
    right_time = (time_award + 90)*1000
    return left_time, right_time

def nominate_related(t, time, name_words, left_time, right_time):
    '''
    Input:
        - Take a text and an award
    Output:
        - Return True if text is related to the award, False otherwise
    '''
    t_lower = t.lower()

    '''
    if 'nominate' not in t_lower:
        return False
    '''

    time = int(time)
    if time > left_time and time < right_time:
        return True

    include = 0.0
    for w in name_words:
        if w in t_lower:
            include = include + 1.0
    if include / len(name_words) >= 0.6:
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

def find_nominate(words):
    """
    Input:
        - Take a list of words
    Output:
        - return the index of first word that contains nominate, return -1 otherwise
    """
    nominate_related_words = ['nomina', 'nominees', 'win', 'won', 'lost', 'lose']

    for i in range(len(words)):
        if any([(word in words[i].lower()) for word in nominate_related_words]):
            return i

    return -1


def find_nominees(tweets, award, time_award):
    """
    Input:
        - Take a list of tweets and an award
    Output:
        - Return a sorted dictionary by value where keys are potential nominee of the award and value is the number of occurences in tweets
    """

    possible_nominees = {}
    max_back = 8
    name_words = clean_award_name(award.name)
    left_time, right_time = get_l_r_time(time_award)

    for tweet in tweets:
        text = tweet['text']
        if nominate_related(text,tweet['timestamp_ms'], name_words, left_time, right_time):
            sentences = re.split("\?|\!|;", text)
            for sentence in sentences:
                if 'nominat' in sentence.lower():
                    #print('{}: {}'.format(award.name, sentence))
                    #print('\n\n')
                    find_nominee_in_sentence(sentence, max_back, possible_nominees)

    sorted_nominees = sort_dict(possible_nominees)
    return sorted_nominees


def collect_right(words, nominate_index, max_back):
    res = []
    for i in range(max_back):
        j = nominate_index + i + 1
        curr = ''
        while j < len(words):
            if (j - nominate_index) > 9:
                break
            if j == nominate_index + i + 1:
                curr = curr + words[j]
            else:
                curr = curr + " " + words[j]
            res.append(curr)
            j = j+1
    return res

def collect_left(words, nominate_index, max_back):
    res = []
    for i in range(max_back):
        j = nominate_index - i - 1
        curr = ''
        while j >= 0:
            if (nominate_index - j) > 9:
                break
            if j == nominate_index - i - 1:
                curr = words[j] + curr
            else:
                curr = words[j] + " " + curr
            res.append(curr)
            j = j - 1
    return res

def find_nominee_in_sentence(sentence, max_back, possible_nominees):
    """
    Input:
        - Take a sentence, an amount of words to skip, and a dictionary of current possible nominees
    Output:
        - Add to the dictionary all the possible nominees found in the sentence
    """
    sentence = re.sub("\.|\?|\!|\'|\"|\(|\)|\[|\]|,|@|\*|\"", ' ', sentence)
    passive_voice_word = ['was', 'were', 'is', 'are', 'get']
    left_word = ['nominated', 'nominees']
    words = sentence.split()
    nominate_index = find_nominate(words)
    if (words[nominate_index] in left_word  and (words[nominate_index-1] in passive_voice_word or words[nominate_index-2] in passive_voice_word)):
        left_phrase = collect_left(words, nominate_index, max_back)
        for curr in left_phrase:
            if curr in possible_nominees.keys():
                possible_nominees[curr] = possible_nominees[curr] + 1
            else:
                possible_nominees[curr] = 1

    else:
        right_phrase = collect_right(words, nominate_index, max_back)
        for curr in right_phrase:
            if curr in possible_nominees.keys():
                possible_nominees[curr] = possible_nominees[curr] + 1
            else:
                possible_nominees[curr] = 1
        left_phrase = collect_left(words, nominate_index, max_back)
        for curr in left_phrase:
            if curr in possible_nominees.keys():
                possible_nominees[curr] = possible_nominees[curr] + 1
            else:
                possible_nominees[curr] = 1



def nominee_from_dict(answer, name,  max_count = 50, max_word = 15):
    """
    Input:
        - a sorted dictionary of possible nominee with occurence. max number of key to look through and max amount of match return
    Output:
        - Return the a list of best possible matches to nominee. (look for name and the return strings should not contains any stop words)
    """
    stop_words = ['it', 'she', 'he', 'they', 'this', 'that', 'you', 'I', 'we',
                  'is', 'are', 'was', 'were', 'be', 'will', 'should',
                  'his', 'her', 'them', 'us',
                  'awards', 'golden', 'globes',
                  'nominees', 'nominate', 'nominee', 'nominated', 'lose', 'lost'] + clean_award_name(name)
    res =[]
    i = 0
    j = 0
    for k in answer.keys():
        if i >= max_count and j >= 1: break
        if j >= max_word: break

        if not is_all_cap(k):
            continue

        if '#' in k:
            continue
        if any([(word.lower() in stop_words) for word in k.split()]):
            continue
        if get_caps_num(k) < 2:
            continue

        add = True
        contain_all_english_words = True
        for w in k.split():
            if len(w) < 3 or len(w) > 15:
                add = False

            if w.lower() not in english_words_lower_alpha_set:
                contain_all_english_words = False

        if len(k.split()) < 5 and add and not contain_all_english_words:
            res.append(k)
            i = i+1

    res2 = {}
    for k in res:
        res2[k] = get_caps_num(k)

    res2 = sort_dict(res2)
    nominee = []
    for s in res:
        nominee.append(s.lower())
        if len(nominee) > 6:
            break

    return nominee

def is_all_cap(t):
    t_lower = t.lower().split()
    t_norm = t.split()
    for i in range(len(t_lower)):
        if t_lower[i][0] == t_norm[i][0]:
            return False
    return True


def get_caps_num(t):
    t_lower = t.lower()
    t_lower = t_lower.split()
    t_split = t.split()
    res = 0
    for i in range(len(t_split)):
        if t_lower[i] != t_split[i]:
            res = res + 1

    return res


def get_nominee_all_awards(tweet_file_name, award_names):
    file_name_length = len(tweet_file_name)
    file_namw_wth_json = tweet_file_name[0:file_name_length - 5]
    get_time(tweet_file_name, award_names)


    time_award = load_tweets(file_namw_wth_json + "_award_time.json")

    tweets = load_tweets(tweet_file_name)

    nominate_tweets = nominate_data(tweets)

    nominees = {}
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i + 1
        time_happen = int(time_award[name])
        answer = find_nominees(nominate_tweets, award, time_happen)
        nominee = nominee_from_dict(answer, name)
        nominees[name] = nominee
        print(name + ": " + str(nominee))

    with open("data/nominees_" + file_namw_wth_json + ".json", "w") as outfile:
        json.dump(nominees, outfile)

    return nominees


def main():
    award_names = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    nominee_2013 = get_nominee_all_awards('gg2013_clean.json', award_names)
    nominee_2015 = get_nominee_all_awards('gg2015_clean.json', award_names)


if __name__ == "__main__":
    main()
