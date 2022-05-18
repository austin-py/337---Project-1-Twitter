
import re
from unicodedata import name
from json_reader import load_tweets
import config
from award_names import award_names_w_best as anwb

FILE = config.FILE
AWARD_SHOW_NAME = config.AWARD_SHOW_NAME


def print_awards(awards):
    """
    Input:
        - Takes a list of list of awards which contain the name, and the number of times it was mentioned
        - [[Best Drama, 45], [Best Picture, 57]] etc 

    Output:
        - Nothing is returned, but the awards are pritned to stdout. 
    """
    for name in awards:
        print(name[0], "............", name[1])

def clean_awards(awards):
    for award in awards.keys():
        if len(award.split('-')) > 2:
            temp = award.split('-')
            temp = "-".join(temp[:2])
            temp = temp.strip()
            if temp in awards.keys():
                awards[temp] += awards[award]
                awards[award] = 0 
        elif len(award.split('-')) == 2:
            temp = award.split('-')
            if len(temp[1].strip().split(" ")) == 2 or '"' in temp[1]:
                temp = temp[0]
                temp = temp.strip()
                if temp in awards.keys():
                    awards[temp] += awards[award]
                    awards[award] = 0 
    
    return awards

def return_awards(tweets):
    """
    Input: 
        - Takes a dictionary of tweets from json reader

    Output:
        - Outputs a list of award names from the award show represented by the filename. 
    """
    num_tweets = 0
    high_potential = {}
    for tweet in tweets:
        tweet = tweet['text'].strip().lower()
        tweet = tweet.split (" ")
        num_tweets += 1 
        if 'best' in tweet: 
            recording = False
            curr = '' 
            stop_words = ["-","at","for","goes"] 
            end_charachters = [":",".","!"]
            for i in range(len(tweet)):
                if tweet[i] == 'best':
                    recording = True
                    curr = tweet[i]
                elif recording:
                    if tweet[i] != "" and curr != 'best':
                        if tweet[i] in stop_words: 
                            curr = curr.strip()
                            high_potential[curr] = high_potential.get(curr,0) + 1
                        elif tweet[i][-1] in end_charachters:
                            curr = curr + " " + tweet[i][:-1]
                            curr = curr.strip()
                            high_potential[curr] = high_potential.get(curr,0) + 1
                            recording = False
                    curr = curr + " " + tweet[i]
                            
    high_potential = clean_awards(high_potential)
    high_potential = clean_awards(high_potential)
    # This is for the newer version where we find all possible strings after best, and priortize the ones with stop words. 
    really_high_potential = [] 
    for potential in high_potential.keys():
        really_high_potential.append([potential,high_potential[potential]])
    really_high_potential.sort(key = lambda x: x[1],reverse=True)
    #print_awards(really_high_potential)
    just_names = [i[0] for i in really_high_potential]
    

    return just_names[:26]

def get_best_dressed(tweets):
    """
    Input: 
        - Takes a dictionary of tweets from json reader

    Output:
        - Outputs the twitter voted best-dressed. 
    """ 
    num_tweets = 0
    potential_names = {}
    just_names = {}
    for tweet in tweets:
        num_tweets += 1 
        if 'best' in tweet['text']: 
            beginning = re.findall("best dressed [a-zA-Z\s]+",tweet['text'],flags=re.IGNORECASE)
            ending = re.findall("[a-zA-Z\s]+ best dressed",tweet['text'],flags=re.IGNORECASE)
            for item in beginning:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    if (i == AWARD_SHOW_NAME or len(i.split(" ")) > 2):
                        continue
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
            for item in ending:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    if (i == AWARD_SHOW_NAME or len(i.split(" ")) > 2):
                        continue
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
    
    names = []
    statements = []
    for i in just_names.keys():
        names.append([i,just_names[i]])
    for i in potential_names.keys():
        statements.append([i,potential_names[i]])
    
    statements.sort(key = lambda x: x[1],reverse = True)
    names.sort(key= lambda x: x[1],reverse= True)

    return names[0][0]

def get_worst_dressed(tweets):
    """
    Input: 
        - Takes a dictionary of tweets from json reader

    Output:
        - Outputs the twitter voted worst-dressed. 
    """ 
    num_tweets = 0
    potential_names = {}
    just_names = {}
    for tweet in tweets:
        num_tweets += 1 
        if 'worst' in tweet['text']: 
            beginning = re.findall("worst dressed [a-zA-Z\s]+",tweet['text'],flags=re.IGNORECASE)
            ending = re.findall("[a-zA-Z\s]+ worst dressed",tweet['text'],flags=re.IGNORECASE)
            for item in beginning:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    if (i == AWARD_SHOW_NAME or len(i.split(" ")) > 2):
                        continue
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
            for item in ending:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    if (i == AWARD_SHOW_NAME or len(i.split(" ")) > 2):
                        continue
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
    
    names = []
    statements = []
    for i in just_names.keys():
        names.append([i,just_names[i]])
    for i in potential_names.keys():
        statements.append([i,potential_names[i]])
    
    statements.sort(key = lambda x: x[1],reverse = True)
    # for i in statements:
        # print(i)
    names.sort(key= lambda x: x[1],reverse= True)

    return names[0][0]


    
    
    

    

    

if __name__ == '__main__':
    tweets = load_tweets(FILE)
    award_names = return_awards(tweets)
    for i in range(26):
        print("Our ", i, "th pick for award_name is ", award_names[i], ".",sep="")
    temp = get_best_dressed(tweets)
    print('\n\nParser thinks best-dressed is ', temp[0][0], ".")
    temp = get_worst_dressed(tweets)
    print('\n\nParser thinks worst-dressed is ', temp[0][0], ".")