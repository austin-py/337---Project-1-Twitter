from json_reader import *
from classes import *
import re
import nltk
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


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
    keyphrases = ["\swins", "\snominated\sfor", "\swinner\sof", "\shaswon", "\snominated", "\swins\sthe", "\slost", "\sloses\sto",
                  "\slost\sto", "\sdid\snot\swin", "\sdidn't\swin", "\sgoes\sto"]
    redflag_phrases = []
    for kp in keyphrases:
        fa_str = f".*(?= {kp})"
        candidate_lists.append(re.findall(fa_str, text))

    for candidate_list in candidate_lists:
        for word in candidate_list:
            if human_name(word):
                if word in cand_dict:  # add a red flag checker for a more refined score
                    cand_dict[word] += 1
                else:
                    cand_dict[word] = 1


def human_name(word):
    return type(ne_chunk(pos_tag(word_tokenize(word)))) == Tree


def find_nominees(data, award):
    potential_nominees = {}
    for tweet in data:
        text = tweet['text']
        if related_to_award(text, award):
            sentences = re.split("\.|\?|\!", text)
            for sentence in sentences:
                sentence = sentence.lower()
                nominee_candidates(sentence, potential_nominees)

    return sort_dict(potential_nominees)

def nominees_for_award(nom_dict):
        for nom in nom_dict:
        print(nom_dict[nom])


def main():
    tweets = load_tweets('gg2013.json')
    award_names = ['best supporting actor', 'best supporting actress', 'best director', 'best motion picture',
                   'best actor', 'best actress', 'best screen play', 'best animated feature film', 'best television series']
    i = 1
    for name in award_names:
        award = Award(i, name, 'actor')
        i = i+1
        nominees_dict = find_nominees(tweets, award)
        nominees = nominees_for_award(nominees_dict)
        '''
        print(name + " Nominees: ")
        for nominee in nominees:
            print(nominee)
            print('\n')
        '''


if __name__ == "__main__":
    main()
