def write_file(dictionary):
    for key, value in dictionary.items():
        print('QuestionID : ' + key)
        print('Answer : ' + value)
        print('\n')


# Read the file from disk
def read_file(filename):
    fh = open(filename, 'r')
    content = fh.read()
    fh.close()
    return content

def read_responses(filename ,answers):
    fh = open(filename, 'r')
    fw = open('test.answers', 'wb')
    content = fh.readlines()

    try:
        for line in content:
            print(line)
            print(answers[line.strip()])
    except:
        print('')






