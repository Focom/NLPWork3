import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag, map_tag
import re
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree


def processQuestion(question, classe):

    tokens = nltk.word_tokenize(question)
    tagged = nltk.pos_tag(tokens)
    for i in range(0, len(tagged)):
        if(tagged[0][1] == "WP") or (tagged[0][1] == "WDT") or (tagged[0][1] == "WP$") or (tagged[0][1] == "WRB"):
            WH_word = tagged[0][0]
            WH_BI_word = tagged[0][0] + " " + tagged[1][0]
            WH_Pos = tagged[0][1]
            WH_after = tagged[1][1]
    output = [question, classe, WH_word, WH_BI_word, WH_Pos, WH_after]

    return output


def sentenceChunk(sentence):

    stop = set(stopwords.words('english'))
    sent_tokenize_list = sent_tokenize(sentence)
    listOfTree = []

    for i in sent_tokenize_list:
        sent = nltk.tag.pos_tag(i.split())
        parse_tree = nltk.ne_chunk(sent)
        # print(parse_tree)
        # listOfTree.append(parse_tree)
        # print(parse_tree)
        # parse_tree.remove("Which")
    return parse_tree


def parseIdentity(tree):
    for element in tree:
        text = str(element)
        classe = re.match("\([A-Z]+ (.*)/", text)
        try:
            print(classe.group(1))
        except:
            pass

    return None



def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
            if type(i) == Tree:
                    current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                    named_entity = " ".join(current_chunk)
                    if named_entity not in continuous_chunk:
                            continuous_chunk.append(named_entity)
                            current_chunk = []
            else:
                    continue
            
    return continuous_chunk


def createString(s,namedEntity):
    tokens = nltk.word_tokenize(s)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    for keys in tagged:
        word = keys[0]
        pos = keys[1]
        if (word not in namedEntity):
            if(pos == "CD" or pos == "NNP" or pos == "NN" or pos == "VBG"):
                namedEntity.append(word)
        else:
            pass
    return namedEntity
    

def removeDuplicate(list):
    for element in list:
        test = element.split()
        if (len(test) > 1):
            for key in test:
                list.remove(key)
    try:
        list.remove("Which")
    except:
        pass
    return list


#Retourne un tableau avec les mot a donne a elasticsearch
def wordForQuery(question):
    a= get_continuous_chunks(question)
    b = createString(s,a)
    c = removeDuplicate(b)
    return c

s = "Which French monarch reinstated the divine right of the monarchy to France and was known as `The Sun King' because of the splendour of his reign?"
print(wordForQuery(s))
