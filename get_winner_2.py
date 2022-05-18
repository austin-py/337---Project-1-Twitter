from json_reader import *
from award_time import *
from classes import *
import re
import pandas as pd
import numpy as np

def winning_datas(tweets):
    result = []
    winning_related_words = ['win', 'won', 'winning']
    for tweet in tweets:
        t = tweet['text'].lower()
        if any([(word in t) for word in winning_related_words]):
            result.append(tweet)

    return result

def sort_dict(dictionary):
    """
    Input:
        - Take a dictionary
    Output:
        - A sorted dictionary by value
    """
    sorted_keys = sorted(dictionary, key=dictionary.get, reverse=True)
    sorted_dict = {}
    for k in sorted_keys:
        sorted_dict[k] = dictionary[k]
    return sorted_dict


def find_winner(winning_tweets, nominees):
    count = {}
    for n in nominees:
        count[n] = 0
    for tweet in winning_tweets:
        t = tweet['text'].lower()
        for n in nominees:
            if n in t:
                count[n] = count[n] + 1
    sorted_count = sort_dict(count)
    return list(sorted_count.keys())[0]

def get_winner_all_awards(tweet_file_name, nominees_dict):
    file_name_length = len(tweet_file_name)
    file_name_wth_json = tweet_file_name[0:file_name_length - 5]
    
    tweets = load_tweets(tweet_file_name)

    winning_tweets = winning_datas(tweets)

    winners = {}
    i = 1
    for k in nominees_dict.keys():
        answer = find_winner(winning_tweets, nominees_dict[k])
        winners[k] = answer

    with open("data/winners_" + file_name_wth_json + ".json", "w") as outfile:
        json.dump(winners, outfile)

    return winners

def main():
    nominees_dict_2013 = {'best screenplay - motion picture': ['zero dark thirty', 'lincoln', 'silver linings playbook', 'argo', 'django unchained'], 'best director - motion picture': ['kathryn bigelow', 'ang lee', 'steven spielberg', 'quentin tarantino', 'ben affleck'], 'best performance by an actress in a television series - comedy or musical': ['zooey deschanel', 'tina fey', 'julia louis-dreyfus', 'amy poehler', 'lena dunham'], 'best foreign language film': ['the intouchables', 'kon tiki', 'a royal affair', 'rust and bone', 'amour'], 'best performance by an actor in a supporting role in a motion picture': ['alan arkin', 'leonardo dicaprio', 'philip seymour hoffman', 'tommy lee jones', 'christoph waltz'], 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ['hayden panettiere', 'archie panjabi', 'sarah paulson', 'sofia vergara', 'maggie smith'], 'best motion picture - comedy or musical': ['the best exotic marigold hotel', 'moonrise kingdom', 'salmon fishing in the yemen', 'silver linings playbook', 'les miserables'], 'best performance by an actress in a motion picture - comedy or musical': ['emily blunt', 'judi dench', 'maggie smith', 'meryl streep', 'jennifer lawrence'], 'best mini-series or motion picture made for television': ['the girl', 'hatfields & mccoys', 'the hour', 'political animals', 'game change'], 'best original score - motion picture': ['argo', 'anna karenina', 'cloud atlas', 'lincoln', 'life of pi'], 'best performance by an actress in a television series - drama': ['connie britton', 'glenn close', 'michelle dockery', 'julianna margulies', 'claire danes'], 'best performance by an actress in a motion picture - drama': ['marion cotillard', 'sally field', 'helen mirren', 'naomi watts', 'rachel weisz', 'jessica chastain'], 'cecil b. demille award': ['jodie foster'], 'best performance by an actor in a motion picture - comedy or musical': ['jack black', 'bradley cooper', 'ewan mcgregor', 'bill murray', 'hugh jackman'], 'best motion picture - drama': ['django unchained', 'life of pi', 'lincoln', 'zero dark thirty', 'argo'], 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ['max greenfield', 'danny huston', 'mandy patinkin', 'eric stonestreet', 'ed harris'], 'best performance by an actress in a supporting role in a motion picture': ['amy adams', 'sally field', 'helen hunt', 'nicole kidman', 'anne hathaway'], 'best television series - drama': ['boardwalk empire', 'breaking bad', 'downton abbey (masterpiece)', 'the newsroom', 'homeland'], 'best performance by an actor in a mini-series or motion picture made for television': ['benedict cumberbatch', 'woody harrelson', 'toby jones', 'clive owen', 'kevin costner'], 'best performance by an actress in a mini-series or motion picture made for television': ['nicole kidman', 'jessica lange', 'sienna miller', 'sigourney weaver', 'julianne moore'], 'best animated feature film': ['frankenweenie', 'hotel transylvania', 'rise of the guardians', 'wreck-it ralph', 'brave'], 'best original song - motion picture': ['act of valor', 'stand up guys', 'the hunger games', 'les miserables', 'skyfall'], 'best performance by an actor in a motion picture - drama': ['richard gere', 'john hawkes', 'joaquin phoenix', 'denzel washington', 'daniel day-lewis'], 'best television series - comedy or musical': ['the big bang theory', 'episodes', 'modern family', 'smash', 'girls'], 'best performance by an actor in a television series - drama': ['steve buscemi', 'bryan cranston', 'jeff daniels', 'jon hamm', 'damian lewis'], 'best performance by an actor in a television series - comedy or musical': ['alec baldwin', 'louis c.k.', 'matt leblanc', 'jim parsons', 'don cheadle']}
    nominees_dict_2015 = {'best screenplay - motion picture': ['the grand budapest hotel', 'gone girl', 'boyhood', 'the imitation game', 'birdman'], 'best director - motion picture': ['wes anderson', 'ava duvernay', 'david fincher', 'alejandro inarritu gonzalez', 'richard linklater'], 'best performance by an actress in a television series - comedy or musical': ['lena dunham', 'edie falco', 'julia louis-dreyfus', 'taylor schilling', 'gina rodriguez'], 'best foreign language film': ['force majeure', 'gett: the trial of viviane amsalem', 'ida', 'tangerines', 'leviathan'], 'best performance by an actor in a supporting role in a motion picture': ['robert duvall', 'edward norton', 'mark ruffalo', 'j.k. simmons'], 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': ['uzo aduba', 'kathy bates', 'allison janney', 'michelle monaghan', 'joanne froggatt'], 'best motion picture - comedy or musical': ['birdman', 'into the woods', 'pride', 'st. vincent', 'the grand budapest hotel'], 'best performance by an actress in a motion picture - comedy or musical': ['emily blunt', 'helen mirren', 'julianne moore', 'quvenzhane wallis', 'amy adams'], 'best mini-series or motion picture made for television': ['the missing', 'the normal heart', 'olive kitteridge', 'true detective', 'fargo'], 'best original score - motion picture': ['the imitation game', 'birdman', 'gone girl', 'interstellar', 'the theory of everything'], 'best performance by an actress in a television series - drama': ['claire danes', 'viola davis', 'julianna margulies', 'robin wright', 'ruth wilson'], 'best performance by an actress in a motion picture - drama': ['jennifer aniston', 'felicity jones', 'rosamund pike', 'reese witherspoon', 'julianne moore'], 'cecil b. demille award': ['george clooney'], 'best performance by an actor in a motion picture - comedy or musical': ['ralph fiennes', 'bill murray', 'joaquin phoenix', 'christoph waltz', 'michael keaton'], 'best motion picture - drama': ['foxcatcher', 'the imitation game', 'selma', 'the theory of everything', 'boyhood'], 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': ['alan cumming', 'colin hanks', 'bill murray', 'jon voight', 'matt bomer'], 'best performance by an actress in a supporting role in a motion picture': ['jessica chastain', 'keira knightley', 'emma stone', 'meryl streep', 'patricia arquette'], 'best television series - drama': ['downton abbey (masterpiece)', 'game of thrones', 'the good wife', 'house of cards', 'the affair'], 'best performance by an actor in a mini-series or motion picture made for television': ['martin freeman', 'woody harrelson', 'matthew mcconaughey', 'mark ruffalo', 'billy bob thornton'], 'best performance by an actress in a mini-series or motion picture made for television': ['jessica lange', 'frances mcdormand', "frances o'connor", 'allison tolman', 'maggie gyllenhaal'], 'best animated feature film': ['big hero 6', 'the book of life', 'the boxtrolls', 'the lego movie', 'how to train your dragon 2'], 'best original song - motion picture': ['big eyes', 'noah', 'annie', 'the hunger games: mockingjay - part 1', 'selma'], 'best performance by an actor in a motion picture - drama': ['steve carell', 'benedict cumberbatch', 'jake gyllenhaal', 'david oyelowo', 'eddie redmayne'], 'best television series - comedy or musical': ['girls', 'jane the virgin', 'orange is the new black', 'silicon valley', 'transparent'], 'best performance by an actor in a television series - drama': ['clive owen', 'liev schreiber', 'james spader', 'dominic west', 'kevin spacey'], 'best performance by an actor in a television series - comedy or musical': ['louis c.k.', 'don cheadle', 'ricky gervais', 'william h. macy', 'jeffrey tambor']}


    winner_2013 = get_winner_all_awards('gg2013_clean.json', nominees_dict_2013)
    winner_2015 = get_winner_all_awards('gg2015_clean.json', nominees_dict_2015)


if __name__ == "__main__":
    main()