#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
evaluate IMWe survey
"""

from __future__ import print_function, division

from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

__author__ = 'jbuss'


base_folder = path.join("/home/jbuss/VCP/IMWe/2015/Eval")
PC_num_ind  = path.join(base_folder, "PC_num_ind.csv")
PC_txt_ind  = path.join(base_folder, "PC_txt_in.csv")

TEAM_num_ind  = path.join(base_folder, "TEAM_num_ind.csv")
TEAM_txt_ind  = path.join(base_folder, "TEAM_txt_ind.csv")

pRatings = PdfPages(path.join(base_folder, "Ratings.pdf"))
pPieCharts = PdfPages(path.join(base_folder, "PieCharts.pdf"))


categories = (
"Very good",
"Good",
"Middle",
"Not so good",
"Bad",
"Did not\n participate",
"Total respondents",
"Respondents who skipped this question",
"Did not participate"
)

questions ={
    "Arrival"                   : (24,    19),
    "Welcome"                   : (25,    20),
    "Opening"                   : (26,    21),
    "Games"                     : (28,    23),
    "International_Evening"     : (29,    24),
    "Night_Game"                : (31,    26),    "Creative_Evening"          : (33,    28),
    "Night_Dance"               : (35,    29),
    "Day_Out"                   : (37,    31),
    "Team_Day_Out"              : (None,  32),
    "Be_Prepared"               : (38,    33),
    "Scouting_Cafe"             : (40,    35),
    "Good_Friday_Service"       : (41,    36),
    "Out_of_the_Box"            : (43,    38),
    "Concert"                   : (44,    40),
    "Easter_Service"            : (45,    41),
    "Easter_Walk"               : (47,    43),
    "End_Game"                  : (48,    44),
    "Closing_Ceremony"          : (49,    45),
    "Give_A_Gift"               : (51,    47),
    "Chatting_Time"             : (53,    49),
    "Dream_Time"                : (55,    51),
    "Closing_of_the_Day"        : (57,    53),
    "Meditation"                : (59,    55),
    "Envenings"                 : (61,    57),
}




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


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

def plotRatingHistogram( array1, array2, categories, relative=False):
    figPlot = plt.figure()
    with plt.xkcd():
        fig, ax = plt.subplots()
        index = np.arange(6)
        bar_width = 0.5
        opacity = 0.7

        max1 = max2 = 0

        numRespondents=0
        for i in range(0,3):
            if array1[i]:
                numRespondents+=array1[i][1]

        factor = 1
        yprefix = "Total "
        ysuffix = ""
        if relative:
            factor = 100/numRespondents
            yprefix ="Relative "
            ysuffix = " [ %]"

        max1 = 0
        if array1:
            if array1[0]:
                rects1 = plt.bar(index, factor*array1[0][0][:6], bar_width,
                         alpha=opacity,
                         color='c',
                         label='PCs (1)')
                max1 += array1[0][0][:6]


            if array1[1]:
                rects2 = plt.bar(index, factor*array1[1][0][:6], bar_width,
                         alpha=opacity,
                         color='b',
                         bottom=factor*array1[0][0][:6],
                         label='PCs (2-8)')
                max1 += array1[1][0][:6]


            if array1[2]:
                rects3 = plt.bar(index, factor*array1[2][0][:6], bar_width,
                         alpha=opacity,
                         color='g',
                         bottom=factor*array1[0][0][:6]+factor*array1[1][0][:6],
                         label='PCs (>8)')
                max1 += array1[2][0][:6]


            if numRespondents:
                max1 = np.max( max1*factor)

        if array2:
            rects4 = plt.bar(index + bar_width, factor*array2[0][:6]/array2[1], bar_width,
                     alpha=opacity,
                     color='r',
                     label='Team')
            max2 = np.max(array2[0][:6]/array2[1]*factor)




        max3 = np.maximum(max2,max1)
        print(max3, max1, max2)

        plt.ylim(0, max3+10)
        # plt.xlabel('Rating')
        plt.ylabel(yprefix +'Number of Respondents'+ysuffix)
        title = str(key).replace("_", " ")
        plt.title(title, fontdict = {'verticalalignment': 'bottom'})
        plt.xticks(index + bar_width, categories)
        plt.legend(loc='best', fancybox=True, framealpha=0.5,prop={'size':10})

        plt.tight_layout()
        pRatings.savefig()
        plt.savefig(path.join(base_folder, "pix", title+"Dist.png"))
        #plt.show()

def plotPyChart(sizes ,labels, title):
    figPie = plt.figure(figsize=(8,8))
    def my_autopct(pct):
        total=sum(sizes)
        val=int(pct*total/100.0)
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)

    if not sizes:
        return



    with plt.xkcd():
        # with plt.xkcd():
        import matplotlib as mpl
        mpl.rcParams['font.size'] = 20.0
        mpl.rcParams['font.weight'] = 'bold'
        # mpl.rcParams['font.family'] = 'serif'
        title = str(title).replace("_", " ")
        explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
        colors = ['red', 'blue', 'lightskyblue', 'lightcoral']
        plt.pie(sizes, colors=colors,
                # autopct='%1.1f%%',
                autopct=my_autopct,
                shadow=False,
                startangle=180,
                radius=0.2,
                )

        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.legend(
            loc='center left',
            bbox_to_anchor=(0.6, 0.08),
            fancybox=False,
            labels=labels,
            prop={'size':14, 'weight' : 'normal'}
        )

        plt.title(
            title,
            fontdict = {
                'verticalalignment': 'bottom',
                'size': 24,
                # 'family' : 'sans',
                'weight' : 'bold'})
        #plt.show()
        pPieCharts.savefig()
        plt.savefig(path.join(base_folder, "pix", title+"Pie.png"), bbox_inches='tight')



#Main FUnction
if __name__ == "__main__":
    # Read in the evaluation files of Team and PCs
    pcData      = readCsvFile2(PC_num_ind)
    teamData    = readCsvFile2(TEAM_num_ind)

    # Reproduce Question 24
    # print(pcData["Q"])
    for key in questions:
        category = questions[key]
        print (category[0], category[1], key)



        numIMWesKeys = getRatingKeys(1, nMax=4)

        print(numIMWesKeys[0])
        newPcData = pcData.loc[pcData[numIMWesKeys[0]] == 1]
        medPcData = pcData.loc[pcData[numIMWesKeys[1]] == 2]
        oldPcData = pcData.loc[pcData[numIMWesKeys[2]] == 3]

        combinedPCs = histogramQuestionRating(getRatingKeys(category[0], nMax=7), pcData)
        newPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), newPcData)
        medPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), medPcData)
        oldPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), oldPcData)

        pcArray = (newPcArray, medPcArray, oldPcArray)

        teamArray = histogramQuestionRating(getRatingKeys(category[1], nMax=7), teamData)


        plotRatingHistogram( pcArray, teamArray, categories)

        print(pcArray, teamArray)
        print(combinedPCs)

        if combinedPCs:
            sizes = (combinedPCs[0][5], combinedPCs[1] - combinedPCs[0][5])
            labels = 'not participated', 'participated'
            plotPyChart(sizes, labels, key+ " (PCs)")

            sizes = (100 - combinedPCs[1], combinedPCs[1])
            labels = 'not participated', 'participated'
            plotPyChart(sizes, labels, "Survey ("+key+ ") PCs")

        if teamArray:
            sizes = (teamArray[0][5], teamArray[1] - teamArray[0][5])
            labels = 'not participated', 'participated'
            plotPyChart(sizes, labels, key+ " (Team)")

            sizes = (12 - teamArray[1], teamArray[1])
            labels = 'not participated', 'participated'
            plotPyChart(sizes, labels, "Survey ("+key+ ") Team")


    pRatings.close()
    pPieCharts.close()




