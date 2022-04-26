# import class
from classes import *


# create ceremony, award with types and assign the nominees and winner to award with correct type
test_ceremony = Ceremony(1, "Oscar")
type = ['movie', 'actor', 'director']



print("\nCheck for correct type when assign. Should return 9 True:")
for i in range(3):
    temp_award = Award(i+1, "Award " + str(i+1), type[i])
    ceremony_award_bind(temp_award, test_ceremony)
    for j in range(2):
        nominee = Contestant(i*2+j+1, "Contestant " + str(i*2+j+1), type[i])
        print(nominated(temp_award, nominee))
    w = temp_award.nominees[0]
    print(won(temp_award, w))

# print to check if assignment works
print("\n\nCheck nominees and winners for award")
test_ceremony.print()


# check if the nomination assignment check for types
test_nominee = Contestant(7, "Contestant 7", 'actress')
print("\n\nTest nominate with wrong type. Should return False: ")
for a in test_ceremony.awards:
    print(nominated(a, test_nominee))

print("\n\nCheck nominees and winners for award again to see contestant 7 not in any of them")
test_ceremony.print()

# check if the won function check for already nominees
test_nominee_2 = Contestant(8, "Contestant 8", 'movie')
print("\n\nTest win with right type but not in nominee list. Should return False: ")
print(won(test_ceremony.awards[0], test_nominee_2))


#check reassignment for winners
print("\n\nCheck nominees and winners for award again to see contestant 8 not in any of them")
test_ceremony.print()

print("\n\n Change winner for movie award:")
test_nominee_3 = Contestant(9, "Contestant 9", 'movie')
print(nominated(test_ceremony.awards[0], test_nominee_3))
print(won(test_ceremony.awards[0], test_nominee_3))
test_ceremony.print()

print("\n\n Add presenter")
presenter_1 = Presenter(1, "Presenter 1")
present(test_ceremony.awards[0], presenter_1)
test_ceremony.print()

print("\n\n Remove presenter")
remove_presenter(test_ceremony.awards[0], presenter_1)
test_ceremony.print()

print("\n\n Remove winner from award 1")
remove_winner(test_ceremony.awards[0], test_ceremony.awards[0].winner)
test_ceremony.print()


print("\n\n Remove contestant 3 from award 2")
remove_nominee(test_ceremony.awards[1], test_ceremony.awards[1].nominees[0])
test_ceremony.print()

print("\n\nGet all nominees")
nominees = test_ceremony.get_nominees()
for n in nominees:
    print(n.name)

print("\n\nGet all winners")
winners = test_ceremony.get_winners()
for n in winners:
    if n:
        print(n.name)