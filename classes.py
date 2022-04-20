# Ceremony class
class Ceremony:
    def __init__(self, ID, name):
        self.ID = ID
        self.name = name
        self.awards = []

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



