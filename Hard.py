import nltk
from nltk.metrics import jaccard_distance
from pprint import pprint
import operator
import Filter_responses
import WordNet
import word2vec_extractor
import os
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# w2v = os.path.join("../hw8_dataset/GoogleNews-vectors-negative300.bin")
# W2vecextractor = word2vec_extractor.Word2vecExtractor(w2v)

def find_hard_answers(features, story, sch):

    sent_story = Filter_responses.get_sentences(story)
    sent_sch = Filter_responses.get_sentences(sch)
    # sent_story = Filter_responses.clean_document(sent_story)
    # sent_sch = Filter_responses.clean_document(sent_sch)
    final = {}

    for qid, feature in features.items():
        if feature['Difficulty'] == 'Hard':
            print(qid)
            print('Type : ', feature['Difficulty'])
            print('Question :', feature['Question'])
            if feature['Type'] == 'Story':
                final[qid] = rank_hard(feature, sent_story)
            else:
                final[qid] = rank_hard(feature, sent_sch)
            print('Answer: ', final[qid])

    # pprint(final)

    return final

def rank_hard(feature, sentences):
    wordnet_candidates = WordNet.filter_answer_wordnetAPI(feature['Question'].split(), sentences, 0)
    word2vec_candidates = sent2vec(feature['pos_keywords'], Filter_responses.clean_document(sentences))
    scores = {}
    for key, value in wordnet_candidates.items():
        scores[key] = (wordnet_candidates[key] + word2vec_candidates[key]) / 2.0
    scores = sorted(scores.items(), key = operator.itemgetter(1))[::-1]
    index = scores[0][0]
    return  Filter_responses.clean_text(' '.join(sentences[index]))

def sent2vec(question, sentences):

    scores = {}

    features_question = word2vec_extractor.W2vecextractor.sent2vec(' '.join(question))
    features_question = features_question.reshape(1,-1)
    for i in range(len(sentences)):
        features_sent = word2vec_extractor.W2vecextractor.sent2vec(' '.join(sentences[i]))

        features_sent = features_sent.reshape(1,-1)
        scores[i] = sklearn.metrics.pairwise.cosine_similarity(features_question,features_sent)
    return (scores)