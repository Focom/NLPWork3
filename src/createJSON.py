import math 
import csv, json, sys
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag, map_tag

csv.field_size_limit(sys.maxsize)

def getDataPath(Path):
    _id,count=0,0
    allData = []
    

    with open(Path,'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')

        for row in tsvin:
            _id+=1
            allData.append({"index": {"_index": "wikipedia", "_type": "text", "_id": str(_id)}})
            name = row[1]
            text = row[4]
            body = constructSentenceWithList(text)       
            allData.append({"title":name,"body":body})
            
            if(_id % 5000==0):
                count+=1
                name = "JSON"+str(count)+".json"
                createJson(name, allData)
                allData = []
            
            
            print(_id)
            
        count+=1
        name = "JSON"+str(count)+".json"
        createJson(name, allData)

def createJson(nameOfJSON, dataArray):

    with open(nameOfJSON, 'w') as f:
        for i in range(0,len(dataArray)):
            f.write(json.dumps(dataArray[i], ensure_ascii=False))
            f.write("\n")

  
def constructSentenceWithList(listOfSentence):

    body=''
    for indice in range(0,len(listOfSentence)):                
        body += str(listOfSentence[indice])
    return body

getDataPath("JsonFiles/Data.tsv")