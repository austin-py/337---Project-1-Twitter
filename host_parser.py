from json_reader import load_tweets
from collections import OrderedDict

def has_host(input_tweet):
    host_forms = ['host', 'hosts', 'hosting']
    words = input_tweet.split()

    for w in words:
        for h in host_forms:
            if w.lower() == h:
                return True

def find_common_phrase():
    tweets = load_tweets('gg2013.json')
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
    for w in sorted_top_10_words:
        print("{} | count: {} | loc: {}".format(w, word_count[w], word_avg_loc[w]))

def main():
    find_common_phrase()

if __name__ == '__main__':
    main()



