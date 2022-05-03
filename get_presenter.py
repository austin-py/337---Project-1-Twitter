from json_reader import *
from classes import *
import re

def present_related(t, award):
    """
    Input:
        - Take a text and an award
    Output:
        - Return True if text is related to the award, False otherwise
    """
    name = award.name.lower()
    name_words = name.split()
    present_words = ['present']

    if name not in t.lower():
        return False

    for w in present_words:
        if w in t.lower():
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
        if 'present' in words[i]:
            return i

    return -1


def find_presenter(tweets, award):
    """
    Input:
        - Take a list of tweets and an award
    Output:
        - Return a sorted dictionary by value where keys are potential presenter of the award and value is the number of occurences in tweets
    """

    possible_presenters = {}
    max_back = 5

    for tweet in tweets:
        text = tweet['text']
        if present_related(text, award):
            sentences = re.split("\.|\?|\!", text)
            for sentence in sentences:
                sentence = sentence.lower()
                if 'present' in sentence and award.name.lower() in sentence:
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
    sentence = re.sub("\.|\?|\!|\'|\"|\(|\)|\[|\]|,", ' ', sentence)
    passive_voice_word = ['was', 'were', 'is', 'are']
    sentence = sentence.lower()
    words = sentence.split()
    present_index = find_present(words)
    if words[present_index] == 'presented' and words[present_index-1] in passive_voice_word:
        for i in range(max_back):
            j = present_index + i + 1
            curr = ''
            while j < len(words):
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
                if j == present_index - i - 1:
                    curr = words[j] + curr
                else:
                    curr = words[j] + " " + curr
                if curr in possible_presenters.keys():
                    possible_presenters[curr] = possible_presenters[curr] + 1
                else:
                    possible_presenters[curr] = 1
                j = j-1



def presenter_from_dict(answer, max_count = 15, max_word = 2):
    """
    Input:
        - a sorted dictionary of possible presenter with occurence. max number of key to look through and max amount of match return
    Output:
        - Return the a list of best possible matches to presenter. (look for name and the return strings should not contains any stop words)
    """
    stop_words = ['a', 'the', 'and', 'of', 'as', 'to', 'at', 'in', 'on', 'is', 'are', 'was', 'were']
    res =[]
    i = 0
    j = 0
    for k in answer.keys():
        if i >= max_count: break
        if j >= max_word: break
        if len(k.split()) == 2 or len(k.split()) == 3:
            contain_stop_word = False
            words = k.split()
            for w in stop_words:
                if w in words:
                    contain_stop_word = True
            if not contain_stop_word:
                j = j + 1
                res.append(k)
        i = i+1
    return res




def main():
    tweets = load_tweets('gg2013.json')
    award_names = ['best supporting actor', 'best supporting actress', 'best director', 'best motion picture',
                   'best actor', 'best actress', 'best screen play', 'best animated feature film', 'best television series']
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i+1
        answer = find_presenter(tweets, award)
        presenters = presenter_from_dict(answer)
        print(name + ": " + str(presenters))



if __name__ == "__main__":
    main()
