from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
import os
from matplotlib.pyplot import gca
from cycler import cycler

fpath = '/home/jbuss/.local/share/fonts/CaesarDressing-Regular.ttf'
if os.path.exists(fpath):
    prop = fm.FontProperties(fname=fpath, size=16)
    fname = os.path.split(fpath)[1]
else:
    prop = fm.FontProperties(fname=None)
    fname = None

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

def setAxesFont(ax, prop, leg_loc='upper right'):
    ax.legend(loc=leg_loc, prop=prop)
    ax.xaxis.get_label().set_fontproperties(prop)
    ax.yaxis.get_label().set_fontproperties(prop)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(prop)
    return ax

def setLines(ax):
    ax.yaxis.grid(linewidth=1., linestyle='-', color = "grey")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    return ax


def plotStackedRating(data, team_data, pc_key, team_key, rating_categories, group_name="group"):
    fig = plt.figure(figsize=(10,7))
    topic = str(pc_key).split(":")[1]
    print(topic)
    fig.canvas.set_window_title(topic)
    gs = gridspec.GridSpec(3, 1)
    plt.subplots_adjust(hspace = 0.3)
    ax1 = plt.subplot(gs[0:2,0])

    grouped = data.groupby(group_name)[pc_key]
    categories = dict()
    for name,group in grouped:
        categories[name] = pd.Categorical(group.dropna(), categories=rating_categories)
        categories[name] = categories[name].value_counts()
    categories = pd.DataFrame(categories)
    categories.plot(kind="bar", stacked=True, ax=ax1, rot=0,alpha=0.8,cmap='gnuplot')
    ax1.set_ylim([0,60])

    setAxesFont(ax1, prop)
    ax1.set_title("PARTICIPANTS", fontproperties=prop, fontsize=22)
    setLines(ax1)
    #ax1.get_yaxis().set_visible(False)

    #ax.set_xticklabels(rating_categories)
    ax2 = plt.subplot(gs[2,0], sharex=ax1)
    #ax2 = plt.subplot(313, sharex=ax1)
    team_cat = pd.Categorical(team_data[team_key].dropna(), categories=rating_categories)
    team_cat = pd.DataFrame(team_cat.value_counts())
    team_cat.plot(kind="bar", ax=ax2, rot=0, color = 'blue',alpha=0.8)
    ax2.set_ylim([0,20])
    setAxesFont(ax2, prop)
    ax2.legend().set_visible(False)
    setLines(ax2)
    ax2.set_title("TEAM", fontproperties=prop)
    #ax2.get_yaxis().set_visible(False)
    #gs.tight_layout(fig)
    plt.show()




rating_categories = ['Very good', 'Good', 'Okay', 'Not so good', 'Bad']
