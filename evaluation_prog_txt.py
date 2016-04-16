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
import math
from matplotlib.backends.backend_pdf import PdfPages

__author__ = 'jbuss'


base_folder = path.join("/home/jbuss/VCP/IMWe/2015/Eval")
PC_num_ind  = path.join(base_folder, "PC_num_ind.csv")
PC_txt_ind  = path.join(base_folder, "PC_txt_ind.csv")

TEAM_num_ind  = path.join(base_folder, "TEAM_num_ind.csv")
TEAM_txt_ind  = path.join(base_folder, "TEAM_txt_ind.csv")

pRatings = PdfPages(path.join(base_folder, "WS_Ratings.pdf"))
pPieCharts = PdfPages(path.join(base_folder, "WS_PieCharts.pdf"))

answersFile =  path.join(base_folder, "answers.doc")


categories = (
"Very good",
"Good",
"Middle",
"Not so good",
"Bad",
"Did not\n participate",
)

IGs = (
"1 Times",
"2 Times",
"3 Times",
"4 Times",
"5 Times",
"6 Times",
"More than 6 Times",
)

questions ={
    "01_Teamer"                        : (None,   1, "name"),
    "02_Workshop"                      : (15,  None, "rating", 9),
    "03_Workshop_Rating"               : (16,    15, "rating", 6),
    "04_Comments_Workshop"             : (17,    16, "comment"),
    "05_Program_Contribution"          : (18,  None, "comment"),
    "06_Program_Contribution_2016"     : (19,  None, "comment"),
    "07_IGs"                           : (20,  None, "rating", 7),
    "08_Comments_IG"                   : (21,    17, "comment"),
    "09_Music_IGs"                     : (22,  None, "rating", 5),
    "10_Comments_Music_IGs"            : (23,    18, "comment"),
    "11_Arrival"                       : (24,    19, "rating", 6),
    "12_Welcome"                       : (25,    20, "rating", 6),
    "13_Opening"                       : (26,    21, "rating", 6),
    "14_Comments_1st_day"              : (27,    22, "comment"),
    "15_Games"                         : (28,    23, "rating", 6),
    "16_International_Evening"         : (29,    24, "rating", 6),
    "17_Comments_2nd_day"              : (30,    25, "comment"),
    "18_Night_Game"                    : (31,    26, "rating", 6),
    "19_Comments_3rd_day"              : (32,    27, "comment"),
    "20_Creative_Evening"              : (33,    28, "rating", 6),
    "21_Comments_4th_day"              : (34,    30, "comment"),
    "22_Night_Dance"                   : (35,    29, "rating", 6),
    "23_Day_Out_Places"                : (36,    19, "rating", 6),
    "24_Day_Out"                       : (37,    None, "rating", 6),
    "25_Team_Day_Out"                  : (None,  32, "rating", 6),
    "26_Be_Prepared"                   : (38,    33, "rating", 6),
    "27_Comments_5th_day"              : (39,    34, "comment"),
    "28_Scouting_Cafe"                 : (40,    35, "rating", 6),
    "29_Good_Friday_Service"           : (41,    36, "rating", 6),
    "30_Comments_6th_day"              : (42,    37, "comment"),
    "31_Out_of_the_Box"                : (43,    38, "rating", 6),
    "32_Concert"                       : (44,    40, "rating", 6),
    "33_Easter_Service"                : (45,    41, "rating", 6),
    "34_Comments_7th_day"              : (46,    42, "comment"),
    "35_Easter_Walk"                   : (47,    43, "rating", 6),
    "36_End_Game"                      : (48,    44, "rating", 6),
    "37_Closing_Ceremony"              : (49,    45, "rating", 6),
    "38_Comments_8th_day"              : (50,    46, "comment"),
    "39_Give_A_Gift"                   : (51,    47, "rating", 6),
    "40_Comments_Half_Week_Game"       : (52,    48, "comment"),
    "41_Chatting_Time"                 : (53,    49, "rating", 6),
    "42_Comments_Chatting_time"        : (54,    50, "comment"),
    "43_Dream_Time"                    : (55,    51, "rating", 6),
    "44_Comments_Dream_Time"           : (56,    52, "comment"),
    "45_Closing_of_the_Day"            : (57,    53, "rating", 6),
    "46_Comments_Closing_of_the_day"   : (58,    54, "comment"),
    "47_Meditation"                    : (59,    55, "rating", 6),
    "48_Comments_Meditation"           : (60,    56, "comment"),
    "49_Envenings"                     : (61,    57, "rating", 6),
    "50_Comments_Envenings"            : (62,    58, "comment"),
    "51_Comments_Program_Week"         : (63,    59, "comment"),

}

pcCategories = "1st_Time_PC", "2-8_time_PC", "More_Than_8_Times_PC"

workshops = {
"Q15_1" : "Rattlesnake Gazette",
"Q15_2" : "WANTED - Portray Drawing",
"Q15_3" : "World of Wonders",
"Q15_4" : "Bead it!",
"Q15_5" : "Stamped!",
"Q15_6" : "The black tent accademy",
"Q15_7" : "Midnight in Rattlesnake Creek",
"Q15_8" : "The Sound of Litter",
"Q15_9" : "Felting",
}

teamers = {
"Liene" :           (None,1),
"Schabi" :          ("Q15_2",2),
"Julia" :           ("Q15_4",3),
"Lubeck" :          ("Q15_7",4),
"Daniel" :          ("Q15_6",5),
"Chris" :           ("Q15_7",6),
"Jens Buss" :       ("Q15_8",7),
"Jon" :             ("Q15_3",8),
"Stef" :            ("Q15_9",9),
"Brajda" :          ("Q15_1",10),
"Sheriff Gump" :    ("Q15_8",11),
"Rieke" :           ("Q15_5",12),
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

#Main FUnction
if __name__ == "__main__":
    # Read in the evaluation files of Team and PCs
    pcData      = readCsvFile2(PC_num_ind)
    pcTxtData      = readCsvFile2(PC_txt_ind)
    teamData    = readCsvFile2(TEAM_num_ind)

    pcData.fillna(0, inplace=True)
    teamData.fillna(0, inplace=True)

    aFile = open(answersFile, 'w')

    # Reproduce Question 24
    # print(pcData["Q"])
    # for key in sorted(questions.iterkeys()):
    #     category = questions[key]
    #
    #
    #     if "rating" in questions[key][2] and not "Workshop" in key :
    #         continue
    #         print (category[0], category[1], key)
    #
    #         numIMWesKeys = getRatingKeys(1, nMax=questions[key][3]+1)
    #
    #         print(numIMWesKeys[0])
    #         newPcData = pcData.loc[pcData[numIMWesKeys[0]] == 1]
    #         medPcData = pcData.loc[pcData[numIMWesKeys[1]] == 2]
    #         oldPcData = pcData.loc[pcData[numIMWesKeys[2]] == 3]
    #
    #         combinedPCs = histogramQuestionRating(getRatingKeys(category[0], nMax=7), pcData)
    #         newPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), newPcData)
    #         medPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), medPcData)
    #         oldPcArray = histogramQuestionRating(getRatingKeys(category[0], nMax=7), oldPcData)
    #
    #         pcArray = (newPcArray, medPcArray, oldPcArray)
    #
    #         teamArray = histogramQuestionRating(getRatingKeys(category[1], nMax=7), teamData)
    #
    #
    #         plotRatingHistogram( pcArray, teamArray, categories)
    #
    #         print(pcArray, teamArray)
    #         print(combinedPCs)
    #
    #         if combinedPCs:
    #             sizes = (combinedPCs[0][5], combinedPCs[1] - combinedPCs[0][5])
    #             labels = 'not participated', 'participated'
    #             plotPyChart(sizes, labels, key+ " (PCs)")
    #
    #             sizes = (100 - combinedPCs[1], combinedPCs[1])
    #             labels = 'not participated', 'participated'
    #             plotPyChart(sizes, labels, "Survey ("+key+ ") PCs")
    #
    #         if teamArray:
    #             sizes = (teamArray[0][5], teamArray[1] - teamArray[0][5])
    #             labels = 'not participated', 'participated'
    #             plotPyChart(sizes, labels, key+ " (Team)")
    #
    #             sizes = (12 - teamArray[1], teamArray[1])
    #             labels = 'not participated', 'participated'
    #             plotPyChart(sizes, labels, "Survey ("+key+ ") Team")
    #
    #     # comments part
    #     if "comment" in questions[key][2] and not "Workshop" in key:
    #         #print (category[0], category[1], key)
    #
    #         qID_PC      = "Q{}".format(questions[key][0])
    #         qID_TEAM    = "Q{}".format(questions[key][1])
    #
    #         print("="*80)
    #         aFile.write("="*80+"\n")
    #         print(key.replace('_', ' '))
    #         aFile.write(key.replace('_', ' ')[3:].replace('Answers', '')+"\n")
    #         print("="*80)
    #         aFile.write("="*80+"\n")
    #         #print(qID_PC, qID_TEAM, key)
    #
    #         print("Team Answers")
    #         aFile.write("Team"+"\n")
    #         print("-"*80)
    #         aFile.write("-"*80+"\n")
    #
    #
    #         if questions[key][1]:
    #             for id in teamers:
    #                 respondentnumber = int(teamers[id][1])-1
    #                 query = "Respondent_Number == {}".format( respondentnumber )
    #                 if teamData[qID_TEAM][respondentnumber]:
    #                     print(id+": ", teamData[qID_TEAM][respondentnumber])
    #                     aFile.write(id.encode('utf-8')+": "+ teamData[qID_TEAM][respondentnumber].encode('utf-8')+"\n\n")
    #
    #                     #
    #                     # for line in teamData[qID_TEAM]:
    #                     #         if line == 0:
    #                     #             continue
    #                     #         print("- "+line)
    #                     #         aFile.write("- "+ line.encode('utf-8')+"\n")
    #                     #         # aFile.write(teamData["Q1"][respondentnumber].encode('utf-8')+": "+ teamData[qID_TEAM][respondentnumber].encode('utf-8')+"\n\n")
    #
    #         if not questions[key][0]:
    #             print(questions[key])
    #             aFile.write(questions[key]+"\n")
    #             continue
    #         for i in range(1,4):
    #             print("-"*80)
    #             aFile.write("-"*80+"\n")
    #             print(pcCategories[i-1].replace('_', ' ')+" Answers")
    #             aFile.write(pcCategories[i-1].replace('_', ' ')+"\n")
    #             print("-"*80)
    #             aFile.write("-"*80+"\n")
    #
    #             field = "Q1_"+str(i)
    #             data = pcData.query("{} == {}".format(field, i))
    #             for line in data[qID_PC]:
    #                 if line == 0:
    #                     continue
    #                 print("<> "+line)
    #                 aFile.write("- "+line.encode('utf-8')+"\n")
    #
    #     # workshop comments part
    #     if "comment" in questions[key][2] and "Workshop" in key:
    #         #check for workshop
    #         qID_PC      = "Q{}".format(questions[key][0])
    #         qID_TEAM    = "Q{}".format(questions[key][1])
    #
    #         print("="*80)
    #         aFile.write("="*80+"\n")
    #         print(key.replace('_', ' '))
    #         aFile.write(key.replace('_', ' ')[3:]+"\n")
    #         print("="*80)
    #         aFile.write("="*80+"\n")
    #
    #         for ws_key in workshops:
    #             print("="*80)
    #             aFile.write("="*80+"\n")
    #             print(workshops[ws_key])
    #             aFile.write(workshops[ws_key]+"\n")
    #
    #             ws_teamer = list()
    #             for id in teamers:
    #                 if teamers[id][0] == ws_key:
    #                     ws_teamer.append(id)
    #             print("Teamers: {}".format(ws_teamer))
    #             aFile.write("Teamers: ")
    #             for teamer in ws_teamer:
    #                 aFile.write(teamer+", ")
    #             aFile.write("\n\n")
    #             print("-"*80)
    #
    #             # PC comments
    #             for i in range(1,4):
    #                 print()
    #                 print(pcCategories[i-1].replace('_', ' '))
    #                 aFile.write("-"*80+"\n")
    #                 aFile.write(pcCategories[i-1].replace('_', ' ')+"\n")
    #                 print("-"*80)
    #                 aFile.write("-"*80+"\n")
    #
    #                 field = "Q1_"+str(i)
    #                 data = pcData.query("{} == {}".format(field, i)).query("{} == {}".format(ws_key, ws_key.split("_")[1]))
    #                 for line in data[qID_PC]:
    #                     if line == 0:
    #                         continue
    #                     print("<> "+line)
    #                     aFile.write("<> "+line.encode('utf-8')+"\n\n")
    #
    #             #Teamer comments:
    #             print("Team Answers")
    #             aFile.write("-"*80+"\n")
    #             aFile.write("Workshop Leader(s)"+"\n")
    #             print("-"*80)
    #             aFile.write("-"*80+"\n")
    #
    #             for ws_leader in ws_teamer:
    #                 respondentnumber = int(teamers[ws_leader][1])-1
    #                 print(teamData["Q1"][respondentnumber]+": ", teamData[qID_TEAM][respondentnumber])
    #                 aFile.write(teamData["Q1"][respondentnumber].encode('utf-8')+": "+ teamData[qID_TEAM][respondentnumber].encode('utf-8')+"\n\n")
    #
    #                 # workshop comments part
    #                 # if "rating" in questions[key][2] and "Workshop" in key:

    ws_categories = list()
    for i in sorted(workshops):
        ws_categories.append(workshops[i][:20])

    print(ws_categories)

    #PC distribution over WS
    pc_qs = list()
    for i in range(1,4):
        pc_qs.append("Q1_{}".format(i))

    print(pc_qs)

    ws_qs = list()
    for i in range(1,len(workshops)+1):
        ws_qs.append("Q15_{}".format(i))

    print(ws_qs)

    wsop_qs = list()
    for i in range(1,len(categories)):
        wsop_qs.append("Q16_{}".format(i))

    print(wsop_qs)

    # pcArray=list()
    # for i,pc in enumerate(pc_qs):
    #     query = "{} == {}".format(pc,i+1)
    #     data = np.array(pcData.query(query)[ws_qs])
    #     data[data != 0] = 1
    #     pcArray.append(data.sum(axis=0))
    # pcArray = np.array(pcArray)
    # print(pcArray, pcArray.sum(axis=0))
    #
    # plotHistogramArray(pcArray, ws_categories, pcCategories, "Workshop")
    # plt.savefig(path.join(base_folder, "pix", "WorkshopDist.png"))
    #
    # pcArray=list()
    # for i,pc in enumerate(pc_qs):
    #     pc_query = "{} == {}".format(pc,i+1)
    #     data = np.array(pcData.query(pc_query)[wsop_qs])
    #     data[data != 0] = 1
    #     pcArray.append(data.sum(axis=0))
    #     print(pc, data)
    # pcArray = np.array(pcArray)
    #
    # plotHistogramArray(pcArray, categories[:-1], pcCategories, "All Workshops Rating")
    # plt.savefig(path.join(base_folder, "pix", "All Workshops Rating.png"))
    #
    # wsArray=list()
    # for i,ws in enumerate(ws_qs):
    #     ws_query = "{} == {}".format(ws,i+1)
    #     print(ws_query, wsop_qs)
    #     pcArray=list()
    #     for i,pc in enumerate(pc_qs):
    #         pc_query = "{} == {}".format(pc,i+1)
    #         data = np.array(pcData.query(ws_query).query(pc_query)[wsop_qs])
    #         data[data != 0] = 1
    #         pcArray.append(data.sum(axis=0))
    #         print(pc, data)
    #     pcArray = np.array(pcArray)
    #
    #     plotHistogramArray(pcArray, categories[:-1], pcCategories, workshops[ws]+" Rating")
    #     plt.savefig(path.join(base_folder, "pix", workshops[ws]+" Rating.png"))
    #
    #
    # imweop_qs = list()
    # for i in range(1,len(categories)):
    #     imweop_qs.append("Q2_{}".format(i))
    #
    # # IMWe rating
    # wsArray=list()
    # for i,ws in enumerate(ws_qs):
    #     ws_query = "{} == {}".format(ws,i+1)
    #     print(ws_query, wsop_qs)
    #     pcArray=list()
    #     for i,pc in enumerate(pc_qs):
    #         pc_query = "{} == {}".format(pc,i+1)
    #         data = np.array(pcData.query(ws_query).query(pc_query)[imweop_qs])
    #         data[data != 0] = 1
    #         pcArray.append(data.sum(axis=0))
    #         print(pc, data)
    #     pcArray = np.array(pcArray)
    #
    #     plotHistogramArray(pcArray, categories[:-1], pcCategories, workshops[ws]+" Rating IMWe")
    #     plt.savefig(path.join(base_folder, "pix", workshops[ws]+" Rating IMWe.png"))

    # IG participation
    ig_qs = list()
    for i in range(1,len(IGs)+1):
        ig_qs.append("Q20_{}".format(i))

    pcArray=list()
    for i,pc in enumerate(pc_qs):
        pc_query = "{} == {}".format(pc,i+1)
        data = np.array(pcData.query(pc_query)[ig_qs])
        data[data != 0] = 1
        pcArray.append(data.sum(axis=0))
        print(pc, data)
    pcArray = np.array(pcArray)

    plotHistogramArray(pcArray, IGs, pcCategories, "IG Participation")
    plt.savefig(path.join(base_folder, "pix", "IG_Participation.png"))

    pRatings.close()
    pPieCharts.close()

    # Music IG participation
    ig_qs = list()
    for i in range(1,len(IGs)-1):
        ig_qs.append("Q22_{}".format(i))

    pcArray=list()
    for i,pc in enumerate(pc_qs):
        pc_query = "{} == {}".format(pc,i+1)
        data = np.array(pcData.query(pc_query)[ig_qs])
        data[data != 0] = 1
        pcArray.append(data.sum(axis=0))
        print(pc, data)
    pcArray = np.array(pcArray)

    plotHistogramArray(pcArray, IGs[:-2], pcCategories, "Music IG Participation")
    plt.savefig(path.join(base_folder, "pix", "MusicIGParticipation.png"))

    # pRatings.close()
    # pPieCharts.close()