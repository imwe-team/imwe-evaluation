from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def reindexSeries(series, indexes):
    return series.reindex(indexes)

def searchKeyByRegex(data, regex):
    keys = data.filter(regex=regex).keys()
    return keys.values[0]

def countValuesByOccurency(data):
    return data.value_counts()

def correctGenders(data, key):
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
