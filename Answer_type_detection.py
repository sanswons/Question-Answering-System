import pickle
import nltk


def find_answer_type(questions_file):
    # question content
    d = {}
    with open(questions_file, 'r') as f:
        for line in f.readlines():
            line = line.rstrip()
            pair = line.split(':')
            if pair[0] == 'QuestionID':
                key = pair[1].strip()
                d[key] = {}

            if pair[0] == 'Difficulty':
                d[key][pair[0]] = pair[1].strip()

            if pair[0] == 'Question':
                d[key][pair[0]] = pair[1].strip()

            if pair[0] == 'Type':
                try:
                    d[key][pair[0]] = pair[1].strip().split('|')[1]
                except:
                    d[key][pair[0]] = pair[1].strip()

    # print(d)
                    # Answer_type

    for key, feature in d.items():
        wh_word = nltk.word_tokenize(feature['Question'])[0]
        ans_type = 'ans_type'
        if wh_word == 'Who':
            d[key][ans_type] = 'person'
        if wh_word == 'Where':
            d[key][ans_type] = 'location'
        if wh_word == 'What':
            d[key][ans_type] = 'thing'
        if wh_word == 'When':
            d[key][ans_type] = 'time'
        if wh_word == 'Why':
            d[key][ans_type] = 'reason'
        d[key]['wh_word'] = wh_word
    '''

    # add ROOT word dependency
    wh_dep_words = pickle.load(open(root_pickle_file, 'rb'))
    for key, value in wh_dep_words.items():
        d[key]['wh_dep_word'] = value
    '''
    return d