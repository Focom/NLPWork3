import json

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def getNameFromQuery(query):
    data = es.search(index="wikipedia", doc_type="text", body=query)
    # result = []
    # for i in range(0, len(data["hits"]["hits"])):
    #     result.append(data["hits"]["hits"][i]["_source"]["Name"])
    return data


def askQuestion(question):
    classe = "Person"
    words = question.split()
    words.append(classe)
    question = {
  "query": {
    "match": {
      "body": {
        "query":'Sun + King',
        "minimum_should_match": "100%"
      }
    }
  }
}

    return getNameFromQuery(question)['hits']['hits'][0]

def query(sentence):
    output=" ".join(sentence)
    return output


print(query(['Which French', 'France', 'Sun King', 'monarch', 'divine', 'right', 'monarchy', 'splendour', 'reign']))
print(askQuestion("Which French monarch reinstated the divine right of the monarchy to France and was known as `The Sun King' because of the splendour of his reign?"))


