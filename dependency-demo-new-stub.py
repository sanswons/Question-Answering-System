#!/usr/bin/env python
'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import re, sys, nltk, operator
from nltk.parse import DependencyGraph
from nltk.stem.wordnet import WordNetLemmatizer

# Read the lines of an individual dependency parse
def read_dep(fh):
    dep_lines = []
    for line in fh:
        line = line.strip()
        if len(line) == 0:
            return update_inconsistent_tags("\n".join(dep_lines))
        elif re.match(r"^QuestionId:\s+(.*)$", line):
            # You would want to get the question id here and store it with the parse
            continue
        dep_lines.append(line)
    if len(dep_lines) > 0:
        return update_inconsistent_tags("\n".join(dep_lines))
    else:
        return None

# Note: the dependency tags return by Stanford Parser are slightly different than
# what NLTK expects. We tried to change all of them, but in case we missed any, this
# method should correct them for you.
def update_inconsistent_tags(old):
    return old.replace("root", "ROOT")

# Read the dependency parses from a file
def read_dep_parses(depfile):
    fh = open(depfile, 'r')

    # list to store the results
    graphs = []
    
    # Read the lines containing the first parse.
    dep = read_dep(fh)

    # While there are more lines:
    # 1) create the DependencyGraph
    # 2) add it to our list
    # 3) try again until we're done
    while dep is not None:
        graph = DependencyGraph(dep)
        graphs.append(graph)

        dep = read_dep(fh)
    fh.close()

    return graphs

# Return the word of the root node
def find_root_word(graph):
    for node in graph.nodes.values():
        if node['rel'] == 'ROOT':
            return node["word"]
    return None

# find the node with similar word
def find_node(word, graph):
    for node in graph.nodes.values():
        if 'word' in node and node["word"] == word:
            return node
    return None

def get_dependents(node, graph):
    results = []
    for item in node["deps"]:
        address = node["deps"][item][0]
        dep = graph.nodes[address]
        results.append(dep)
        results += get_dependents(dep, graph)
    return results

def pretty_question(qgraph):
    question = []
    for q in qgraph.nodes.values():
        if 'word' in q and q['word'] is not None:
            question.append(q['word'])
    return " ".join(question)

def find_answer(qgraph, sgraphs):
    qword = find_root_word(qgraph)
    # look for answer in the sgraphs, return the first match
    for sgraph in sgraphs:
        snode = find_node(qword, sgraph)
        if snode is None or 'address' not in snode:
            continue
        for node in sgraph.nodes.values():
            #print("node in nodelist:", node)
            #print("Our relation is:", node['rel'], ", and word is:", node['word'])
            #print("Our node is:", node)
            if node is None or 'head' not in node:
                continue
            if node['head'] == snode["address"]:
                if node['rel'] == "nmod":
                    deps = get_dependents(node, sgraph)
                    deps.append(node)
                    deps = sorted(deps, key=operator.itemgetter("address"))
                    return " ".join(dep["word"] for dep in deps)

if __name__ == '__main__':
    text_file = "blogs-02.story"
    dep_file = "blogs-02.story.dep"
    q_file = "fables-02.questions.dep"

    # Read the dependency graphs into a list
    sgraphs = read_dep_parses(dep_file)
    for sgraph in sgraphs:
        for node in sgraph.nodes.values():
            print(node)
    
    qgraphs = read_dep_parses(q_file)

    # TODO: You may need to include different rules in find_answer() for
    # different types of questions. For example, the rule here is good for
    # answering "Where was the crow sitting?", but not necessarily the others.
    # You would have to figure this out like in the chunking demo
    for qgraph in qgraphs:
        print("Question:", pretty_question(qgraph), "?")
        answer = find_answer(qgraph, sgraphs)
        print("Answer:", answer)
        print()

    # example of how to use a lemmatizer
    print("\nLemma:")
    lmtzr = WordNetLemmatizer()
    for node in sgraphs[1].nodes.values():
        tag = node["tag"]
        word = node["word"]
        if word is not None:
            if tag.startswith("V"):
                print(lmtzr.lemmatize(word, 'v'))
            else:
                print(lmtzr.lemmatize(word, 'n'))
    print()
