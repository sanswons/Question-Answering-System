import nltk
from nltk.metrics import jaccard_distance
from pprint import pprint
import operator
import Filter_responses
import WordNet

def find_medium_answers(features, story, sch):

    sent_story = Filter_responses.get_sentences(story)
    sent_sch = Filter_responses.get_sentences(sch)

    final = {}

    for qid, feature in features.items():

        if feature['Difficulty'] == 'Medium':
            print(qid)
            print('Difficulty :', feature['Difficulty'])
            print('Question :', feature['Question'])
            if feature['Type'] == 'Story':
                final[qid] = rank_medium(feature, sent_story)
            else:
                final[qid] = rank_medium(feature, sent_sch)
            print('Answer: ', final[qid])

    # pprint(final)

    return final

def rank_medium(feature, sentences):
    wordnet_candidates = WordNet.filter_answer_wordnetAPI(feature['Question'].split(), sentences, 0)
    # print(wordnet_candidates)
    dist_candidates = Filter_responses.filter_by_distance(feature['Question'].split(), sentences)
    # print(dist_candidates)
    scores = {}
    for key, value in wordnet_candidates.items():
        scores[key] = (2*wordnet_candidates[key] + dist_candidates[key]) / 3.0

    scores = sorted(scores.items(), key = operator.itemgetter(1))[::-1]
    # print(scores)
    index = scores[0][0]
    return  ' '.join(sentences[index]+sentences[scores[1][0]])

