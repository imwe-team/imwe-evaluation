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
from IPython import embed
from matplotlib import cm

fpath = '/home/jbuss/.local/share/fonts/CaesarDressing-Regular.ttf'
cmap = mpl.cm.get_cmap('Set1')

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

def definePCgroup(data, col_name="group"):
    mask1  = data[searchKeyByRegex(data, "Q1")] == 1
    mask23 = np.logical_and(data[searchKeyByRegex(data, "Q1")] > 1, data[searchKeyByRegex(data, "Q1")] < 4)
    mask4  = data[searchKeyByRegex(data, "Q1")] >= 4
    data.loc[mask1,  col_name] = "1st Time"
    data.loc[mask23, col_name] = "2-3 Times"
    data.loc[mask4,  col_name] = ">3 Times"
    return data

def setAxesFont(ax, prop, leg_loc='upper right'):
    ax.legend(loc=leg_loc, prop=prop)
    ax.xaxis.get_label().set_fontproperties(prop)
    ax.yaxis.get_label().set_fontproperties(prop)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontproperties(prop)
    return ax

def setLines(ax):
    ax.yaxis.grid(linewidth=1., linestyle='-', color = "grey")
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    return ax

def getGroupedCategories(data, key, group_name):
    grouped = data.groupby(group_name)[key]
    categories = dict()
    for name,group in grouped:
        categories[name] = pd.Categorical(group.dropna(), categories=rating_categories)
        categories[name] = categories[name].value_counts()
    categories = pd.DataFrame(categories)
    return categories

def plotStackedRating(data, team_data, pc_key, team_key, rating_categories, group_name="group"):
    fig = plt.figure(figsize=(10,7))

    topic = str(pc_key).split(":")[1]
    fig.canvas.set_window_title(topic)

    gs = gridspec.GridSpec(3, 1)
    plt.subplots_adjust(hspace = 0.3)

    categories = getGroupedCategories(data, pc_key, group_name)

    ax1 = plt.subplot(gs[0:2,0])
    categories.plot(kind="bar", stacked=True, ax=ax1, rot=0,alpha=0.8,cmap=cmap)
    ax1.set_ylim([0,60])
    setAxesFont(ax1, prop)
    setLines(ax1)
    ax1.set_title("PARTICIPANTS", fontproperties=prop, fontsize=22)

    team_cat = pd.Categorical(team_data[team_key].dropna(), categories=rating_categories)
    team_cat = pd.DataFrame(team_cat.value_counts())

    ax2 = plt.subplot(gs[2,0], sharex=ax1)
    team_cat.plot(kind="bar", ax=ax2, rot=0,alpha=0.8, color=cmap(0.2))
    ax2.set_ylim([0,20])
    setAxesFont(ax2, prop)
    setLines(ax2)
    ax2.set_title("TEAM", fontproperties=prop, fontsize=22)
    ax2.legend().set_visible(False)
    return fig

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        if height == 0:
            continue
        ax.text(rect.get_x() + rect.get_width()/2., height+0.1*np.log(height+1),
                '%d' % int(height),
                ha='center', va='bottom', fontproperties=prop)

def plotHistogram(data, key):

    fig, ax1 = plt.subplots(figsize=(10,7))
    topic = str(key).split(":")[1]
    fig.canvas.set_window_title(topic)
    gs = gridspec.GridSpec(3, 1)

    #histogramize
    hist, bins = np.histogram(data[key], bins=20)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    width = 0.9*(bins[1] - bins[0])

    #plot
    rects = ax1.bar(bin_centers, hist, align='center', width=width, alpha=0.8, color=cmap(0.5))
    ax1.set_xticks(np.arange(min(bins), max(bins)+1, 2.0))
    autolabel(rects, ax1)

    ax1.set_ylim([0,30])
    setAxesFont(ax1, prop)
    setLines(ax1)
    ax1.set_title("PARTICIPANTS", fontproperties=prop, fontsize=22)

    return fig

def plotCategories(data, key, categories=['< 18', '18-25', '26-30', '> 30']):
    fig, ax = plt.subplots(figsize=(10,7))
    topic = str(key).split(":")[1]
    fig.canvas.set_window_title(topic)

    rating = pd.Categorical(data[key], categories=categories)
    result = rating.value_counts()
#    embed()
    rects = ax.bar(range(len(result.index)), result.values, align='center', alpha=0.8, color=cmap(0.5))
    plt.xticks(range(len(result.index)), result.index, size='small')

    autolabel(rects, ax)

    ax.set_ylim([0,60])
    setAxesFont(ax, prop)
    setLines(ax)
    ax.set_title("PARTICIPANTS", fontproperties=prop, fontsize=22)

    return fig
    #plt.title(data.key())

def plotCategoriesPyChart(data, key, categories=['< 18', '18-25', '26-30', '> 30']):
    topic = str(key).split(":")[1]

    rating = pd.Categorical(data[key], categories=categories)
    result = rating.value_counts()

    fig = plotPyChart(result.values ,result.index, topic)

    return fig

def cmapToArray(cmap=cmap, ncolors=4):
    colors = []
    step=1./ncolors
    for i in np.arange(start=0, stop=1+step, step=step):
        colors.append(cmap(i))
    return np.array(colors)

def plotPyChart(sizes ,labels, title):
    fig, ax = plt.subplots(figsize=(10,7))
    fig.canvas.set_window_title(title)
    def my_autopct(pct):
        total=sum(sizes)
        val=int(pct*total/100.0)
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)

    ncolors=4
    if len(labels) > 4:
        print(len(labels))
        ncolors = len(labels)

    cs=cm.Set1(np.arange(ncolors)/float(ncolors))

    explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
    patches, texts, autotexts = ax.pie(sizes, labels=None, colors=cs,
            # autopct='%1.1f%%',
            autopct=my_autopct,
            shadow=True,
            startangle=90,
            radius=0.5
            )


    # Set aspect ratio to be equal so that pie is drawn as a circle.
    ax.axis('equal')
    ax.set_title(title, y=1.06, fontdict = {'verticalalignment': 'bottom'}, fontproperties=prop, fontsize=22)
    plt.setp(autotexts, fontproperties=prop)
    plt.setp(texts, fontproperties=prop)
    setAxesFont(ax, prop)
    ax.legend(prop=prop, labels=labels, loc="best")

    return fig

def plotCategorizedIndexDf(data, key, title = "source"):
    fig, ax = plt.subplots(figsize=(10,7))
    fig.canvas.set_window_title(title)
#    embed()
    rects = ax.bar(range(len(data[key].index)), data[key].values.flatten(), align='center', alpha=0.8, color=cmap(0.5))
    plt.xticks(range(len(data[key].index)), data[key].index, size='small', horizontalalignment='right', rotation=45)

    autolabel(rects, ax)

    ax.set_ylim([0,60])
    setAxesFont(ax, prop)
    setLines(ax)
    ax.set_title("PARTICIPANTS", fontproperties=prop, fontsize=22)

    pos1 = ax.get_position() # get the original position
    ax.set_position([pos1.x0, pos1.y0+0.2,  pos1.width, pos1.height/ 1.3]) # set a new position
    return fig
    #plt.title(data.key())

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

age_categories=['< 18', '18-25', '26-30', '> 30']

rating_categories = ['Very good', 'Good', 'Okay', 'Not so good', 'Bad']

binary_categories=['Yes', 'No']
