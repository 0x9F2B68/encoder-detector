import cchardet as chardet
import sys
import os
import codecs


def count_statistic(file_full_path, lines_num = 1000):
    """
    Function will determine encoding line by line and count how many times 
    each encoding was found.
    Output: list with founded encodings sorted by popularity.
    """
    with open(file_full_path, "rb") as f:
        encodings_result = [] # 'statistics' 
        encoding_holder = []
        for line in f:
            if lines_num < 1:
                break
            lines_num -= 1
            # list [ [encoding , lines] , ... ]
            line_encoding = chardet.detect(line)
            # print("line_encoding: ",line_encoding)
            if type(line_encoding['confidence']) != "NoneType" or line_encoding['confidence'] > 0.5:
                if line_encoding['encoding'] in encoding_holder:
                    for i in encodings_result: # check is there encoding in statistics 
                        if i[0] == line_encoding['encoding']: # if there is
                            i[1] += 1
                else: 
                    encodings_result.append([line_encoding['encoding'], 1]) # adding new encoding is statistics
                    encoding_holder.append(line_encoding['encoding'])
    # sort list by second value in inner list    
    sorted_encodings_result = sorted(encodings_result, key=lambda x: x[1], reverse=True) 
    result = []
    for i in sorted_encodings_result:
        result.append(i[0])
    # print("ENC RES:", encodings_result)
    # print("SORTED ENC RES:", sorted_encodings_result)
    # print("RESULT LIST: ", result)
    return result

check = False
if len(sys.argv) == 2:
    file_full_path = sys.argv[1]
elif len(sys.argv) == 3:
        check = True if sys.argv[2] != 0 else False
        file_full_path = sys.argv[1]
else:
    file_full_path = input("Enter full path to file: ")

while not os.path.exists(file_full_path):
    file_full_path = input("Enter proper full file path!\n")

"""
Global determine
"""
work = True
byte_num = int(-1) # number of bytes for .read()
with open(file_full_path, "rb") as f:
    while work:
        try:
            if byte_num == -1: # to make code work a bit faster
                msg = f.read(byte_num)
            else:
                msg = f.read(byte_num) + f.readline()
            # print("delecious")
            work = False

        except MemoryError:
            if byte_num == -1:
                byte_num = 10000000000 # 1.000.000.000
            else:
                byte_num = int(byte_num / 2)
            # print("doesn't fit, trying", byte_num)

    result = chardet.detect(msg)
    # print("Proposal: ", result['encoding'])
    # print("Confidence: ", result['confidence'])

    if check:
        statistic = count_statistic(file_full_path, 50000)
        # print(statistic)
        if result['confidence'] < 0.55:
            result['encoding'] = statistic[0]

print(result['encoding'])
