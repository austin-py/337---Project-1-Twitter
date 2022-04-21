from classes import *
import re
from txt_reader import load_tweets

def get_winner(input_tweet):
    win_forms = ['win', 'wins', 'won', 'winning']
    winner = ''
    award = ''
    words = input_tweet.split()
    for i in range(len(words)):
        curr_word = words[i]
        for form in win_forms:
            if curr_word.lower() == form.lower():
                if i < len(words) - 3:
                    award = words[i+1] + ' ' + words[i+2]
                else:
                    award = ''

                if i > 0:
                    winner = words[i-1]
                else:
                    winner = ''
                return winner, award

def main():
    tweets = load_tweets()
    for t in tweets:
        winner, award = get_winner(t)
        print('winner for {} is {}'.format(award, winner))

if __name__ == '__main__':
    main()



