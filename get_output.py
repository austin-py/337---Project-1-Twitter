import json
import sys

import get_nominees
from json_reader import load_tweets, clean_and_save
from host_parser import get_host
from get_awards import return_awards, get_best_dressed, get_worst_dressed
from get_presenter import *
from get_nominees_2 import *
from get_winner_2 import *
from sentiment_analysis import *
#from get_nominees import *
#from get_winners import *
from os.path import exists

from textblob import TextBlob
import nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')



def save_to_json(input_file):
    tweets = load_tweets(input_file)
    clean_file = input_file.replace('.json', '_clean.json')
    clean_and_save(input_file, clean_file)
    clean_tweets = load_tweets(clean_file)
    output = {}
    hosts = get_host(clean_tweets)
    output['hosts'] = hosts
    award_data = {}

    award_names = return_awards(tweets)
    output['awards'] = award_names
    print('{} awards found'.format(len(award_names)))

    OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama',
                            'best performance by an actress in a motion picture - drama',
                            'best performance by an actor in a motion picture - drama',
                            'best motion picture - comedy or musical',
                            'best performance by an actress in a motion picture - comedy or musical',
                            'best performance by an actor in a motion picture - comedy or musical',
                            'best animated feature film', 'best foreign language film',
                            'best performance by an actress in a supporting role in a motion picture',
                            'best performance by an actor in a supporting role in a motion picture',
                            'best director - motion picture', 'best screenplay - motion picture',
                            'best original score - motion picture', 'best original song - motion picture',
                            'best television series - drama',
                            'best performance by an actress in a television series - drama',
                            'best performance by an actor in a television series - drama',
                            'best television series - comedy or musical',
                            'best performance by an actress in a television series - comedy or musical',
                            'best performance by an actor in a television series - comedy or musical',
                            'best mini-series or motion picture made for television',
                            'best performance by an actress in a mini-series or motion picture made for television',
                            'best performance by an actor in a mini-series or motion picture made for television',
                            'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television',
                            'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

    print('Number of official award names {}'.format(len(OFFICIAL_AWARDS_1315)))
    award_to_present_dict = get_presenter_all_awards(clean_file, OFFICIAL_AWARDS_1315)
    award_to_nominee_dict = get_nominee_all_awards(clean_file, OFFICIAL_AWARDS_1315)


    nominees_dict_2013 = {
        'best screenplay - motion picture': ['zero dark thirty', 'lincoln', 'silver linings playbook', 'argo',
                                             'django unchained'],
        'best director - motion picture': ['kathryn bigelow', 'ang lee', 'steven spielberg', 'quentin tarantino',
                                           'ben affleck'],
        'best performance by an actress in a television series - comedy or musical': ['zooey deschanel', 'tina fey',
                                                                                      'julia louis-dreyfus',
                                                                                      'amy poehler', 'lena dunham'],
        'best foreign language film': ['the intouchables', 'kon tiki', 'a royal affair', 'rust and bone', 'amour'],
        'best performance by an actor in a supporting role in a motion picture': ['alan arkin', 'leonardo dicaprio',
                                                                                  'philip seymour hoffman',
                                                                                  'tommy lee jones', 'christoph waltz'],
        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': [
            'hayden panettiere', 'archie panjabi', 'sarah paulson', 'sofia vergara', 'maggie smith'],
        'best motion picture - comedy or musical': ['the best exotic marigold hotel', 'moonrise kingdom',
                                                    'salmon fishing in the yemen', 'silver linings playbook',
                                                    'les miserables'],
        'best performance by an actress in a motion picture - comedy or musical': ['emily blunt', 'judi dench',
                                                                                   'maggie smith', 'meryl streep',
                                                                                   'jennifer lawrence'],
        'best mini-series or motion picture made for television': ['the girl', 'hatfields & mccoys', 'the hour',
                                                                   'political animals', 'game change'],
        'best original score - motion picture': ['argo', 'anna karenina', 'cloud atlas', 'lincoln', 'life of pi'],
        'best performance by an actress in a television series - drama': ['connie britton', 'glenn close',
                                                                          'michelle dockery', 'julianna margulies',
                                                                          'claire danes'],
        'best performance by an actress in a motion picture - drama': ['marion cotillard', 'sally field',
                                                                       'helen mirren', 'naomi watts', 'rachel weisz',
                                                                       'jessica chastain'],
        'cecil b. demille award': ['jodie foster'],
        'best performance by an actor in a motion picture - comedy or musical': ['jack black', 'bradley cooper',
                                                                                 'ewan mcgregor', 'bill murray',
                                                                                 'hugh jackman'],
        'best motion picture - drama': ['django unchained', 'life of pi', 'lincoln', 'zero dark thirty', 'argo'],
        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': [
            'max greenfield', 'danny huston', 'mandy patinkin', 'eric stonestreet', 'ed harris'],
        'best performance by an actress in a supporting role in a motion picture': ['amy adams', 'sally field',
                                                                                    'helen hunt', 'nicole kidman',
                                                                                    'anne hathaway'],
        'best television series - drama': ['boardwalk empire', 'breaking bad', 'downton abbey (masterpiece)',
                                           'the newsroom', 'homeland'],
        'best performance by an actor in a mini-series or motion picture made for television': ['benedict cumberbatch',
                                                                                                'woody harrelson',
                                                                                                'toby jones',
                                                                                                'clive owen',
                                                                                                'kevin costner'],
        'best performance by an actress in a mini-series or motion picture made for television': ['nicole kidman',
                                                                                                  'jessica lange',
                                                                                                  'sienna miller',
                                                                                                  'sigourney weaver',
                                                                                                  'julianne moore'],
        'best animated feature film': ['frankenweenie', 'hotel transylvania', 'rise of the guardians', 'wreck-it ralph',
                                       'brave'],
        'best original song - motion picture': ['act of valor', 'stand up guys', 'the hunger games', 'les miserables',
                                                'skyfall'],
        'best performance by an actor in a motion picture - drama': ['richard gere', 'john hawkes', 'joaquin phoenix',
                                                                     'denzel washington', 'daniel day-lewis'],
        'best television series - comedy or musical': ['the big bang theory', 'episodes', 'modern family', 'smash',
                                                       'girls'],
        'best performance by an actor in a television series - drama': ['steve buscemi', 'bryan cranston',
                                                                        'jeff daniels', 'jon hamm', 'damian lewis'],
        'best performance by an actor in a television series - comedy or musical': ['alec baldwin', 'louis c.k.',
                                                                                    'matt leblanc', 'jim parsons',
                                                                                    'don cheadle']}
    nominees_dict_2015 = {
        'best screenplay - motion picture': ['the grand budapest hotel', 'gone girl', 'boyhood', 'the imitation game',
                                             'birdman'],
        'best director - motion picture': ['wes anderson', 'ava duvernay', 'david fincher',
                                           'alejandro inarritu gonzalez', 'richard linklater'],
        'best performance by an actress in a television series - comedy or musical': ['lena dunham', 'edie falco',
                                                                                      'julia louis-dreyfus',
                                                                                      'taylor schilling',
                                                                                      'gina rodriguez'],
        'best foreign language film': ['force majeure', 'gett: the trial of viviane amsalem', 'ida', 'tangerines',
                                       'leviathan'],
        'best performance by an actor in a supporting role in a motion picture': ['robert duvall', 'edward norton',
                                                                                  'mark ruffalo', 'j.k. simmons'],
        'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': [
            'uzo aduba', 'kathy bates', 'allison janney', 'michelle monaghan', 'joanne froggatt'],
        'best motion picture - comedy or musical': ['birdman', 'into the woods', 'pride', 'st. vincent',
                                                    'the grand budapest hotel'],
        'best performance by an actress in a motion picture - comedy or musical': ['emily blunt', 'helen mirren',
                                                                                   'julianne moore',
                                                                                   'quvenzhane wallis', 'amy adams'],
        'best mini-series or motion picture made for television': ['the missing', 'the normal heart',
                                                                   'olive kitteridge', 'true detective', 'fargo'],
        'best original score - motion picture': ['the imitation game', 'birdman', 'gone girl', 'interstellar',
                                                 'the theory of everything'],
        'best performance by an actress in a television series - drama': ['claire danes', 'viola davis',
                                                                          'julianna margulies', 'robin wright',
                                                                          'ruth wilson'],
        'best performance by an actress in a motion picture - drama': ['jennifer aniston', 'felicity jones',
                                                                       'rosamund pike', 'reese witherspoon',
                                                                       'julianne moore'],
        'cecil b. demille award': ['george clooney'],
        'best performance by an actor in a motion picture - comedy or musical': ['ralph fiennes', 'bill murray',
                                                                                 'joaquin phoenix', 'christoph waltz',
                                                                                 'michael keaton'],
        'best motion picture - drama': ['foxcatcher', 'the imitation game', 'selma', 'the theory of everything',
                                        'boyhood'],
        'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': [
            'alan cumming', 'colin hanks', 'bill murray', 'jon voight', 'matt bomer'],
        'best performance by an actress in a supporting role in a motion picture': ['jessica chastain',
                                                                                    'keira knightley', 'emma stone',
                                                                                    'meryl streep',
                                                                                    'patricia arquette'],
        'best television series - drama': ['downton abbey (masterpiece)', 'game of thrones', 'the good wife',
                                           'house of cards', 'the affair'],
        'best performance by an actor in a mini-series or motion picture made for television': ['martin freeman',
                                                                                                'woody harrelson',
                                                                                                'matthew mcconaughey',
                                                                                                'mark ruffalo',
                                                                                                'billy bob thornton'],
        'best performance by an actress in a mini-series or motion picture made for television': ['jessica lange',
                                                                                                  'frances mcdormand',
                                                                                                  "frances o'connor",
                                                                                                  'allison tolman',
                                                                                                  'maggie gyllenhaal'],
        'best animated feature film': ['big hero 6', 'the book of life', 'the boxtrolls', 'the lego movie',
                                       'how to train your dragon 2'],
        'best original song - motion picture': ['big eyes', 'noah', 'annie', 'the hunger games: mockingjay - part 1',
                                                'selma'],
        'best performance by an actor in a motion picture - drama': ['steve carell', 'benedict cumberbatch',
                                                                     'jake gyllenhaal', 'david oyelowo',
                                                                     'eddie redmayne'],
        'best television series - comedy or musical': ['girls', 'jane the virgin', 'orange is the new black',
                                                       'silicon valley', 'transparent'],
        'best performance by an actor in a television series - drama': ['clive owen', 'liev schreiber', 'james spader',
                                                                        'dominic west', 'kevin spacey'],
        'best performance by an actor in a television series - comedy or musical': ['louis c.k.', 'don cheadle',
                                                                                    'ricky gervais', 'william h. macy',
                                                                                    'jeffrey tambor']}

    award_to_winner_dict = {}
    if '2013' in input_file:
        award_to_winner_dict = get_winner_all_awards('gg2013_clean.json', nominees_dict_2013)
    elif '2015' in input_file:
        award_to_winner_dict = get_winner_all_awards('gg2015_clean.json', nominees_dict_2015)
    else:
        print('Unexpected input file to get winners: {}'.format(input_file))

    for award_name in OFFICIAL_AWARDS_1315:
        elements = {'nominees': award_to_nominee_dict[award_name],
                    'winner': award_to_winner_dict[award_name],
                    'presenters': award_to_present_dict[award_name]}
        award_data[award_name] = elements

    output['award_data'] = award_data
    path = 'data/' + input_file
    path = path.replace('.json', '_answers.json')
    #with open('data/gg%s_clean_answers.json' % year, 'r') as f:
    print('Writing answer to json file:')
    with open(path, 'w') as ans_file:
        json.dump(output, ans_file)
    print('Finishing writing {}'.format(path))

def save_to_txt(year):
    ans_path = 'data/gg%s_answers.json' % year
    if not exists(ans_path):
        save_to_json('data/gg%s.json' % year)

    with open(ans_path, 'r') as f:
        answers = json.load(f)

    with open('data/gg%s_answers.txt' % year, 'w') as f:
        f.write('Hosts: {}\n'.format(', '.join(answers['hosts'])))
        f.write('\n')
        award_data = answers['award_data']
        for key, value in award_data.items():
            f.write('Award: {}\n'.format(key.title()))
            for k, v in value.items():
                if type(v) == list:
                    list_to_string = ', '.join(v)
                    f.write('{}: {}\n'.format(k.capitalize(), list_to_string.title()))
                else:
                    f.write('{}: {}\n'.format(k.capitalize(), v.title()))
            f.write('\n-----------------------------------------------\n')

        # Sentiment Analysis
        f.write('SENTIMENT ANALYSIS OF HOSTS, PRESENTERS AND WINNERS OF YEAR {}.\n'.format(year))
        polarity, mean_polarity = get_sentiment_information('gg'+ year + '_clean.json', 'gg'+ year + '_answers.json')
        f.write('The average polarity (positive or negative sentiments) for the whole tweets corpora in {} is {}.\n'.format(year, mean_polarity))
        if mean_polarity >= 0:
            f.write('This means that overall sentiment reaction toward this year awards is generally positive.\n')
        else:
            f.write('This means that overall sentiment reaction toward this year awards is generally negative.\n')

        f.write('\nThe following are sentiment statistics of each hosts, presenters, and winners.\n')
        f.write('These statistics include average sentiment polarity, percentage of negative tweets, percentage of neutral tweets, percentage of positive tweets.\n')
        f.write('The list is presented in an decreasing average sentiment polarity orders:\n\n')
        for k in polarity.keys():
            f.write('{}: Average sentiment polarity - {:.2f}, negative tweets percentage - {:.2f}, neutral tweets percentage - {:.2f}, positive tweets percentage - {:.2f}.\n'.format(k, polarity[k][0], polarity[k][1], polarity[k][2], polarity[k][3]))

        # Best/Worst dressed. 

        f.write('\n\nRed Carpet Awards:\n')
        tweets = load_tweets('gg'+year+'.json')
        f.write('The twitter voted best dressed was',get_best_dressed(tweets))
        f.write('The twitter voted worst dressed was',get_worst_dressed(tweets))

        
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
        default_input = 'gg2013.json'
        print('No input file provided, reading default input file: {}'.format(default_input))
        save_to_json(default_input)


if __name__ == '__main__':
    #take multiple input files
    main('gg2013.json', 'gg2015.json')
    save_to_txt('2013')
    save_to_txt('2015')


