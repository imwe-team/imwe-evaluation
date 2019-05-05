from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import re
from matplotlib.backends.backend_pdf import PdfPages

from eval_tools import *
import eval_tools as et
def printFirstKLines(filepath, k=1):
    f = codecs.open(filepath, "r", "utf-16")
    lines = f.readlines()
    for i, line in enumerate(lines):
        print(line)
        if i > k:
            break
    return lines

def getRatingKeys(questionNr, firstNum=1, nMax=6):
    if not questionNr:
        return None
    questionIds = list()
    for i in range(firstNum,nMax):
        questionIds.append("Q{}_{}".format(questionNr, i))
    return questionIds

def getRatingForQuestion(qNr, dataFrame):
    return dataFrame[getRatingKeys(qNr)]

def getQNumber(question):
    return str(question).split(sep=":")[0]

def histogramQuestionRating(keys, dataFrame):
    if not keys:
        return None
    for key in keys:
        if not key in dataFrame.columns:
            dataFrame[key] = None

    data = dataFrame[keys]
    output = list()
    for i, key in enumerate(data.keys()):
        output.append(data[key].sum()/(i+1))

    output = np.nan_to_num(np.array(output))
    sum = output.sum()
    return output, sum

def reindexSeries(series, indexes):
    return series.reindex(indexes)

def searchKeyByRegex(data, regex):
    keys = data.filter(regex=regex).keys()
    return keys.values[0]

# def searchKeysByRegex(data, regex):
#     keys = data.filter(regex=regex).keys()
#     return keys.values

def countValuesByOccurency(data):
    return data.value_counts()

def correctGenders(data, key=None):
    if key == None:
        key = data.filter(regex='gender').keys()[0]
    data['female'] = np.logical_or(data[key].str.contains('f'), data[key].str.contains('w'))
    data.loc[data['female'] == True, key] = "female"
    data.loc[data['female'] == False, key] = "male"
    return data

def definePCgroup(data, col_name="group"):
    mask1  = data[searchKeyByRegex(data, "Q1")] == 1
    mask23 = np.logical_and(data[searchKeyByRegex(data, "Q1")] > 1, data[searchKeyByRegex(data, "Q1")] < 4)
    mask4  = data[searchKeyByRegex(data, "Q1")] >= 4
    data.loc[mask1,  col_name] = "1st Time"
    data.loc[mask23, col_name] = "2-3 Times"
    data.loc[mask4,  col_name] = ">3 Times"
    return data

def getGroupedCategories(data, key, group_name):
    grouped = data.groupby(group_name)[key]
    categories = dict()
    for name,group in grouped:
        categories[name] = pd.Categorical(group.dropna(), categories=et.rating_categories)
        categories[name] = categories[name].value_counts()
    categories = pd.DataFrame(categories)
    return categories

def convertNanToStr(categories):
    for k, cat in enumerate(categories):
        if str(cat) == 'nan':
            categories[k]='nan'
    return categories

def shortenWhitespace(txt):
    return re.sub( '\s\s+', '; ', txt ).strip()
