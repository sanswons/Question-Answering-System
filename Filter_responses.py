import nltk
from nltk.metrics import jaccard_distance
from pprint import pprint
import operator
from nltk.corpus import stopwords
import re
import WordNet
from nltk.stem import PorterStemmer


def get_sentences(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    # tokens = [t.lower() for sentence in sentences if t[1] in important_tags]
    return sentences


def clean_document(sentences):
    clean_text = []
    important_tags = ['VBN', 'NNS', 'VBP', 'NNP', 'NN', 'VBD', 'JJ', 'JJR', 'JJS']
    for sentence in sentences:
        tagged_tokens = nltk.pos_tag(sentence)
        tokens = [t[0].lower() for t in tagged_tokens if t[1] in important_tags]
        tokens = ' '.join(tokens)
        tokens = WordNet.lemmatize(tokens)
        clean_text.append(tokens)
    return clean_text


def longest_common_substring(a, b):
    lengths = [[0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            else:
                lengths[i + 1][j + 1] = max(lengths[i + 1][j], lengths[i][j + 1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x - 1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y - 1]:
            y -= 1
        else:
            assert a[x - 1] == b[y - 1]
            result = a[x - 1] + result
            x -= 1
            y -= 1
    return result


def longest_common_sentence(question_keywords, sentences):
    candidates = {}
    # print('lcs',question_keywords, sentences)
    for i in range(len(sentences)):
        # print(set(question_keywords).union(set(sentences[i])))
        denominator = len(list(set(question_keywords).union(set(sentences[i]))))
        candidates[i] = len(longest_common_substring(question_keywords, sentences[i]))/denominator
    return candidates


def filter_by_distance(question_keywords, sentences):
    sentences = clean_document(sentences)
    question_keywords = WordNet.lemmatize(' '.join(question_keywords))
    candidates = {}
    for i in range(len(sentences)):
        sentence = sentences[i]
        d = 1 - jaccard_distance(set(sentence), set(question_keywords))
        candidates[i] = d
    return candidates

def clean_text(text):
    stop = stopwords.words()
    # text = re.sub('[^A-Za-z0-9]', ' ', text)
    return ' '.join([token for token in text.split() if token not in stop])