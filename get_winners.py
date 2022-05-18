from get_nominees import *
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
            if j < 1:
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