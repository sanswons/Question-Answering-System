import nltk
from nltk.metrics import jaccard_distance
from pprint import pprint
import operator
import Filter_responses
import WordNet


def find_easy_answers(features, story, sch):

    sent_story = Filter_responses.get_sentences(story)
    sent_sch = Filter_responses.get_sentences(sch)
    final = {}

    for qid, feature in features.items():

        if feature['Difficulty'] == 'Easy':
            print(qid)
            print('Type : ',feature['Difficulty'])
            print('Question : ', feature['Question'])
            if feature['Type'] == 'Story':
                final[qid] = rank_easy( feature, sent_story)
            else:
                final[qid] = rank_easy( feature, sent_sch)
            print('Answer: ', final[qid])

    # pprint(final)
    return final

def rank_easy(feature, sentences):
    jdist_candidates = Filter_responses.filter_by_distance(feature['pos_keywords'], sentences)
    # print(jdist_candidates)
    lcs_candidates = Filter_responses.longest_common_sentence(feature['Question'].split(), sentences)
    # print(lcs_candidates)
    scores = {}
    for key, value in jdist_candidates.items():
        scores[key] = (jdist_candidates[key] + 2.0 * lcs_candidates[key])/3
    scores = sorted(scores.items(), key=operator.itemgetter(1))[::-1]
    # print(scores)
    index = scores[0][0]

    return ' '.join(sentences[index]+sentences[scores[1][0]])

