import os
import numpy as np
from collections import Counter
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.metrics import confusion_matrix
from nltk.corpus import stopwords



def make_Dictionary(train_dir):

    stop_word = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'the', 'to', 'of', 'in', 'that', 'an', 'is', 'with', 'he', 'his', 'on', 'as', 'her', 'was', 'but',
                 'The', 'by', 'him', 'for', 'she', 'from', 'it', 'are', 'be', 'they', 'He', 'who', 'at', 'not', 'into',
                 'after', 'and', 'their','has', 'out', 'them', 'then', 'where', 'up', 'They', 'which', 'off', 'about', 'can', 'have'
                 , 'when', 'all', 'while', 'so', 'As', 'before', 'one', 'had', 'only', 'get','In', 'tells', 'go', 'She', 'When', 'away', 'just', 'also', 'how', 'or', 'another',
                 'its', 'gets', 'will', 'not', 'such', 'most', 'other', 'few', 'down', 'over', 'goes', 'back', 'two', 'After', 'would', 'way', 'take', 'three', 'At', 'It', 'behind']

    movies = [os.path.join(train_dir, f) for f in os.listdir(train_dir)]
    all_words = []
    for movie in movies:
        with open(movie) as m:
            for i, line in enumerate(m):
                words = line.split()
                all_words += words

    dictionary = Counter(all_words)
    dick = dictionary.copy()
    list_to_remove = dick.keys()

    for item in list_to_remove:
        if not item.isalpha():
            del dictionary[item]
        elif len(item) == 1:
            del dictionary[item]
        elif item in stop_word:
            del dictionary[item]

    dictionary = dictionary.most_common(3000)

    return dictionary

def extract_features(movie_dir):
    files = [os.path.join(movie_dir,fi) for fi in os.listdir(movie_dir)]
    features_matrix = np.zeros((len(files), 3000))
    docID = 0;
    for fil in files:
      with open(fil) as fi:
        for i,line in enumerate(fi):
            words = line.split()
            for word in words:
              wordID = 0
              for i,d in enumerate(dictionary):
                if d[0] == word:
                  wordID = i
                  features_matrix[docID,wordID] = words.count(word)
        docID = docID + 1
    return features_matrix


# Create a dictionary of words with its frequency

train_dir = 'train-starwars'
dictionary = make_Dictionary(train_dir)

print(dictionary)    #use to see counter of words

# Prepare feature vectors per training mail and its labels

train_labels = np.zeros(190)
train_labels[95:190] = 1
train_matrix = extract_features(train_dir)

# Training Naive bayes classifier

model1 = MultinomialNB()
model1.fit(train_matrix, train_labels)

# Test the unseen text file for Spoilers
test_dir = 'test-starwars'
test_matrix = extract_features(test_dir)
test_labels = np.zeros(20)
test_labels[10:20] = 1
result1 = model1.predict(test_matrix)
print(confusion_matrix(test_labels, result1))