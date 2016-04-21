#!/usr/bin/env python2
"""Plot Ages

Usage:
 plot_ages.py [options]

Options:
 --ignore <keys>      keys to ignore as comma separated list
 --tablename=<name>   [default: table]
 --gammafile=<name>   [default: None]
"""
from __future__ import print_function
import numpy as np
import pandas as pd
from docopt import docopt
import matplotlib.pyplot as plt

pc_file="data/Export_XLSX_Apr_10_2016_07_32_PM_PCs.xlsx"
data = pd.read_excel(pc_file)
data["PC"] = True

def reindexSeries(series, indexes):
    return series.reindex(indexes)

def searchKeysByRegex(data, regex):
    keys = data.filter(regex=regex).keys()
    return keys.values

def countValuesByOccurency(data):
    return data.value_counts()

def correctGenders(data, key):
    data['female'] = np.logical_or(data[key].str.contains('f'), data[key].str.contains('w'))
    data.loc[data['female'] == True, key] = "female"
    data.loc[data['female'] == False, key] = "male"
    return data

def plotCategories(dist, title):
    plt.figure()
    plt.bar(range(len(dist)), dist.values, align='center')
    plt.xticks(range(len(dist)), dist.index, size='small')
    plt.title(key)
    plt.show()

def plotCategories2(data, categories=['< 18', '18-25', '26-30', '> 30']):
    rating = pd.Categorical(data, categories=categories)
    plt.figure()
    rating.value_counts().plot(kind='bar')
    #plt.title(data.key())
    plt.show()


rating_categories = ['Very good', 'Good', 'Okay', 'Not so good', 'Bad']

num_imwes_key = searchKeysByRegex(data, "Q1:")
data[num_imwes_key].hist()

age_keys = searchKeysByRegex(data, "Q2:")
key = age_keys[0]
plotCategories2(data[key], categories=['< 18', '18-25', '26-30', '> 30'])

#plotCategories(age_dist, key)

gender_keys = searchKeysByRegex(data, "Q3:")
key = gender_keys[0]
data = correctGenders(data, key)
gender_dist = data[key].dropna()
gender_dist = countValuesByOccurency(gender_dist)
plotCategories2(data[key], categories=['female', 'male'])

key = searchKeysByRegex(data, "Q4:")[0]
plotCategories2(data[key], categories=rating_categories)

key = searchKeysByRegex(data, "Q6:")[0]
plotCategories2(data[key], categories=rating_categories)

key = searchKeysByRegex(data, "Q8:")[0]
plotCategories2(data[key], categories=rating_categories)

key = searchKeysByRegex(data, "Q10:")[0]
plotCategories2(data[key], categories=rating_categories)

key = searchKeysByRegex(data, "Q17:")[0]
plotCategories2(data[key], categories=rating_categories)

key = searchKeysByRegex(data, "Q22:")[0]
plotCategories2(data[key], categories=rating_categories)

num_imwes_key = searchKeysByRegex(data, "Q1:")
data[num_imwes_key].hist()

num_igs_key = searchKeysByRegex(data, "Q25:")
data[num_igs_key].hist()

num_migs_key = searchKeysByRegex(data, "Q27:")
data[num_migs_key].hist()
