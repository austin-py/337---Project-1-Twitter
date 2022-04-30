
import re
from json_reader import load_tweets
from award_names import award_names_w_best as anwb

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
            #print(potential_name, " was repeated ", potential_names[potential_name], " times\n")
        if potential_names[potential_name] > (UPPER_BOUND * num_tweets):
            people_really_liked.append([potential_name,potential_names[potential_name]])

    high_potential_names.sort(key= lambda x: x[1])
    for pn in high_potential_names:
        print(pn[0], " was repeated ", pn[1], " times\n")

    print("\n\n\n")
    people_really_liked.sort(key= lambda x: x[1])
    for pn in people_really_liked:
        print(pn[0], " was repeated ", pn[1], " times\n")

    print("There are ", len(high_potential_names), "high potential names.\n")
    print("There are ", len(people_really_liked), "things that people really liked.\n")
    print("Processed ", num_tweets, " tweets \n"  )
    return high_potential_names, people_really_liked

high_potential_names, people_really_liked = get_awards()


for n in high_potential_names:
    for name in high_potential_names:
        if n[0] in name[0]:
            n[1] += 1
        elif name[0] in n[0]:
            name[1] +=1 

high_potential_names.sort(key = lambda x: x[1])
for name in high_potential_names:
    print(name[0], "............", name[1])


# high_potential_hits = 0
# people_really_liked_hits = 0 
# for award in anwb:
    # for name in high_potential_names:
        # if award.lower() in name[0] or award.lower().strip() == name[0]:
            # print(name, award.lower())
            # high_potential_hits += 1 
    # for name in people_really_liked:
        # if award.lower() in name[0]:
            # people_really_liked_hits += 1
# 
# print("\n\n\nThere were ", high_potential_hits, " high-potential hits\n")
# print("There were ", people_really_liked_hits, " people really liked hits\n")
"""
-Best dressed or other sentiment votes as voted by twitter might be fairly easy to generate while doing this as well. 
-We might want to tag tweets that we get award names from, because they likely also have information about the nominees or winners. 
"""