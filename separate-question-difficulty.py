#!/usr/bin/env python

import zipfile, argparse, os, sys, re
from collections import defaultdict

###############################################################################
## Utility Functions ##########################################################
###############################################################################


# returns a dictionary where the question numbers are the key
# and its items are another dict of difficulty, question, type, and answer
# e.g. story_dict = {'fables-01-1': {'Difficulty': x, 'Question': y, 'Type':}, 'fables-01-2': {...}, ...}
def getQA(filename):
    content = open(filename, 'rU', encoding='latin1').read()
    question_dict = {}
    for m in re.finditer(r"QuestionID:\s*(?P<id>.*)\n(Question:\s*(?P<ques>.*)\n){0,1}(Answer:\s*(?P<answ>.*)\n){0,1}(Difficulty:\s*(?P<diff>.*)\nType:\s*(?P<type>.*)){0,1}\n*", content):
        qid = m.group("id")
        question_dict[qid] = {}
        question_dict[qid]['Question'] = m.group("ques")
        question_dict[qid]['Answer'] = m.group("answ")
        question_dict[qid]['Difficulty'] = m.group("diff")
        question_dict[qid]['Type'] = m.group("type")
    return question_dict

def write_answer_files(dataset_dict, filename):
    if len(dataset_dict) <= 0:
        return
    file = open(filename, "w")

    keylist = sorted(dataset_dict.keys())
    for key in keylist:
        value = dataset_dict[key]
        file.write('QuestionID: ' + key + '\n')
        file.write('Answer: ' + value['Answer']+ '\n')
        file.write('\n')
    file.close()

def write_solution_files(dataset_dict, filename):
    if len(dataset_dict) <= 0:
        return
    file = open(filename, "w")

    keylist = sorted(dataset_dict.keys())
    for key in keylist:
        value = dataset_dict[key]
        file.write('QuestionID: ' + key + '\n')
        file.write('Question: ' + value['Question'] + '\n')
        file.write('Answer: ' + value['Answer']+ '\n')
        file.write('Difficulty: ' + value['Difficulty']+ '\n')
        file.write('Type: ' + value['Type']+ '\n')
        file.write('\n')
    file.close()



###############################################################################
## Program Entry Point ########################################################
###############################################################################
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assignment 6-8')
    parser.add_argument('-f', dest="fname_list", default="hw8_test_process_stories.txt",  help='File that contant a list of fname in order.')
    parser.add_argument('-p', dest="predict_answer_fname", default="Woonna_answers.txt",  help='File name that contant the predict answers in order.')
    parser.add_argument('-s', dest="standard_answer_fname", default="hw8_test.answers",  help='File name that contant the actual answers in order.')

    args = parser.parse_args()

    fname_list = args.fname_list
    predict_answer_fname = args.predict_answer_fname
    standard_answers_fname = args.standard_answer_fname

    predict_answers_dict = getQA(predict_answer_fname)
    standard_answers_dict = getQA(standard_answers_fname)
    
    easy_questions = defaultdict()
    medium_questions = defaultdict()
    hard_questions = defaultdict()

    easy_solutions = defaultdict()
    medium_solutions = defaultdict()
    hard_solutions = defaultdict()

    with open(fname_list) as input_file:
        for line in input_file:
            fname = line.strip('\n')
            if fname.strip() != "":
                questions = getQA("{}.questions".format(fname))
                
                for j in range(0, len(questions)):
                    qid = j+1
                    qname = "{0}-{1}".format(fname, qid)
                    if qname in questions:
                        diff = questions[qname]["Difficulty"].lower()
                        if diff.startswith('eas'):
                            easy_questions[qname] = predict_answers_dict[qname]
                            easy_solutions[qname] = standard_answers_dict[qname]
                        elif diff.startswith('med'):
                            medium_questions[qname] = predict_answers_dict[qname]
                            medium_solutions[qname] = standard_answers_dict[qname]
                        elif diff.startswith('har'):
                            hard_questions[qname] = predict_answers_dict[qname]
                            hard_solutions[qname] = standard_answers_dict[qname]

    write_answer_files(easy_questions, "predict_easy.answers")
    write_answer_files(medium_questions, "predict_med.answers")
    write_answer_files(hard_questions, "predict_hard.answers")

    write_solution_files(easy_solutions, "solution_easy.answers")
    write_solution_files(medium_solutions, "solution_med.answers")
    write_solution_files(hard_solutions, "solution_hard.answers")
