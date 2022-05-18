from english_words import english_words_lower_alpha_set

from award_time import get_time
from json_reader import *
from classes import *
import re
import nltk
import spacy
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
nlp = spacy.load("en_core_web_sm")
from difflib import SequenceMatcher


def clean_award_name(name):
    # clean award name into tokens of important words
    name = name.lower()
    stop_words = ['a', 'an', 'the', 'and', 'of', 'as', 'to', 'at', 'in', 'on', 'is', 'are', 'was', 'were', 'by', 'or',
                  'for',
                  'original', 'film', 'performance', 'motion', 'picture', 'award', 'role']
    name = re.sub(r"\.|\?|\!|\'|\"|\(|\)|\[|\]|,|-", ' ', name)
    name_words = []
    for w in name.split():
        if w not in stop_words:
            name_words.append(w)
    return name_words


def get_l_r_time(time_award):
    left_time = (time_award - 120)*1000
    right_time = (time_award + 90)*1000
    return left_time, right_time


def winner_related(t, time, name_words, left_time, right_time):
    '''
    Input:
        - Take a text and an award
    Output:
        - Return True if text is related to the award, False otherwise
    '''
    t_lower = t.lower()

    '''
    if 'winner' not in t_lower:
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


'''
def related_to_award(text, award):
    """
    Input:
        - Take some text and an award
    Output:
        - Return True if text is related to the award and potential winners, False otherwise
    """
    name = award.name.lower()  # clean award input text
    keyword = 'for ' + name  # seemingly reliable keyword
    winner_words = [keyword, 'winners', 'winner', 'is winnerd for']
    # ^will probably replace these with regexp phrases

    if name not in text.lower():  # if award isn't mentioned in text ret False
        return False

    for w in winner_words:
        if w in text.lower():
            return True

    return False
    '''


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


# caller function will manage splitting text, this function will only look at sentence chunks
def winner_candidates(text, cand_dict, paf):
    candidate_lists = []
    keyphrasesb4 = [r"\swins", r"\swinner\sof", r"\shaswon", r"\swas\swinnerd", r"\sis\sthe\swinner",
                    r"\swins\sthe", r"\sgoes\sto", r"\sbeats"
                    r"\stakes\shome", r"\sbrings\shome", r"\sbeat\sout", r"\sbeats\sout", r"\spicks\sfor",  r"\sover"]

    keyphrasesaftr = [r"\swinners:", r"\scongratulations\sto",
                      r"\scongrats\sto", r"\sgoes\sto", r"\sbeats", r"\scan't\sbelieve", r"\sbeat\sout",
                      r"\sbeats\sout", r"...\s", r"\spicks\sfor", r"\sloses\sto", r"\slost\sto"]
    redflag_phrases = []
    for kp in keyphrasesaftr:
        fa_str = "(?<=" + kp + ").*"
        new_cand = re.findall(fa_str, text)
        if new_cand != [] and new_cand not in candidate_lists:
            new_cand = [i for i in new_cand if i != '']
            candidate_lists.append(new_cand)
    for kp in keyphrasesb4:
        fa_str = ".*(?=" + kp + ")"
        new_cand = re.findall(fa_str, text)
        if new_cand != [] and new_cand not in candidate_lists:
            new_cand = [i for i in new_cand if i != '']
            candidate_lists.append(new_cand)
    for candidate_list in candidate_lists:
        for sentence in candidate_list:
            if paf:
                locn = human_name(sentence)
            else:
                locn = non_human_name(sentence)

            for cand in locn:
                if cand in cand_dict:
                    cand_dict[cand] += 1
                else:
                    cand_dict[cand] = 1


def non_human_name(text):
    name_list = []
    expressions = [r'"[A-Z][a-z]*(\s([A-Z]|[a-z])[a-z]*)*"', r"'[A-Z][a-z]*(\s([A-Z]|[a-z])[a-z]*)*'",
                   '''"(?:[^\\"]|\\\\|\\")*"''', '''"[^"]*"''', ''' '[a-zA-Z]+.*' ''',
                   ''' '([a-zA-Z]+( [a-zA-Z]+)+).*'.*'[a-zA-Z]+.*' ''', '''"[^"]*"''',
                   r"'[A-Z][a-z]*(\s[A-Z][a-z]*)*'", r'"[A-Z][a-z]*(\s[A-Z][a-z]*)*"',
                   r"(?<=\sthe\smovie\s)(.*?)(,|;|\.)", r"(?<=\sthe\ssong\s)(.*?)(,|;|\.)",
                   r"(?<=\sthe\strack\s)(.*?)(,|;|\.)", r"(?<=\sthe\splay\s)(.*?)(,|;|\.)",
                   r"(?<=\sthe\salbum\s)(.*?)(,|;|\.)", r"(?<=\sthe\sperformance\s)(.*?)(,|;|\.)"]
    for expr in expressions:
        new_name = re.findall(expr, text)
        if new_name != [] and new_name not in name_list:
            new_name = [i for i in new_name if i != '']
            if hasattr(new_name, '__iter__'):
                for tpl in new_name:
                    name_list.append(re.sub(r'[^a-zA-Z\s]', '', "".join(tpl)))
            else:
                name_list.append(re.sub(r'[^a-zA-Z\s]', '', "".join(new_name)))
    return [i for i in name_list if i != '']


def human_name(text):
    name_list = []
    doc = nlp(text)
    for ent in doc.ents:
       if ent.label_ == 'PERSON':
           name_list.append(ent.text)
    for name in name_list:
        if "@" in name:
            name_list.remove(name)
    return name_list

'''
    name_list = []
    nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                name += nltk_result_leaf[0] + ' '
            name_list.append(name)
    return name_list
'''


def find_winners(data, award, time_award):
    potential_winners = {}
    person_award_flag = False
    person_award_kps = ["actor", "actress", "artist", "director", "performance", "singer", "rapper", "producer", 'cecil b. demille award']
    for kp in person_award_kps:
        if kp in award.name:
            person_award_flag = True

    name_words = clean_award_name(award.name)
    left_time, right_time = get_l_r_time(time_award)
    for tweet in data:
        text = tweet['text']
        if winner_related(text, tweet['timestamp_ms'], name_words, left_time, right_time):
            sentences = re.split(r"[.?!;]", text)
            for sentence in sentences:
                # sentence = sentence.lower() #this would make name recognition impossible using nltk
                winner_candidates(sentence, potential_winners, person_award_flag)
    clean_similar_winrs(potential_winners)
    potential_winners = sort_dict(potential_winners)
    return potential_winners
    #return clean_similar_winrs(potential_winners)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def clean_similar_winrs(win_dict):
    for candi in win_dict:
        for candj in win_dict:
            if similar(candi, candj) >= .4 and candi != candj and (win_dict[candi] != -1 and win_dict[candj] != -1):
                if win_dict[candi] > win_dict[candj]:
                    win_dict[candi] += win_dict[candj]
                    win_dict[candj] = -1
                else:
                    break


def winners_for_award(win_dict):
    for nom in win_dict:
        print(nom, win_dict[nom])


def find_winner(words):
    """
    Input:
        - Take a list of words
    Output:
        - return the index of first word that contains winner, return -1 otherwise
    """
    winner_related_words = ['nomina', 'winners', 'win', 'won', 'lost', 'lose']

    for i in range(len(words)):
        if any([(word in words[i].lower()) for word in winner_related_words]):
            return i

    return -1


def winner_data(tweets):
    winner_tweets = []
    winner_related_words = ['nominat', 'winners',  'win', 'won', 'lost', 'lose']
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        t_split = t.split()
        if any([(word in t_split) for word in winner_related_words]):
            words = t.split()
            index = find_winner(words)
            prefix = ' '.join(words[0:(index + 2)])
            if prefix not in tweet_set:
                winner_tweets.append(tweet)
                tweet_set.add(prefix)

    return winner_tweets


def an_award_name(cand, text):
    cand_list = cand.split()
    bool_vec = cand_list
    for word in cand_list:
        for award in text:
            if word not in award.split():
                continue
            else:
                bool_vec[cand_list.index(word)] = True
                break
    for e in bool_vec:
        if not isinstance(e, bool):
            return False
    return True


def get_winner_all_awards(tweet_file_name, award_names):
    file_name_length = len(tweet_file_name)
    file_name_wth_json = tweet_file_name[0:file_name_length - 5]
    get_time(tweet_file_name, award_names)

    time_award = load_tweets(file_name_wth_json + "_award_time.json")

    tweets = load_tweets(tweet_file_name)

    winner_tweets = winner_data(tweets)
    winners = {}
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i+1
        time_happen = int(time_award[name])
        winners_dict = find_winners(winner_tweets, award, time_happen)
        #print(name + " Nominees: \n")
        #print('\n')
        # winners_dict = {key: val for key, val in winners_dict.items() if val >= 11}
        def_not_winners = ["#GoldenGlobes", "Golden Globes", "GoldenGlobes", "Grammys", "Emmys", "oscar", "Oscar"]
        winners_dict = {key: val for key, val in winners_dict.items() if (val != -1 and (not an_award_name(key.lower(), award_names)) and key not in def_not_winners)}
        new_dict = {}
        j = 0
        for key in winners_dict:
            if j < 1:
                new_dict[key] = winners_dict[key]
                j += 1
            else:
                break
        #winners_for_award(new_dict)
        winner = [key.lower() for key in new_dict.keys()]
        winners[name] = winner
    with open("data/winners_" + file_name_wth_json + ".json", "w") as outfile:
        json.dump(winners, outfile)
    return winners


def main():
    award_names = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    winner_2013 = get_winner_all_awards('gg2013_clean.json', award_names)
    print('###########################################################################')
    winner_2015 = get_winner_all_awards('gg2015_clean.json', award_names)


if __name__ == "__main__":
    main()
