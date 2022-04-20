
"""
Current Status:
    - Basically none of it works, been a little bit since I scraped and google is a bit annoying due to the size of the 
      webpage, but beginning to get re-aquainted. 
"""


# Basic interface:
# Not sure if useful or necessary really, 
def take_input():
    """
    This function takes nothing as input and returns a list containing the cermony name and year that 
    the user would like to learn about. 

    Input: 
        - None

    Output: 
        - [ceremony_name, ceremony_year] 
    """
    ceremony_name = input('What is the name of the award-show you would like information about?\n')
    next_question = "What year would yuu like information about " + ceremony_name + " for?\n"
    ceremony_year = input(next_question)
    #print("The ceremony we are gathering data for is", ceremony_name,  "in", ceremony_year, "\n")
    return [ceremony_name, ceremony_year]



# Also not sure if this is really what we should be working on first after looking over slides... 
# He says we should start by giving the parser the categories and then trying to find who wins, this is more 
# The second part of trying to find the categories given the ceremony name. 

# Regardless its one of the only things we can do right now so good to at least get started. 

from bs4 import BeautifulSoup
import requests
from parsel import Selector

#data_in = take_input()
#ceremony_name = data_in[0]
#ceremony_year = data_in[1]

ceremony_name = "Golden Globes"
ceremony_year = "2019"

# def get_category_names(ceremony_name, ceremony_year): #[Beautiful Soup]
    # """
    # Given a ceremony name and year, this function returns a list of award categories for that ceremony. 
    # 
    # Input: 
        # - Ceremony_name (string)
        # - Ceremony_year (string representation of a 4 digit number)
# 
    # Output: 
        # - Categories [List of strings] 
    # """
    # url = "http://www.google.com/search?q=\"" + ceremony_name + " Award Categories " + ceremony_year + "\""
    # page = requests.get(url)
# 
    # soup = BeautifulSoup(page.content, "html.parser")
    # test = soup.find("g-scrolling-carousel")
    # print(test)
    # job_elements = soup.find_all('a', jsname = "I4kCu")
    # print(job_elements)
# 
    # categories = []
    # for result in awards:
        # title = soup.find("something") FIXX 
# 
    #   if title is not None:
        #   categories.append(title)
# 
    # print(categories)
    # return(categories)
# 

def get_category_names(ceremony_name, ceremony_year): #[Parsel selector version]
    """
    Given a ceremony name and year, this function returns a list of award categories for that ceremony. 
    
    Input: 
        - Ceremony_name (string)
        - Ceremony_year (string representation of a 4 digit number)

    Output: 
        - Categories [List of strings] 
    """
    url = "http://www.google.com/search?q=\"" + ceremony_name + " Award Categories " + ceremony_year + "\""
    page = requests.get(url)
    selector = Selector(text=page.text)

    carousel_name = selector.css(".LXqMce").get()
    print(carousel_name)
    awards = selector.css("script::text").getall()

    categories = []
    for result in awards:
        #print(result)
        pass
        #title = result.css(".JjtOHd::text").get()

    #   if title is not None:
        #   categories.append(title)

    print(categories)
    return(categories)


get_category_names(ceremony_name, ceremony_year)