import  re, codecs, csv, nltk


def processQuestion(question,classe):


    tokens = nltk.word_tokenize(question)
 
    tagged = nltk.pos_tag(tokens)

    WH_word=""
    WH_BI_word=""
    WH_Pos=""
    WH_after= ""
    for i in range(0,len(tagged)):
        if(tagged[0][1]=="WP") or (tagged[0][1]=="WDT") or (tagged[0][1]=="WP$") or (tagged[0][1]=="WRB"):
            WH_word=tagged[0][0]
            WH_BI_word=tagged[0][0]+" "+tagged[1][0]
            WH_Pos=tagged[0][1]
            WH_after= tagged[1][1]
        if(tagged[0][0]=="Which"):
            WH_word=tagged[0][0]
            WH_BI_word=tagged[0][0]+" "+tagged[1][0]
            WH_Pos="WDT"
            WH_after= tagged[1][1]
    output= [question, classe, WH_word, WH_BI_word, WH_Pos, WH_after]
    
    return output

def createListe(getTrainData):

    result=[]

    questions = codecs.open(getTrainData, "r", 'utf-8')
    questionsRead = questions.read()
    questions.close()
    listeQuestion=[]
    listeWHpos=[]
    listeBi=[]
    listeClasse=[]
    listebiPos=[]
    listeUni=[]
    listeOfQuestion = re.findall("(.*)\n", questionsRead)

    for i in range(0,len(listeOfQuestion)):
        text = listeOfQuestion[i]
        classe = re.match("^([A-Z])", text)
        question = re.match("^[A-Z] (.*)", text)
        format=processQuestion(question.group(1),classe.group(1))
        listeQuestion.append(format[0])
        listeWHpos.append(format[4])
        listeBi.append(format[3])
        listeClasse.append(format[1])
        listebiPos.append(format[5])
        listeUni.append(format[2])
        
    result.append(listeClasse)
    result.append(listeQuestion)
    result.append(listeBi)
    result.append(listebiPos)
    result.append(listeUni)
    result.append(listeWHpos)

    return result

def constructCsv(getTrainData):
    tab=createListe(getTrainData)
    csv_out = open('DataTrain/mycsv.csv', 'w')
    mywriter = csv.writer(csv_out,delimiter='|',lineterminator='\r\n')
    rows = zip(tab[1],tab[0],tab[4],tab[2],tab[5],tab[3])
    mywriter.writerows(rows)
    csv_out.close()

constructCsv("DataTrain/question-train.txt")
