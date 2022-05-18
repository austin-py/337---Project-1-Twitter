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


'''
def related_to_award(text, award):
    """
    Input:
        - Take some text and an award
    Output:
        - Return True if text is related to the award and potential nominees, False otherwise
    """
    name = award.name.lower()  # clean award input text
    keyword = 'for ' + name  # seemingly reliable keyword
    nominee_words = [keyword, 'nominees', 'nominee', 'is nominated for']
    # ^will probably replace these with regexp phrases

    if name not in text.lower():  # if award isn't mentioned in text ret False
        return False

    for w in nominee_words:
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
def nominee_candidates(text, cand_dict, paf):
    candidate_lists = []
    keyphrasesb4 = [r"\swins", r"\snominated\sfor", r"\swinner\sof", r"\shaswon", r"\swas\snominated", r"\sis\snominated",
                    r"\swins\sthe", r"\slost", r"\sloses\sto",
                    r"\slost\sto", r"\sdid\snot\swin", r"\sdidn't\swin", r"\sgoes\sto", r"\sup\sfor", r"\sbeats"
                    r"\stakes\shome", r"\sbrings\shome", r"\sbeat\sout", r"\sbeats\sout", r"\spicks\sfor"]

    keyphrasesaftr = [r"\snominated", r"\shas\snominated", r"\shave\snominated", r"\snominates", r"\scongratulations\sto",
                      r"\scongrats\sto", r"\sgoes\sto", r"\sover", r"\sbeats", r"\scan't\sbelieve", r"\sbeat\sout",
                      r"\sbeats\sout", r"...\s", r"\spicks\sfor"]
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
        if (new_name != [] and new_name != None) and new_name not in name_list:
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
def find_nominees(data, award, time_award):
    potential_nominees = {}
    person_award_flag = False
    person_award_kps = ["actor", "actress", "artist", "director", "performance", "singer", "rapper", "producer"]
    for kp in person_award_kps:
        if kp in award.name:
            person_award_flag = True

    name_words = clean_award_name(award.name)
    left_time, right_time = get_l_r_time(time_award)
    for tweet in data:
        text = tweet['text']
        if nominate_related(text, tweet['timestamp_ms'], name_words, left_time, right_time):
            sentences = re.split(r"[.?!;]", text)
            for sentence in sentences:
                # sentence = sentence.lower() #this would make name recognition impossible using nltk
                nominee_candidates(sentence, potential_nominees, person_award_flag)
    potential_nominees = sort_dict(potential_nominees)
    return potential_nominees
    #return clean_similar_noms(potential_nominees)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def clean_similar_noms(nom_dict):
    for candi in nom_dict:
        for candj in nom_dict:
            if similar(candi, candj) >= .54 and candi != candj and (nom_dict[candi] != -1 and nom_dict[candj] != -1):
                if nom_dict[candi] > nom_dict[candj]:
                    nom_dict[candi] += nom_dict[candj]
                    nom_dict[candj] = -1
                else:
                    break


def nominees_for_award(nom_dict):
    for nom in nom_dict:
        print(nom, nom_dict[nom])

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


def nominate_data(tweets):
    nominate_tweets = []
    nominate_related_words = ['nominat', 'nominees',  'win', 'won', 'lost', 'lose']
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        t_split = t.split()
        if any([(word in t_split) for word in nominate_related_words]):
            words = t.split()
            index = find_nominate(words)
            prefix = ' '.join(words[0:(index + 2)])
            if prefix not in tweet_set:
                nominate_tweets.append(tweet)
                tweet_set.add(prefix)

    return nominate_tweets


def get_nominee_all_awards(tweet_file_name, award_names):
    file_name_length = len(tweet_file_name)
    file_namw_wth_json = tweet_file_name[0:file_name_length - 5]
    get_time(tweet_file_name, award_names)

    time_award = load_tweets(file_namw_wth_json + "_award_time.json")

    tweets = load_tweets(tweet_file_name)

    nominate_tweets = nominate_data(tweets)
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i+1
        time_happen = int(time_award[name])
        nominees_dict = find_nominees(nominate_tweets, award, time_happen)
        print(name + " Nominees: \n")
        print('\n')
        # nominees_dict = {key: val for key, val in nominees_dict.items() if val >= 11}
        new_dict = {}
        j = 0
        for key in nominees_dict:
            if j < 5:
                new_dict[key] = nominees_dict[key]
                j += 1
            else:
                break
        nominees_for_award(new_dict)
        # nominees = nominees_for_award(nominees_dict)
        '''
        print(name + " Nominees: ")
        for nominee in nominees:
            print(nominee)
            print('\n')
        '''


def main():
    award_names = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
    nominee_2013 = get_nominee_all_awards('gg2013_clean.json', award_names)
    print('###########################################################################')
    nominee_2015 = get_nominee_all_awards('gg2015_clean.json', award_names)


if __name__ == "__main__":
    main()
