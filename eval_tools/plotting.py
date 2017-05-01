from __future__ import print_function, division

from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl

cmap = mpl.cm.get_cmap('Set1')

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def plotRatingHistogram( array1, array2, categories):
    figPlot = plt.figure()
    with plt.xkcd():
        fig, ax = plt.subplots()
        index = np.arange(len(categories))
        bar_width = 0.5
        opacity = 0.7

        max1 = max2 = 0

        numRespondents=0
        for i in range(0,3):
            if array1[i]:
                numRespondents+=array1[i][1]

        max1 = 0
        if array1:
            if array1[0]:
                rects1 = plt.bar(index, 100*array1[0][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PCs (1)')
                max1 += array1[0][0][:6]


            if array1[1]:
                rects2 = plt.bar(index, 100*array1[1][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='b',
                         bottom=100*array1[0][0][:6]/numRespondents,
                         label='PCs (2-8)')
                max1 += array1[1][0][:6]


            if array1[2]:
                rects3 = plt.bar(index, 100*array1[2][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='g',
                         bottom=100*array1[0][0][:6]/numRespondents+100*array1[1][0][:6]/numRespondents,
                         label='PCs (>8)')
                max1 += array1[2][0][:6]


            if numRespondents:
                max1 = np.max( max1/numRespondents*100)

        if array2:
            rects4 = plt.bar(index + bar_width, 100*array2[0][:6]/array2[1], bar_width,
                     alpha=opacity,
                     color='r',
                     label='Team')
            max2 = np.max(array2[0][:6]/array2[1]*100)




        max3 = np.maximum(max2,max1)
        print(max3, max1, max2)

        plt.ylim(0, max3+10)
        plt.xlabel('Rating')
        plt.ylabel('Relative Number of Respondents [%]')
        title = str(key).replace("_", " ")
        plt.title(title, fontdict = {'verticalalignment': 'bottom'})
        plt.xticks(index + bar_width, categories)
        plt.legend(loc='best', fancybox=True, framealpha=0.5,prop={'size':10})

        plt.tight_layout()
        #pRatings.savefig()
        plt.show()

def plotRatingHistogram2( array1, categories):
    figPlot = plt.figure()
    with plt.xkcd():
        fig, ax = plt.subplots()
        index = np.arange(len(categories))
        bar_width = 0.5
        opacity = 0.7

        max1 = max2 = 0

        numRespondents=0
        for i in range(0,3):
            if array1[i].any():
                numRespondents+=array1[i].sum()

        max1 = 0
        if array1.any():
            if array1[0].any():
                rects1 = plt.bar(index, 100*array1[0][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='c',
                         label='PCs (1)')
                max1 += array1[0][0][:6]


            if array1[1].any():
                rects2 = plt.bar(index, 100*array1[1][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='b',
                         bottom=100*array1[0][0][:6]/numRespondents,
                         label='PCs (2-8)')
                max1 += array1[1][0][:6]


            if array1[2].any():
                rects3 = plt.bar(index, 100*array1[2][0][:6]/numRespondents, bar_width,
                         alpha=opacity,
                         color='g',
                         bottom=100*array1[0][0][:6]/numRespondents+100*array1[1][0][:6]/numRespondents,
                         label='PCs (>8)')
                max1 += array1[2][0][:6]


            if numRespondents:
                max1 = np.max( max1/numRespondents*100)

        if array2.any():
            rects4 = plt.bar(index + bar_width, 100*array2[0][:6]/array2[1], bar_width,
                     alpha=opacity,
                     color='r',
                     label='Team')
            max2 = np.max(array2[0][:6]/array2[1]*100)




        max3 = np.maximum(max2,max1)
        print(max3, max1, max2)

        plt.ylim(0, max3+10)
        plt.xlabel('Rating')
        plt.ylabel('Relative Number of Respondents [%]')
        title = str(key).replace("_", " ")
        plt.title(title, fontdict = {'verticalalignment': 'bottom'})
        plt.xticks(index + bar_width, categories)
        plt.legend(loc='best', fancybox=True, framealpha=0.5,prop={'size':10})

        plt.tight_layout()
        #pRatings.savefig()
        plt.show()

def plotHistogramArray(histArray, categories, setNames, title, rotatoion='vertical',relative=None):
    figPlot = plt.figure()
    with plt.xkcd():
        fig, ax = plt.subplots()
        index = np.arange(len(categories))
        bar_width = 0.5
        opacity = 0.7
        colors= 'c', 'b', 'g'

        #calculate numRespondents
        numRespondents=0
        for i in histArray:
            numRespondents+=i.sum()

        factor = 1
        yprefix = "Total "
        ysuffix = ""
        if relative:
            factor = 100/numRespondents
            yprefix ="Relative "
            ysuffix = " [ %]"


        rects = list()
        #plot histograms
        bottom =0
        for k,array in enumerate(histArray):
            if k > 0:
                bottom += histArray[k-1]
            print(k, setNames[k])
            rects.append(
                plt.bar(index,
                        factor*array,
                        bar_width,
                        alpha=opacity,
                        color=colors[k],
                        bottom=factor*bottom,
                        label=setNames[k]
                        )
            )
        plt.xlabel('Rating')
        plt.ylabel(yprefix+'Number of Respondents'+ysuffix)
        plt.title(title, fontdict = {'verticalalignment': 'bottom'})
        plt.xticks(index + bar_width, categories, rotation=rotatoion)
        plt.legend(loc='best', fancybox=True, framealpha=0.5,prop={'size':10})

        plt.tight_layout()
        # pRatings.savefig()
        #plt.show()
        figPlot.clf()



def plotPyChart(sizes ,labels, title):
    figPie = plt.figure()
    def my_autopct(pct):
        total=sum(sizes)
        val=int(pct*total/100.0)
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)

    if not sizes:
        return

    # with plt.xkcd():
    title = str(title).replace("_", " ")
    explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
    colors = ['red', 'blue', 'lightskyblue', 'lightcoral']
    plt.pie(sizes, labels=labels, colors=colors,
            # autopct='%1.1f%%',
            autopct=my_autopct,
            shadow=True,
            startangle=180,
            radius=0.5
            )
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')

    plt.title(title, fontdict = {'verticalalignment': 'bottom'})
    #plt.show()
    pPieCharts.savefig()

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
