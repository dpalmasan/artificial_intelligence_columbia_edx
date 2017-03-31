from os import listdir
from collections import Counter
import string
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

train_path = "aclImdb/train/" # use terminal to ls files under this directory
test_path = "imdb_te.csv" # test data for grade evaluation

# Store stopwords in a list
with open("stopwords.en.txt", "r") as f:
    stopwords = f.read()

stopwords = stopwords.split("\n")


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    '''Implement this module to extract
    and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

    with open(name, "w") as f:
        f.write("row_number,text,polarity\n")
        row_number = 0
        for text in listdir(inpath + "pos"):
            with open(inpath + "pos/" + text, "r") as s:
                f.write(str(row_number) + ",\"" + s.read().replace("\"", "\"\"") + "\",1" + "\n")
                #bag_of_words = s.read()
                #bag_of_words = bag_of_words.replace("<br />", " ")
                #replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
                #bag_of_words = bag_of_words.lower().translate(replace_punctuation)
                #bag_of_words = bag_of_words.split()
                #bag_of_words = [word for word in bag_of_words if word not in stopwords]
                #f.write(str(row_number) + "," + ' '.join(bag_of_words) + ",1\n")
                
            row_number += 1

        for text in listdir(inpath + "neg"):
            with open(inpath + "neg/" + text, "r") as s:
                f.write(str(row_number) + ",\"" + s.read().replace("\"", "\"\"") + "\",0" + "\n")
                #bag_of_words = s.read()
                #bag_of_words = bag_of_words.replace("<br />", " ")
                #replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
                #bag_of_words = bag_of_words.lower().translate(replace_punctuation)
                #bag_of_words = bag_of_words.split()
                #bag_of_words = [word for word in bag_of_words if word not in stopwords]
                #f.write(str(row_number) + "," + ' '.join(bag_of_words) + ",0\n")

            row_number += 1

def preprocess_string(s):
    """
    Removes punctuation and stopwords from a string, it also lowercases the string and
    returns the modified string
    """
    bag_of_words = s
    bag_of_words = bag_of_words.replace("<br />", " ")
    replace_punctuation = string.maketrans(string.punctuation, ' '*len(string.punctuation))
    bag_of_words = bag_of_words.lower().translate(replace_punctuation)
    bag_of_words = bag_of_words.split()
    bag_of_words = [word for word in bag_of_words if word not in stopwords]
    bag_of_words = ' '.join(bag_of_words)
    return bag_of_words

def term_document_matrix(infile="imdb_tr.csv", representation="unigram", tf_idf=False):
    dataset = pd.read_csv(infile)

    # Preprocess text
    dataset['text'] = dataset['text'].apply(preprocess_string)

    if tf_idf:
        if representation == "bigram":
            cv = TfidfVectorizer(stop_words=stopwords, ngram_range=(1, 2))
        else:
            cv = TfidfVectorizer(stop_words=stopwords)
        tdm =  cv.fit_transform(dataset['text'])
        return (cv, tdm, dataset['polarity'])
    else:
        if representation == "bigram":
            cv = CountVectorizer(stop_words=stopwords, ngram_range=(1, 2))
        else:
            cv = CountVectorizer(stop_words=stopwords)
        tdm =  cv.fit_transform(dataset['text'])
        return (cv, tdm, dataset['polarity'])

if __name__ == "__main__":
    '''train a SGD classifier using unigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''

    '''train a SGD classifier using bigram representation,
    predict sentiments on imdb_te.csv, and write output to
    unigram.output.txt'''

    '''train a SGD classifier using unigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''

    '''train a SGD classifier using bigram representation
    with tf-idf, predict sentiments on imdb_te.csv, and write 
    output to unigram.output.txt'''

    imdb_data_preprocess(train_path)

    ##############################
    # Unigram representation     #
    ##############################
    (cv, tdm, polarity) = term_document_matrix()
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(tdm, polarity)

    # Loading and predicting polarity on test set
    testset = pd.read_csv(test_path)
    testset['text'] = testset['text'].apply(preprocess_string)

    # Lazy fix of error, I don't know what happened with encoding
    cv = CountVectorizer(vocabulary=cv.vocabulary_, decode_error='ignore')
    tdm_te = cv.fit_transform(testset['text'])
    predictions = clf.predict(tdm_te)

    # Save predictions to output file
    with open("unigram.output.txt", "w") as f:
        for pred in predictions:
            f.write(str(pred) + "\n")

    ##############################
    # Bi-gram representation     #
    ##############################
    
    (cv, tdmbi, polarity) = term_document_matrix(representation="bigram")

    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(tdmbi, polarity)

    cv = CountVectorizer(vocabulary=cv.vocabulary_, decode_error='ignore', ngram_range=(1, 2))
    tdmbi_te = cv.fit_transform(testset['text'])
    predictions = clf.predict(tdmbi_te)

    # Save predictions to output file (now in a functional programming fashion xD)
    with open("bigram.output.txt", "w") as f:
        f.write('\n'.join(map(str, predictions)))

    ##############################
    # tf-idf scheme              #
    ##############################
    (cv, tdm, polarity) = term_document_matrix(tf_idf=True)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(tdm, polarity)

    # Loading and predicting polarity on test set
    testset = pd.read_csv(test_path)
    testset['text'] = testset['text'].apply(preprocess_string)

    # Lazy fix of error, I don't know what happened with encoding
    cv = TfidfVectorizer(vocabulary=cv.vocabulary_, decode_error='ignore')
    tdm_te = cv.fit_transform(testset['text'])
    predictions = clf.predict(tdm_te)

    # Save predictions to output file
    with open("unigramtfidf.output.txt", "w") as f:
        for pred in predictions:
            f.write(str(pred) + "\n")

    (cv, tdmbi, polarity) = term_document_matrix(representation="bigram", tf_idf=True)

    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(tdmbi, polarity)

    cv = TfidfVectorizer(vocabulary=cv.vocabulary_, decode_error='ignore', ngram_range=(1, 2))
    tdmbi_te = cv.fit_transform(testset['text'])
    predictions = clf.predict(tdmbi_te)

    # Save predictions to output file (now in a functional programming fashion xD)
    with open("bigramtfidf.output.txt", "w") as f:
        f.write('\n'.join(map(str, predictions)))

    
