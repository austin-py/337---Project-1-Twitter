import re
from json_reader import load_tweets
import config
from award_names import award_names_w_best as anwb

FILE = config.FILE
AWARD_SHOW_NAME = config.AWARD_SHOW_NAME

""" 
Fair warning, this file is a bit of a mess right now as i've been testing a bunch of different stuff... 

Will clean it up later, but in the meantime ask if you have any questions. 
"""

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

def get_awards(tweets):
    """
    Input: 
        - Optionally takes a filename from the data folder, defaults to Golden Globes 2013 if not given one. 

    Output:
        - Outputs a list of award names from the award show represented by the filename. 
    """
    num_tweets = 0
    potential_names = {}
    high_potential = {}
    for tweet in tweets:
        original = tweet
        tweet = tweet['text'].strip().lower()
        tweet = tweet.split (" ")
        num_tweets += 1 
        if 'best' in tweet: 
            recording = False
            curr = '' 
            stop_words = ["-","at","for","goes"] #TODO add more 
            end_charachters = [":",".","!"]
            for i in range(len(tweet)):
                if tweet[i] == 'best':
                    recording = True
                    curr = tweet[i]
                elif recording:
                    if tweet[i] != "":
                        if tweet[i] in stop_words or tweet[i][-1] in end_charachters:
                            high_potential[curr] = high_potential.get(curr,0) + 1
                    curr = curr + " " + tweet[i]
                    potential_names[curr] = potential_names.get(curr,0) + 1
               
               
               

            # This was my old way of identifying. Did pretty well but always got the shortest version 
            # the most, so never got description such as "in a tv movie, series, or miniseries" for supporting actress. 
            test = re.findall("best [a-zA-Z\s]+",original['text'],flags=re.IGNORECASE)
            for item in test:
                item = item.strip().lower()
                potential_names[item] = potential_names.get(item,0) + 1

    # This is also alligned with the old way, just did probability basically. 
    high_potential_names = []
    people_really_liked = [] 
    for potential_name in potential_names.keys():
        LOWER_BOUND = 0.00011451933372651638 #Found by 20/#2013 tweets 
        UPPER_BOUND = 0.00028629833431629095 #Found by 50/#2013 tweets 
        if potential_names[potential_name] > (LOWER_BOUND * num_tweets) and potential_names[potential_name] <= (UPPER_BOUND * num_tweets) :
            high_potential_names.append([potential_name,potential_names[potential_name]])
        elif potential_names[potential_name] > (UPPER_BOUND * num_tweets):
            people_really_liked.append([potential_name,potential_names[potential_name]])

    # This is for the newer version where we find all possible strings after best, and priortize the ones with stop words. 
    really_high_potential = [] 
    for potential in high_potential.keys():
        really_high_potential.append([potential,high_potential[potential]])
    really_high_potential.sort(key = lambda x: x[1],reverse=True)
    #print_awards(really_high_potential)
    just_names = [i[0] for i in really_high_potential]
    


    high_potential_names.sort(key= lambda x: x[1])
    people_really_liked.sort(key= lambda x: x[1])
    #print_awards(high_potential_names)
    #print_awards(people_really_liked)

    # just_names = [i[0] for i in high_potential_names]
    # just_names2 = [i[0] for i in people_really_liked]
    # just_names = just_names + just_names2

    return just_names

def get_best_dressed(tweets):
    """
    Input: 
        - Optionally takes a filename from the data folder, defaults to Golden Globes 2013 if not given one.

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
                    if (i == AWARD_SHOW_NAME):
                        continue
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
            for item in ending:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    if (i == AWARD_SHOW_NAME):
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

    return names



# 
# award_names = get_awards(FILE)
# for i in range(26):
    # print("Our ", i, "th pick for award_name is ", award_names[i])
# 
# temp = get_best_dressed(FILE)
# 
# print('\n\nParser thinks best-dressed is ', temp[0][0])
# 