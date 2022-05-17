from get_nominees import *
def main():
    tweets = load_tweets(r'gg2013.json\gg2013.json')
    award_names = ['best supporting actor', 'best supporting actress', 'best director', 'best motion picture',
                   'best actor', 'best actress', 'best screen play', 'best animated feature film', 'best television series']
    i = 1
    for name in award_names:
        global global_award_pick
        global_award_pick = name
        award = Award(i, name, 'actor')
        i = i+1
        nominees_dict = find_nominees(tweets, award)
        print(name + " Winners: ")
        print('\n')
        nominees_dict = {key: val for key, val in nominees_dict.items() if val >= 30}
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
