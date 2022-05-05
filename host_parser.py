from collections import OrderedDict

from json_reader import *
import re

def clean_tweet(input_tweet):
    amp_replaced = replace_amp(input_tweet)
    nonword_removed = remove_nonword_char(amp_replaced)
    cleaned = nonword_removed.lower()
    return cleaned

def remove_nonword_char(input_tweet):
    nonword_removed = re.sub(r'[\W]^\s', '', input_tweet)
    return nonword_removed

def replace_amp(input_tweet):
    replaced = input_tweet.replace('&amp;', 'and')
    return replaced

def has_host(input_tweet):
    host_forms = ['host', 'hosts', 'hosting', 'hosted']

    for form in host_forms:
        if form in input_tweet:
            return True
    return False

def get_host_majority_vote(tweets):
    present_result = {}
    present_participle_result = {}
    plural_noun_result = {}
    past_tense_result = {}
    # passive_result = {}
    # host_forms = ['host', 'hosts', 'hosting', 'hosted']
    for t in tweets:
        text = t['text']
        t_cleaned = clean_tweet(text)
        words = t_cleaned.lower().split()
        for w in words:
            if w == 'host':
                result = get_host_rule_present(t_cleaned, 'host')
                if result is not None:
                    for ngram in result:
                        if ngram in present_result:
                            present_result[ngram] += 1
                        else:
                            present_result[ngram] = 1
            if w == 'hosting':
                result = get_host_rule_present_participle(t_cleaned, 'hosting')
                if result is not None:
                    for ngram in result:
                        if ngram in present_participle_result:
                            present_participle_result[ngram] += 1
                        else:
                            present_participle_result[ngram] = 1
            if w == 'hosts':
                result = get_host_rule_plural_noun(t_cleaned, 'hosts')
                if result is not None:
                    for ngram in result:
                        if ngram in plural_noun_result:
                            plural_noun_result[ngram] += 1
                        else:
                            plural_noun_result[ngram] = 1
            if w == 'hosted':
                # passive result included
                result = get_host_rule_past_tense(t_cleaned, 'hosted')
                if result is not None:
                    for ngram in result:
                        if ngram in past_tense_result:
                            past_tense_result[ngram] += 1
                        else:
                            past_tense_result[ngram] = 1

    majority_vote_result = rank_and_select_final_answers(
        present_result, present_participle_result, plural_noun_result, past_tense_result)
    return majority_vote_result

# get top 10 answers
def rank_and_select_final_answers(*args):
    final_result = {}
    top_n = 10
    for result in args:
        sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        top_n_keys = list(sorted_result.keys())[:top_n]
        for k in top_n_keys:
            if k in final_result:
                final_result[k] += sorted_result[k]
            else:
                final_result[k] = sorted_result[k]

    sorted_final_result = dict(sorted(final_result.items(), key=lambda x:x[1], reverse=True))
    final_top_n_answers = list(sorted_final_result.keys())[:top_n]
    return final_top_n_answers



def print_host_by_form(input_tweet, form):
    #host_forms = ['host', 'hosts', 'hosting', 'hosted']
    words = input_tweet.lower().split()
    if form in words:
        print(input_tweet)

def get_host_rule_present(input_tweet, form):
    if form.lower() != 'host':
        print("Wrong rule \'host\' implemented for form: {}".format(form))
        return None
    cleaned_tweet = clean_tweet(input_tweet)
    end = cleaned_tweet.index('host')
    subtweet = cleaned_tweet[:end]
    words = subtweet.lower().split()
    candidate_answers = []
    # from index of 'host' to the beginning
    for i in range(len(words)-1, -1, -1):
        candidate_answer = ' '.join(words[i:len(words)])
        candidate_answers.append(candidate_answer)
    return candidate_answers

def get_host_rule_present_participle(input_tweet, form):
    if form.lower() != 'hosting':
        print("Wrong rule \'hosting\' implemented for form: {}".format(form))
        return None
    cleaned_tweet = clean_tweet(input_tweet)
    end = cleaned_tweet.index('hosting')
    subtweet = cleaned_tweet[:end]
    words = subtweet.lower().split()
    if len(words) == 0:
        return None
    try:
        if words[len(words)-1].lower() != 'are' and words[len(words)-1] != 'were':
        # print('Unexpected word before hosting: {}'.format(words[len(words)-1]))
        # print(input_tweet)
            return None
    except Exception as e:
        print(cleaned_tweet)
        print(subtweet)
        print('A problem has occured: ', e)

    candidate_answers = []
    # from index of 'are' to the beginning
    for i in range(len(words)-2, -1, -1):
        candidate_answer = ' '.join(words[i:len(words)-1])
        candidate_answers.append(candidate_answer)
    return candidate_answers


def get_host_rule_plural_noun(input_tweet, form):
    if form.lower() != 'hosts':
        print("Wrong rule \'hosts\' implemented for form: {}".format(form))
        return None
    cleaned_tweet = clean_tweet(input_tweet)
    start = cleaned_tweet.index('hosts') + len('hosts')
    subtweet = cleaned_tweet[start:]
    words = subtweet.lower().split()
    candidate_answers = []
    # from index of 'hosts' to the beginning
    for i in range(len(words)):
        candidate_answer = ' '.join(words[0:i+1])
        candidate_answers.append(candidate_answer)
    return candidate_answers

def get_host_rule_past_tense(input_tweet, form):
    if form.lower() != 'hosted':
        print("Wrong rule \'hosted\' implemented for form: {}".format(form))
        return None
    if 'hosted by' in input_tweet:
        return get_host_rule_passive(input_tweet, 'hosted by')

    cleaned_tweet = clean_tweet(input_tweet)
    end = cleaned_tweet.index('hosted')
    subtweet = cleaned_tweet[:end]
    words = subtweet.lower().split()
    candidate_answers = []
    # from index of 'hosts' to the beginning
    for i in range(len(words)-1, -1, -1):
        candidate_answer = ' '.join(words[i:end])
        candidate_answers.append(candidate_answer)
    return candidate_answers

def get_host_rule_passive(input_tweet, form):
    if not 'hosted by' in input_tweet:
        print("Wrong rule \'hosted by\' implemented for form: {}".format(form))

    cleaned_tweet = clean_tweet(input_tweet)
    start = cleaned_tweet.index('hosted by') + len('hosted by')
    subtweet = cleaned_tweet[start:]
    words = subtweet.lower().split()
    candidate_answers = []
    # from index of 'hosts' to the beginning
    for i in range(len(words)):
        candidate_answer = ' '.join(words[0:i+1])
        candidate_answers.append(candidate_answer)
    return candidate_answers


def find_common_phrase(filename=None):
    if filename is None:
        tweets = load_tweets('gg2013.json')
    else:
        tweets = load_tweets('gg2015.json')
    word_count = {}
    word_locations = {}
    host_tweets = []
    for t in tweets:
        if has_host(t['text']):
            words = t['text'].split()
            #words = list(OrderedDict.fromkeys(words))
            for i in range(len(words)-3):
                w = words[i] + ' ' + words[i+1] + ' ' + words[i+2] + ' ' + words[i+3]
                if w in word_count:
                    word_count[w] += 1
                    word_locations[w] += i
                else:
                    word_count[w] = 1
                    word_locations[w] = i
    word_avg_loc = {}
    for w in word_locations.keys():
        word_avg_loc[w] = word_locations[w] / word_count[w]

    word_count_sorted = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))
    top_10_words = list(word_count_sorted.keys())[:10]
    sorted_top_10_words = sorted(top_10_words, key=lambda x: word_avg_loc[x])
    # for w in sorted_top_10_words:
    #     print("{} | count: {} | loc: {}".format(w, word_count[w], word_avg_loc[w]))
    return sorted_top_10_words

def main():
    #print(get_host_rule_present('Joh Doe and Steve Smith host Golden Globe 2022', 'host'))
    #print(get_host_rule_present_participle('Actually excited for the Golden Globes this year because Tine Fey and Amy Poehler are hosting. :D I love them. #SecondCity', 'hosting'))
    #print(get_host_rule_present_participle('Now #GoldenGlobes, when you said Tina &amp; Amy were hosting, it was more of "Hey we need an opening act" thing right.', 'hosting'))
    #print(get_host_rule_plural_noun('RT @goldenglobes: It\'s our hosts Tina Fey and Amy Poehler! #goldenglobes \
        #redcarpet http://t.co/8lqC3ocQ', 'hosts'))
    #print(get_host_rule_past_tense('RT @thetimes: Tonight\'s Golden Globes will be hosted Tina Fey and Amy Poehler. Full nominations here: http://t.co/xEjTpufI http://t.co/NQy5itil', 'hosted'))
    #print(get_host_rule_past_tense('RT @LaurieCrosswell: Every awards show from now on should be hosted by Amy Poelher and Tina Fey. #goldenglobes', 'hosted'))
    # print(remove_nonword_char("Striker@#$__.. as1%23"))
    #print(find_common_phrase())
    #print(find_common_phrase('gg2015.json'))

    tweets = load_tweets('gg2013.json')
    print(get_host_majority_vote(tweets))

    tweets = load_tweets('gg2015.json')
    print(get_host_majority_vote(tweets))


    # for t in tweets:
    #     text = t['text']
    #     if 'hosted' in text:
    #         print(text)
    #         #print('index of \'hosted\' is {}'.format(text.index('were hosting')))
    #         #print_host_by_form(t['text'], 'hosting')
    #         print()


    # host_tweets_length_list = []
    # total_length = 0
    # for t in tweets:
    #     if not host_parser.has_host(t['text']):
    #         continue
    #     host_tweets_length_list.append(len(t['text']))
    #
    # vals, counts = np.unique(host_tweets_length_list, return_counts=True)
    # maxVal = np.max(vals)
    # print(maxVal)
    # bin_ranges = range(0, 200, 10)
    # plt.hist(host_tweets_length_list, bins=bin_ranges, edgecolor='black')
    # plt.show()

if __name__ == '__main__':
    main()



