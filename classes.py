# Ceremony class
class Ceremony:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.awards = []

    def print(self):
        print("------" + self.name + "------")
        for e in self.awards:
            res = e.name + ":\n   Presenters: "
            for n in e.presenters:
                res = res + n.name + ", "
            res = res + "\n   Nominees: "
            for n in e.nominees:
                res = res + n.name + ", "

            res = res + "\n   Winner: "
            if e.winner:
                res = res + e.winner.name
            print(res)

    def get_nominees(self):
        res = set()
        for a in self.awards:
            for n in a.nominees:
                res.add(n)
        return res
    
    def get_winners(self):
        res = set()
        for a in self.awards:
            res.add(a.winner)
        return res

# Award class
class Award:
    def __init__(self, ID, name, type):
        self.ID = ID
        self.ceremony = None
        self.name = name
        self.presenters = []
        self.nominees = []
        self.winner = None
        self.type = type

# Contestant class. Using variabel type for checking instead of inheritance for now
class Contestant:
    def __init__(self, ID, name, type):
        self.ID = ID
        self.name = name
        self.type = type
        self.award_nominated = []
        self.award_won = []

class Presenter:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.award_present = []

# bind award with ceremony
def ceremony_award_bind(award, ceremony):
    award.ceremony = ceremony
    ceremony.awards.append(award)

# nominate a contestant for an award. Return True if success (when type matches), else false
def nominated(award, contestant):
    if award.type == contestant.type:
        award.nominees.append(contestant)
        contestant.award_nominated.append(award)
        return True
    else:
        return False

# a contestant won for an award. Return True if success (when the contestant is already nominated), else false
def won(award, contestant):
    if contestant in award.nominees:
        award.winner = contestant
        contestant.award_won.append(award)
        return True
    else:
        return False

# add a presenter for an award
def present(award, presenter):
    award.presenters.append(presenter)
    presenter.award_present.append(award)

def remove_nominee(award, contestant):
    if contestant in award.nominees:
        award.nominees.remove(contestant)
        contestant.award_nominated.remove(award)
    if contestant == award.winner:
        award.winner = None
        contestant.award_won.remove(award)

def remove_winner(award, winner):
    if winner == award.winner:
        award.winner = None
        winner.award_won.remove(award)

def remove_presenter(award, presenter):
    if presenter in award.presenters:
        award.presenters.remove(presenter)
        presenter.award_present.remove(award)





