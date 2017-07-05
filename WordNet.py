from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
import sys, os
import re
import operator
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
import pickle
from pprint import pprint
from nltk.corpus import stopwords
import Filter_responses

brown_ic = wordnet_ic.ic('ic-brown.dat')


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'

    if tag.startswith('V'):
        return 'v'

    if tag.startswith('J'):
        return 'a'

    if tag.startswith('R'):
        return 'r'

    return None


def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None


def lemmatize(phrase):
    porter_stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    phrase = word_tokenize(phrase)
    for i in range(len(phrase)):
        phrase[i] = lemmatizer.lemmatize(phrase[i])
    return phrase


def sentence_similarity(question, sentence):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    # question = lemmatize(question)
    question = pos_tag(question)

    # sentence = lemmatize(sentence)
    sentence = pos_tag(sentence)

    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in question]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence]

    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]

    score, count = 0.0, 0

    # For each word in the first sentence
    for i in range(len(synsets1)):
        # Get the similarity value of the most similar word in the other sentence
        scores = []
        try:
            scores.extend( max([synsets1[i].wup_similarity(ss, brown_ic) for ss in synsets2]),
                           max([synsets1[i].lin_similarity(ss, brown_ic) for ss in synsets2]),
                           max([synsets1[i].res_similarity(ss, brown_ic) for ss in synsets2]),
                           max([synsets1[i].jcn_similarity(ss, brown_ic) for ss in synsets2]))
            best_score = sum(scores)/len(scores)
        except:
            best_score = None
        # Check that the similarity could have been computed

        if best_score is not None:
            score += best_score
            count += 1

    # Average the values
    try:
        score /= count
    except:
        score = 0

    return score


def filter_answer_wordnetAPI(question, sentences, threshold):
    answers = {}
    for i in range(len(sentences)):
        similarity = (sentence_similarity(question, sentences[i]) + sentence_similarity(sentences[i], question))/2
        if similarity > threshold:
            answers[i] = similarity
        else:
            answers[i] = 0

    # print(answers)
    return answers
