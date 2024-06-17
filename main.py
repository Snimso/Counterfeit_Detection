#===================Importing dependencies=================================#
import string
import numpy as np
import pandas as pd

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

pd.options.display.memory_usage = 'deep'

final_score = 0

dfmain = pd.read_csv('final_dataset.csv', encoding='latin1') #encoding because of special chars

intinput = int(input("Enter Input Entry field (0-7651)")) #For now using this, ideally our interface should have something jisme cust inp daalsake#


#======================Parameter A: Verification Check=====================#
if (dfmain['verified'].iloc[intinput])==0:
    final_score+=25

#======================Parameter B: NLP Analysis============================#


#======================Parameter C: Classifier=============================#
nltk.download('stopwords')

df = pd.read_csv('Classifier_dataset.csv', usecols = ["text_", "label_num"], dtype={"label_num" : "int8"})


df['text_'] = df['text_'].apply(lambda x: x.replace('\r\n', ' ')) 


#stemming 
stemmer = PorterStemmer()
corpus = []

stopwords_set = set(stopwords.words('english'))

for i in range(len(df)):
    text = df['text_'].iloc[i].lower()
    text = text.translate(str.maketrans('','',string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    text = ' '.join(text)
    corpus.append(text)


#vectorize 
vectorizer = TfidfVectorizer()
x = vectorizer.fit_transform(corpus).toarray()
y = df['label_num']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state=42)

clf = MultinomialNB()
clf.fit(x_train, y_train)
print(f"Model accuracy: {accuracy_score(y_test, clf.predict(x_test))}")




#email_to_classify = df.text.values[10]
def finrev():
    inputint = int(input("Enter an index from the database (0-9999):"))
    if (inputint<0 or inputint>9999):
        print("INVALID")
        return
    else:
        email_to_classify = df.review.values[inputint]
        email_text = email_to_classify.lower().translate(str.maketrans('', '', string.punctuation)).split()
        email_text = [stemmer.stem(word) for word in email_text if word not in stopwords_set]
        email_text = ' '.join(email_text)

        email_corpus = [email_text]

        x_email = vectorizer.transform(email_corpus)

        finval = clf.predict(x_email)
        if finval[0] == 0:
            print("Your email is not spam")
        if finval[0] == 1:
            print("Your email is spam")





