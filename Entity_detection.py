import nltk
from pprint import pprint
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


def find_keywords(features):
    stopwords = set(nltk.corpus.stopwords.words("english"))
    important_tags = ['VBN', 'NNS', 'VBP', 'NNP', 'NN', 'VBD','JJ', 'JJR', 'JJS']
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    for qid, feature in features.items():
        tagged_tokens = nltk.pos_tag(nltk.word_tokenize(feature['Question']))
        tokens = [t[0].lower() for t in tagged_tokens if t[1] in important_tags]
        tokens.extend([lemmatizer.lemmatize(t[0].lower()) for t in tagged_tokens if t[1] in important_tags])
        # tokens.extend([stemmer.stem(t[0].lower()) for t in tagged_tokens if t[1] in important_tags])

        tokens = list(set(tokens))
        feature['pos_keywords'] = tokens

    for qid, feature in features.items():
        synonyms = []
        for token in feature['pos_keywords']:
            for synonym in wn.synsets(token):
                synonyms.extend([str(lemma.name()) for lemma in synonym.lemmas()])
        feature['wordnet_synonyms'] = synonyms

    return features

