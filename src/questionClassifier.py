import os

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from scipy.sparse import csr_matrix
import pandas, time, spacy



def pre_process(data):
    return pandas.get_dummies(data)


def transform_data_matrix(X_train, X_predict):
    X_train_columns = list(X_train.columns)
    X_predict_columns = list(X_predict.columns)

    X_trans_columns = list(set(X_train_columns + X_predict_columns))

    trans_data_train = {}

    for col in X_trans_columns:
        if col not in X_train:
            trans_data_train[col] = [0 for i in range(len(X_train.index))]
        else:
            trans_data_train[col] = list(X_train[col])

    XT_train = pandas.DataFrame(trans_data_train)
    XT_train = csr_matrix(XT_train)

    trans_data_predict = {}

    for col in X_trans_columns:
        if col not in X_predict:
            trans_data_predict[col] = 0
        else:
            trans_data_predict[col] = list(X_predict[col])  # KeyError

    XT_predict = pandas.DataFrame(trans_data_predict)
    XT_predict = csr_matrix(XT_predict)
    # get_data_info(XT_predict)

    return XT_train, XT_predict



def support_vector_machine(X_train, y, X_predict):
    lin_clf = LinearSVC()
    lin_clf.fit(X_train, y)
    prediction = lin_clf.predict(X_predict)
    return prediction



def get_question_predict_data(en_doc):
    sent_list = list(en_doc.sents)
    sent = sent_list[0]
    wh_bi_gram = []
    root_token = ""
    wh_pos = ""
    wh_nbor_pos = ""
    wh_word = ""
    for token in sent:
        if token.tag_ == "WDT" or token.tag_ == "WP" or token.tag_ == "WP$" or token.tag_ == "WRB":
            wh_pos = token.tag_
            wh_word = token.text
            wh_bi_gram.append(token.text)
            wh_bi_gram.append(str(en_doc[token.i + 1]))
            wh_nbor_pos = en_doc[token.i + 1].tag_

    qdata_frame = [{'WH': wh_word, 'WH-POS': wh_pos, 'WH-NBOR-POS': wh_nbor_pos}]

    dta = pandas.DataFrame(qdata_frame)
    return dta

def classify_question(en_doc):
    dta = pandas.read_csv(os.path.join('DataTrain/mycsv.csv'), sep='|')

    y = dta.pop('Class')

    dta.pop('#Question')
    dta.pop('WH-Bigram')
    print(dta)
    X_train = pre_process(dta)

    question_data = get_question_predict_data(en_doc)
    X_predict = pre_process(question_data)

    X_train, X_predict = transform_data_matrix(X_train, X_predict)

    return str(support_vector_machine(X_train, y, X_predict))


en_nlp = spacy.load("en")
dta = pandas.read_csv('DataTrain/mycsv.csv', sep='|')
y = dta.pop('Class')
dta.pop('#Question')
dta.pop('WH-Bigram')
X_train = pre_process(dta)

question = 'Which country, with and area greater than the combined areas of France, Germany and Italy, was part of the vice-royalty of New Spain, established in 1535 until it achieved independence in 1821?'
en_doc = en_nlp(u'' + question)
question_data = get_question_predict_data(en_doc)
X_predict = pre_process(question_data)

X_train, X_predict = transform_data_matrix(X_train, X_predict)
print(support_vector_machine(X_train, y, X_predict))

