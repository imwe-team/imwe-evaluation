from __future__ import print_function, division

from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib.backends.backend_pdf import PdfPages

def readCsvFile(filepath):
    f = codecs.open(filepath, "r", "utf-16")
    data = dict()

    #read first line
    fstLine = f.readline()

    keyList = list()
    for i in fstLine.split(','):
        key = str(i.replace('"', ''))
        keyList.append(key)
        data[key] = list()
    print(keyList)

    # #read lines
    # lines = f.readlines()
    # for line in lines:
    #     print(line)
    #     fields = line.split(',')
    #     for i,field in enumerate(fields):
    #         print(keyList[i], field)
    #     break

def readCsvFile2(filename):
    data = pd.read_csv(filename, encoding="utf-16")
    return data

def writeSortedQuestionsToTxt(data, questions, outfolder, groups="group"):
    for question in questions:
        writeSortedQuestionToTxt(data, question, outfolder, groups)

def writeSortedQuestionToTxt(data, question, outfolder, groups="group"):
    print(question)
    q_num = str(question).split(sep=":")[0]
    open(os.path.join(outfolder, q_num+".txt"), 'w')
    with open(os.path.join(outfolder, q_num+".txt"), 'a') as f:
        f.write(question)
        for group in data[groups].value_counts().keys():
            if data[question][data[groups] == group].dropna().count() == 0:
                print("skipping")
                continue
            f.write("\n\n")
            f.write(group+": \n")

            d = data[question][data[groups] == group].dropna()
            d.to_csv(f, header=False, index=False, mode="a")

def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
