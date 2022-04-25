def load_tweets():
    with open('data/test_tweets.txt') as tweet_file:
        tweets = set(tweet_file.read().split('\n'))

    return tweets
