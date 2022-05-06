
from json_reader import load_tweets
import config 
from get_awards import get_awards, get_best_dressed

class Parser:
    def __init__(self) -> None:
        self.tweets = load_tweets(config.FILE)
        self.file = config.FILE

    def get_host(self):
        pass 
    
    def get_presenters(self):
        pass 

    def get_nominees(self):
        pass

    def get_winner(self):
        pass 

    def get_awards(self):
        award_names = get_awards(self.tweets)
        # for i in range(26):
            # print("Our ", i, "th pick for award_name is ", award_names[i])
        return award_names

    def get_best_dressed(self):
        temp = get_best_dressed(self.tweets)
        # print('\n\nParser thinks best-dressed is ', temp[0][0])
        return temp[0][0]


parser = Parser()
print(parser.get_awards()[:26])
print(parser.get_best_dressed())