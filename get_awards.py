
import re
from json_reader import load_tweets
from award_names import award_names_w_best as anwb


def clean_up(potential_awards):
    """
    Input:
        - Takes a list of list of awards which contain the name, and the number of times it was mentioned
        - [[Best Drama, 45], [Best Picture, 57]] etc 
    Output:
        - Returns the list with updated counts. This tries to take longer sentences such as 
          "best drama at the golden globes goes to _____" and still use them in the ocunt for "best drama"

          Current bug: 
          Double counts since it runs both lists, since proportional for all of them not sure it matters to much. 

          Elimites from things like best comedy series to best comedy... which gets the spirit of the award but doesnt finish it.
          Basically always shortens, which isn't always what the award names want.  Another example is "Best actor in motion picture -> best actor" 
    """
    for n in potential_awards:
        for name in potential_awards:
            if n[0] in name[0]:
                print("ADDED COUNT TO", n[0], "PROGRAM THINKS ", n[0], " IN ", name[0])
                n[1] += 1
            elif name[0] in n[0]:
                name[1] +=1 
                print("ADDED COUNT TO", name[0], "PROGRAM THINKS ", name[0], " IN ", n[0])
    return potential_awards

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

def get_awards(filename=None):
    """
    Input: 
        - Optionally takes a filename from the data folder, defaults to Golden Globes 2013 if not given one. 
    Output:
        - Outputs a list of award names from the award show represented by the filename. 
    """
    tweets = load_tweets(filename=filename)
    num_tweets = 0
    potential_names = {}
    for tweet in tweets:
        num_tweets += 1 
        if 'best' in tweet['text']: # It is significantly faster to check this here then just let regex do it all. 
            test = re.findall("best [a-zA-Z\s]+",tweet['text'],flags=re.IGNORECASE)
            for item in test:
                item = item.strip().lower()
                potential_names[item] = potential_names.get(item,0) + 1

    high_potential_names = []
    people_really_liked = [] 
    for potential_name in potential_names.keys():
        LOWER_BOUND = 0.00011451933372651638 #Found by 20/#2013 tweets 
        UPPER_BOUND = 0.00028629833431629095 #Found by 50/#2013 tweets 
        if potential_names[potential_name] > (LOWER_BOUND * num_tweets) and potential_names[potential_name] <= (UPPER_BOUND * num_tweets) :
            high_potential_names.append([potential_name,potential_names[potential_name]])
        elif potential_names[potential_name] > (UPPER_BOUND * num_tweets):
            people_really_liked.append([potential_name,potential_names[potential_name]])

    high_potential_names = clean_up(high_potential_names)
    high_potential_names.sort(key= lambda x: x[1])


    people_really_liked = clean_up(people_really_liked)
    people_really_liked.sort(key= lambda x: x[1])
    return high_potential_names, people_really_liked

def get_best_dressed(filename=None):
    """
    Input: 
        - Optionally takes a filename from the data folder, defaults to Golden Globes 2013 if not given one. 
    Output:
        - Outputs the twitter voted best-dressed. 
    """
    tweets = load_tweets(filename=filename)
    num_tweets = 0
    potential_names = {}
    just_names = {}
    for tweet in tweets:
        num_tweets += 1 
        if 'best' in tweet['text']: # It is significantly faster to check this here then just let regex do it all. 
            test = re.findall("best dressed [a-zA-Z\s]+",tweet['text'],flags=re.IGNORECASE)
            test2 = re.findall("[a-zA-Z\s]+ best dressed",tweet['text'],flags=re.IGNORECASE)
            for item in test:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
            for item in test2:
                temp = re.findall('([A-Z][a-z]+(?=\s[A-Z])(?:\s[A-Z][a-z]+)+)',item)
                for i in temp:
                    just_names[i] = just_names.get(i,0) + 1
                potential_names[item] = potential_names.get(item,0) + 1
    
    names = []
    statements = []
    for i in just_names.keys():
        names.append([i,just_names[i]])
    for i in potential_names.keys():
        statements.append([i,potential_names[i]])
    
    statements.sort(key = lambda x: x[1])
    statements.reverse()

    names.sort(key= lambda x: x[1])
    names.reverse()

    return names,statements 




#high_potential_names, people_really_liked = get_awards()
temp,temp1 = get_best_dressed('gg2015.json')
for i in range(10):
    print(temp[i])
print("TEST")
for i in range(10):
    print(temp1[i])

print("TEST")
print(temp[0][0])
print(temp1[0][0])







#print_awards(high_potential_names)
#print_awards(people_really_liked)


"""
-Best dressed or other sentiment votes as voted by twitter might be fairly easy to generate while doing this as well. 
-We might want to tag tweets that we get award names from, because they likely also have information about the nominees or winners. 
"""