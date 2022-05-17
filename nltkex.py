import nltk
import enchant
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.corpus import words
import spacy

#eng_dict = enchant.Dict("en_US")
#print(eng_dict.check("Hugh"))
#print("Jahleel" in words.words())


nlp = spacy.load("en_core_web_sm")
doc = nlp('''Scarlett Johanssen from Apple is looking at buying U.K. startup for $1 billion and this is a sample text that contains the name Jahleel Davis Hayes who is one of the developers of this project.
You can also find the surname Murray here.''')
doc2 = nlp('Modern Family and Django Unchained')
print(doc2.ents[0].label_, doc2.ents[1].label_)
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
'''
text = 
# quotes go here
This is a sample text that contains the name Jahleel Davis Hayes who is one of the developers of this project.
You can also find the surname Murray here.
# quotes go here

nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
for nltk_result in nltk_results:
    if type(nltk_result) == Tree:
        name = ''
        for nltk_result_leaf in nltk_result.leaves():
            name += nltk_result_leaf[0] + ' '
        print ('Type: ', nltk_result.label(), 'Name: ', name)
'''