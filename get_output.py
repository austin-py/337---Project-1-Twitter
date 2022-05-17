import json
import sys

import get_nominees
from json_reader import load_tweets, clean_and_save
from host_parser import get_host
from get_awards import get_awards
from get_presenter import *
from get_nominees import *
from os.path import exists

def save_to_json(input_file):
    tweets = load_tweets(input_file)
    output = {}
    hosts = get_host(tweets)
    output['hosts'] = hosts
    award_data = {}

    #Not sure how not to hard-code awards while still use official award names
    #award_names = get_awards(tweets)
    #print('{} awards found'.format(len(award_names)))

    official_award_names = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    # official_award_names = ['best supporting actor', 'best supporting actress', 'best director', 'best motion picture',
    #                'best actor', 'best actress', 'best screen play', 'best animated feature film',
    #                'best television series']

    print('Number of official award names {}'.format(len(official_award_names)))
    award_to_present_dict = get_presenter_all_awards(input_file, official_award_names)
    i = 1
    for award_name, presenters in award_to_present_dict.items():
        elements = {'nominees': [], 'winner': [], 'presenters': presenters}
        get_nominees.global_award_pick = award_name
        award = Award(i, award_name, 'actor')
        i = i + 1
        sorted_nominees_dict = sort_dict(find_nominees(tweets, award))
        elements['nominees'] = list(sorted_nominees_dict.keys())
        award_data[award_name] = elements

    output['award_data'] = award_data
    path = 'data/' + input_file
    path = path.replace('.json', '_answers.json')
    #with open('data/gg%s_clean_answers.json' % year, 'r') as f:
    print('Writing answer to json file:')
    with open(path, 'w') as ans_file:
        json.dump(output, ans_file)
    print('Finishing writing {}'.format(path))

def save_to_txt(input_file):
    path = 'data/' + input_file
    ans_path = path.replace('.json', '_answers.json')
    if not exists(ans_path):
        save_to_json(input_file)
    with open(path, 'r') as answer_file:
        dict_answers = json.load(answer_file)

    print('hosts: {}'.format())




def main(*args):
    if len(sys.argv) > 1:
        print('Running {}:'.format(sys.argv[0]))
        for i in range(1, len(sys.argv)):
            save_to_json(sys.argv[i])
        print('Finishing running {}'.format(sys.argv[0]))
    elif len(args) != 0:
        for arg in args:
            save_to_json(arg)
    else:
        default_input = 'gg2013_clean.json'
        print('No input file provided, reading default input file: {}'.format(default_input))
        save_to_json(default_input)


if __name__ == '__main__':
    #take multiple input files
    main('gg2013_clean.json', 'gg2015_clean.json')
    #save_to_txt('gg2013_clean.json')
    #main()


