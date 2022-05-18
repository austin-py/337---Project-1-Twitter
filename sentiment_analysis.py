import ssl

from textblob import TextBlob
from json_reader import *
import numpy as np
import time
import nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')

def sort_dict(dictionary):
    """
    Input:
        - Take a dictionary
    Output:
        - A sorted dictionary by value
    """
    sorted_keys = sorted(dictionary, key=dictionary.get, reverse = True)
    sorted_dict = {}
    for k in sorted_keys:
        sorted_dict[k] = dictionary[k]
    return sorted_dict

def get_polarity_all_tweets(tweets):
    result = []
    for tweet in tweets:
        text = tweet['text']
        blob = TextBlob(text)
        avg = 0
        for sentence in blob.sentences:
            avg = avg + sentence.sentiment.polarity
        avg = avg/(len(blob.sentences))
        result.append(avg)
    return result


def relevant_data(tweets, people):
    relevant_tweets = []
    tweet_set = set()
    for tweet in tweets:
        t = tweet['text'].lower()
        contain_name = any([(name.lower() in t) for name in people])
        if not contain_name:
            continue
        words = t.split()
        prefix = ''
        if len(words) < 4:
            prefix = ' '.join(words[0:4])
        if len(words) < 8:
            prefix = ' '.join(words[0:7])
        if len(words) > 12:
            prefix = ' '.join(words[0:10])
        if prefix not in tweet_set:
            relevant_tweets.append(tweet)
            tweet_set.add(prefix)

    return relevant_tweets

def get_all_hosts_winners_presenters(file_name):
    data = load_tweets(file_name)
    presenters = set()
    winners = set()
    hosts = data['hosts']
    award_data = data['award_data']
    for k in award_data.keys():
        for p in award_data[k]['presenters']:
            presenters.add(p)
        winners.add(p)

    presenters = list(presenters)
    winners = list(winners)
    people = hosts + presenters + winners
    return list(people)

def get_sentiment_information_person(person, tweets_polarity, tweets):
    sum = 0
    negative = 0
    neutral = 0
    positive = 0
    count  = 0
    for i in range(len(tweets)):
        text = tweets[i]['text']
        if person in text.lower():
            sum = sum + tweets_polarity[i]
            if tweets_polarity[i] < 0:
                negative = negative + 1
            elif tweets_polarity[i] == 0:
                neutral = neutral + 1
            else:
                positive = positive + 1

            count = count + 1

    if count > 0:
        return sum/count, negative/count, neutral/count, positive/count
    else:
        return 0, 0, 0, 0


def get_sentiment_information(tweets_file_name, people_file_name):
    tweets = load_tweets(tweets_file_name)
    people = get_all_hosts_winners_presenters(people_file_name)
    tweets = relevant_data(tweets, people)
    tweets_polarity = get_polarity_all_tweets(tweets)

    print(np.mean(tweets_polarity))

    avg_polarity_people = {}
    all_polarity_people = {}
    polarity_result = {}

    for person in people:
        avg_polarity, neg_percent, neu_percent, pos_percent =  get_sentiment_information_person(person.lower(), tweets_polarity, tweets)
        avg_polarity_people[person] = avg_polarity
        all_polarity_people[person] = [avg_polarity, neg_percent, neu_percent, pos_percent]

    avg_polarity_people = sort_dict(avg_polarity_people)
    for k in avg_polarity_people.keys():
        polarity_result[k] = all_polarity_people[k]
        #print('{}: Average sentiment polarity - {:.2f}, negative tweets percentage - {:.2f}, neutral tweets percentage - {:.2f}, positive tweets percentage - {:.2f}'.format(k, all_polarity_people[k][0], all_polarity_people[k][1], all_polarity_people[k][2], all_polarity_people[k][3]))

    return polarity_result, np.mean(tweets_polarity)

def main():
    start_time = time.time()
    polarity_2013, mean_polarity_2013 = get_sentiment_information('gg2013_clean.json', 'gg2013_answers.json')
    polarity_2015, mean_polarity_2015 = get_sentiment_information('gg2015_clean.json', 'gg2015_answers.json')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()