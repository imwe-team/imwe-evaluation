from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from matplotlib.backends.backend_pdf import PdfPages
import logging
import click

#!/usr/bin/env python2
# -*- coding:utf-8 -*-
"""
evaluate IMWe survey
"""

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
    "Did not\n participate",)

IGs = (
    "1 Times",
    "2 Times",
    "3 Times",
    "4 Times",
    "5 Times",
    "6 Times",
    "More than 6 Times",)

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

@click.command()
@click.argument('pc_num_file', type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True) )
@click.argument('pc_txt_file', type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True) )
@click.argument('team_num_file', type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True) )
@click.argument('team_txt_file', type=click.Path(exists=True, dir_okay=False, file_okay=True, readable=True) )
@click.option('--outfile_answers', type=click.Path(exists=False, dir_okay=False, file_okay=True, readable=True) )
@click.option('--outfile_ratings', type=click.Path(exists=False, dir_okay=False, file_okay=True, readable=True) )
@click.option('--outfile_charts', type=click.Path(exists=False, dir_okay=False, file_okay=True, readable=True) )

def main(pc_num_file, pc_txt_file, team_num_file, team_txt_file, outfile_answers, outfile_ratings, outfile_charts):

    # Read in the evaluation files of Team and PCs
    pcData      = readCsvFile2(PC_num_ind)
    pcTxtData      = readCsvFile2(PC_txt_ind)
    teamData    = readCsvFile2(TEAM_num_ind)

    pcData.fillna(0, inplace=True)
    teamData.fillna(0, inplace=True)

    aFile = open(answersFile, 'w')

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

if __name__ == "__main__":
    main()
