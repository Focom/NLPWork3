import  pandas, glob

from sklearn.naive_bayes import MultinomialNB as mod
from sklearn.ensemble import RandomForestClassifier as mod2
from sklearn.feature_extraction.text import CountVectorizer

#Choix du classifieurn i=1 NaivesBayes sinon RandomForest
#################################Partie 0
def choiceClassifier(i):

    if(i==1):
        classifier=mod
    else:
        classifier=mod2

    return classifier

#################################Partie 1
#Construction du fichier csv s'il n'est pas encore présent dans le répértoire
def construCsv():

    a = glob.glob("*.csv")
    if (len(a)==0):
        exo2.constructCsv()


#################################Partie 2
#Construction du modèle prédictive en fonction du choiceClassifier() et prédiction sur un certain nombre de ligne résévées au test
def constructModel(cc,j):

    classifieur=choiceClassifier(j)
    result=[]
    # Transformation de mon document csv en dataframe grâce à panda
    df_train= pandas.read_csv('DataTrain/mycsv.csv')
    final=pandas.DataFrame(data=df_train)
    #Y sera mon vecteur de classe et x le vecteur de question associé
    vecteurClasseTrain=final["Classe"][:cc]
    
    # print(vecteurClasseTrain)
    vecteurQuestion=final["Question"]
    classifier=classifieur()
    targetsClasse=vecteurClasseTrain[:cc].values
    vecteurClasseTest=final["Classe"][cc:].values
    # print(final["Classe"][cc:])
    count_vectorizer = CountVectorizer()
    counts = count_vectorizer.fit_transform(vecteurQuestion[:cc].values)
    classifier.fit(counts, targetsClasse)

    examples = vecteurQuestion[cc:]
    example_counts = count_vectorizer.transform(examples)
    predictions = classifier.predict(example_counts)

    result.append(predictions)
    result.append(vecteurClasseTest)
    result.append(examples)
    result.append(j)
    result.append(final["Classe"].values)

    return result

#################################Partie 3

#Ici on construit un dictionnaire qui nous stock les différence entre les vraies prédictions et les fausses pour chaque classe
def construcTableRP(predictions,trueclass):

    result = {}

    for i in range(0,len(predictions)):

        if(predictions[i]==trueclass[i]):

            result[str(i)]=({
                "class":predictions[i],
                "bool": True
            })

        else:
            result[str(i)]=({
                "class": predictions[i],
                "bool": False
            })

    return result
#################################Partie 4

def truePositive(classe,tableRP):

    data = tableRP
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"])) :
            result+=1
    return result

def falsePositive(classe,tableRP):

    data = tableRP
    result=0
    for i in range(0,len(data)):

        if ((classe == data[str(i)]["class"]) & (data[str(i)]["bool"]==False)) :
            result+=1
    return result

def trueNegative(classeOption,Model):

    data = Model[1]
    data.sort()
    result=0
    for classe in data:

        if(classe!=classeOption):
            result+=1
    return result

def falseNegative(classeOption,Model):

    data = Model[1]
    data.sort()
    result=0
    for classe in data:

        if(classe==classeOption):
            result+=1
    return result

def precision(classe,Model,tableRP):
    try:
        return truePositive(classe,tableRP)/(truePositive(classe,tableRP)+falsePositive(classe,tableRP))
    except ZeroDivisionError:
        return 0

def recall(classe,Model,tableRP):
    return truePositive(classe,tableRP)/(falseNegative(classe,Model))
#################################Partie 5

def general(Model, tableRP,classe):
    if(Model[3]==1):
        cl="Naives Bayes"
    else:
        cl="Random Forest"

    print("Pour la classe ",classe," et un modèle ",cl," la précision est de:")
    print(precision(classe,Model,tableRP))
    return precision(classe,Model,tableRP)
    #print("Pour un rappel de:")
    #print(recall(classe,Model,tableRP))

def result(list,model,tableRP):
    liste=[]
    if (model[3]==1):
        print("Pour Naives Bayes:")
    else:
        print("Pour Random Forest")

    for key in list:

        
        liste.append(general(model,tableRP,key))
    return liste

    print("-------------------")

def countElement(model,liste):
    countListe=[]
    letters=model[4]
    for element in liste:
        countListe.append((letters==element).sum())
    return countListe


Model1=constructModel(900, 1)
liste=["P","L","O","T","R","M","C","A","D","F","W","B","X"]

letters = Model1[4]
#Model2=constructModel(1200, 2)
tableRp1=construcTableRP(Model1[0],Model1[1])
#tableRp2=construcTableRP(Model2[0],Model2[1])
newY=result(liste,Model1,tableRp1)
#result(liste,Model2,tableRp2)


import matplotlib
matplotlib.use('TkAgg')
from pylab import *


x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13])
y = np.array(newY)
y2 = np.array(countElement(Model1,liste))
my_xticks = ["P","L","O","T","R","M","C","A","D","F","W","B","X"]



fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.xticks(x, my_xticks)
ax1.set_ylabel('y1', color='b')
plt.plot(x,y,'b-o', label="Précision")
plt.legend()


ax2 = ax1.twinx()

ax2.set_ylabel('y2', color='r')


plt.plot(x,y2,'r-o', label="Nombre d'élément dans la classe")
plt.legend()


plt.show()
show()




def constructModel(question,csvPath):

    dataFrame = createDataFrame(csvPath)

    df_train =  {'Classe': None ,'Question': question }
    frame = pandas.DataFrame(df_train, index=[0])
    
    df3=dataFrame.append(frame,ignore_index=True)
    sizeOfCsv=len(dataFrame)

    vecteurClass = dataFrame["Classe"].values
    vecteurQuestion = df3["Question"].values
    
    model = mod2()
    count_vectorizer = CountVectorizer()

    counts = count_vectorizer.fit_transform(vecteurQuestion)
    model.fit(counts[:sizeOfCsv].toarray(),vecteurClass[:sizeOfCsv])
   
    predicted = model.predict(counts[sizeOfCsv])

    print(predicted)
  
def createDataFrame(csvPath):
    df_train = pandas.read_csv(csvPath)
    dataFrame = pandas.DataFrame(data=df_train)
    return dataFrame

constructModel("who is the an walk on the moon ?","DataTrain/mycsv.csv")