from classes import *
import re
from json_reader import load_tweets

# Find the following:
# Host(s) (for the entire ceremony)
# Award Names
# Presenters, mapped to awards*
# Nominees, mapped to awards*
# Winners, mapped to awards*

# Get host
def get_host(input_tweet):
    host_forms = ['host', 'hosts', 'hosting']
    words = input_tweet.split()
    for w in words:
        for h in host_forms:
            if w.lower() == h:
                print(input_tweet)

# Get award names
def get_award(input_tweet):
    award_names = list()
    words = input_tweet.split()
    for w in words:
        if w.lower() == 'best':
            print(input_tweet)

# Get presenter
def get_presenter(input_tweet):
    presenters = list()
    words = input_tweet.split()
    for w in words:
        if w.lower() == 'present':
            print(input_tweet)

# Get Nominee
def get_nominee(input_tweet):
    nominee_forms = ['nominee', 'nominated']
    nominee = list()
    words = input_tweet.split()
    for w in words:
        for n in nominee_forms:
            if w.lower() == n:
                print(input_tweet)

# Get winner
def get_winner(input_tweet):
    win_forms = ['win', 'wins', 'won', 'winning']
    winner = ''
    award = ''
    words = input_tweet.split()
    for i in range(len(words)):
        curr_word = words[i]
        for form in win_forms:
            if curr_word.lower() == form.lower():
                print(input_tweet)


def main():
    tweets = load_tweets()
    for t in tweets:
        text = t['text']
        get_host(text)



if __name__ == '__main__':
    main()



