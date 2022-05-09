import json
import sys
from json_reader import load_tweets, clean_and_save
from host_parser import get_host
from get_awards import get_awards
from get_presenter import *

def save_to_json(input_file):
    tweets = load_tweets(input_file)
    output = {}
    hosts = get_host(tweets)
    output['hosts'] = hosts
    award_data = {}
    award_names = get_awards(tweets)
    print('{} awards found'.format(len(award_names)))
    i = 1
    for award_name in award_names:
        items = {}
        items['nominees'] = []
        items['winner'] = []
        award = Award(i, award_name, 'actor')
        i = i + 1
        presenters = presenter_from_dict(find_presenter(tweets, award))
        items['presenters'] = presenters
        award_data[award_name] = items

    output['award_data'] = award_data
    path = 'data/ans_' + input_file
    print('Writing answer to json file:')
    with open(path, 'w') as ans_file:
        json.dump(output, ans_file)
    print('Finishing writing {}'.format(path))


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
    main('gg2013_clean.json', 'gg2015_clean.json')


