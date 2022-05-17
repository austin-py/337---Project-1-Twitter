from json_reader import *
from classes import *
import re
import nltk
import spacy
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
nlp = spacy.load("en_core_web_sm")
global global_award_pick

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
def nominee_candidates(text, cand_dict):
    candidate_lists = []
    keyphrasesb4 = [r"\swins", r"\snominated\sfor", r"\swinner\sof", r"\shaswon", r"\swas\snominated", r"\sis\snominated",
                    r"\swins\sthe", r"\slost", r"\sloses\sto",
                    r"\slost\sto", r"\sdid\snot\swin", r"\sdidn't\swin", r"\sgoes\sto", r"\sup\sfor", r"\sbeats"
                    r"\stakes\shome", r"\sbrings\shome", r"\sbeat\sout", r"\sbeats\sout"]

    keyphrasesaftr = [r"\snominated", r"\shas\snominated", r"\shave\snominated", r"\snominates", r"\scongratulations\sto",
                      r"\scongrats\sto", r"\sgoes\sto", r"\sover", r"\sbeats", r"\scan't\sbelieve", r"\sbeat\sout",
                      r"\sbeats\sout", r"...\s"]
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
            global global_award_pick
            if global_award_pick == "best motion picture":
                stop = True
            locn = human_name(sentence)
            for cand in locn:
                if cand in cand_dict:
                    cand_dict[cand] += 1
                else:
                    cand_dict[cand] = 1


def non_human_name(text):
    name_list = []
    expressions = [r'"[A-Z][a-z]*(\s([A-Z]|[a-z])[a-z]*)*"', r"'[A-Z][a-z]*(\s([A-Z]|[a-z])[a-z]*)*'",
                   r"'[A-Z][a-z]*(\s[A-Z][a-z]*)*'", r'"[A-Z][a-z]*(\s[A-Z][a-z]*)*"',
                   r"(?<=\sthe\smovie\s)(.*?)(,|;|\.)", r"(?<=\sthe\ssong\s)(.*?)(,|;|\.)",
                   r"(?<=\sthe\strack\s)(.*?)(,|;|\.)", r"(?<=\sthe\splay\s)(.*?)(,|;|\.)",
                   r"(?<=\sthe\salbum\s)(.*?)(,|;|\.)", r"(?<=\sthe\sperformance\s)(.*?)(,|;|\.)"]
    for expr in expressions:
        new_name = re.findall(expr, text)
        if new_name != [] and new_name not in name_list:
            new_name = [i for i in new_name if i != '']
            name_list.append(new_name)


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
def find_nominees(data, award):
    potential_nominees = {}
    for tweet in data:
        text = tweet['text']
        if related_to_award(text, award):
            sentences = re.split("\.|\?|\!", text)
            for sentence in sentences:
                # sentence = sentence.lower() #this would make name recognition impossible using nltk
                nominee_candidates(sentence, potential_nominees)

    return sort_dict(potential_nominees)


def nominees_for_award(nom_dict):
    for nom in nom_dict:
        print(nom, nom_dict[nom])


def main():
    tweets = load_tweets(r'gg2013.json')
    award_names = ['best supporting actor', 'best supporting actress', 'best director', 'best motion picture',
                   'best actor', 'best actress', 'best screen play', 'best animated feature film', 'best television series']
    i = 1
    for name in award_names:
        global global_award_pick
        global_award_pick = name
        award = Award(i, name, 'actor')
        i = i+1
        nominees_dict = find_nominees(tweets, award)
        nominees_for_award(nominees_dict)
        # nominees = nominees_for_award(nominees_dict)
        '''
        print(name + " Nominees: ")
        for nominee in nominees:
            print(nominee)
            print('\n')
        '''


if __name__ == "__main__":
    main()
