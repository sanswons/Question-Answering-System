import argparse
import nltk
from pprint import pprint
import operator
from nltk.parse import DependencyGraph
from nltk.stem import PorterStemmer
import pickle
import sys
from nltk.tree import Tree
import re
import Answer_type_detection
import Entity_detection
import read_write
import Filter_responses
import Easy
import Medium
import Hard


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Assignment 3')
    parser.add_argument( dest="list_of_stories")
    args = parser.parse_args()
    list_of_stories = args.list_of_stories

    fh = open(list_of_stories, 'r')
    stories = fh.readlines()
    fh.close()
    for story in stories:
        print(story)
        story = re.sub('\n','', story)
        sch_file = story + ".sch"
        story_file = story + '.story'
        questions_file = story + '.questions'
        answers_file = story + ".answers"
        story_par_file = story + '.story.par'
        sch_par_file = story + '.sch.par'

        final = []
        answers = {}

        features = Answer_type_detection.find_answer_type(questions_file)
        features = Entity_detection.find_keywords(features)
        answers = Easy.find_easy_answers(features, read_write.read_file(story_file), read_write.read_file(sch_file))
        answers.update(Medium.find_medium_answers(features, read_write.read_file(story_file), read_write.read_file(sch_file)))
        answers.update(Hard.find_hard_answers(features, read_write.read_file(story_file), read_write.read_file(sch_file)))

        final = (sorted(answers.items(), key=lambda item: (int(item[0].split('-')[2]), item[1])))

        # pprint(final)

        filename = 'Woonna_answers.txt'
        with open(filename, 'a') as f:
            for answer in final:
                f.write('QuestionID: ')
                f.write(answer[0])
                f.write('\n')
                f.write('Answer: ')
                f.write(answer[1])
                f.write('\n\n')



