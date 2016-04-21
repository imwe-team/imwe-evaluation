#!/usr/bin/env python2
"""Plot Ages

Usage:
 plot_general_common_num.py [options]

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
from eval_tools import *
import os

pc_file     ="data/2016_PCs_txt.xlsx"
team_file   ="data/2016_Team_txt.xlsx"
outfolder   ="./images/pcs/"
q_file      = dict(
                io  = "data/2016/Questions.xls",
                sheetname = "pc_only" )
data = pd.read_excel(pc_file)
team_data = pd.read_excel(team_file)

data.drop(data.index[0], inplace=True)
team_data.drop(team_data.index[0], inplace=True)

questions = pd.read_excel(**q_file)

num_questions = questions[questions.Type != "Comments"]
ratings = num_questions[questions.Type == "Rating"]

data = definePCgroup(data, col_name="group")

#Number of imweop_qs
num_imwes_key = searchKeyByRegex(data, "Q1:")
fig = plotHistogram(data, num_imwes_key)
fig.savefig(os.path.join(outfolder,"Q1"+".png"), dpi=300, transparent=True)

ages_key = searchKeyByRegex(data, "Q2:")
fig = plotCategories(data, ages_key, categories=age_categories)
fig.savefig(os.path.join(outfolder,"Q2"+".png"), dpi=300, transparent=True)

gender_key = searchKeyByRegex(data, "Q3:")
data = correctGenders(data, gender_key)
fig = plotCategories(data, gender_key, categories=['female', 'male'])
fig.savefig(os.path.join(outfolder,"Q3"+".png"), dpi=300, transparent=True)

fig = plotCategoriesPyChart(data, gender_key, categories=['female', 'male'])
fig.savefig(os.path.join(outfolder,"Q3_pie"+".png"), dpi=300, transparent=True)

info_key = searchKeyByRegex(data, "Q13:")
fig = plotCategories(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q13"+".png"), dpi=300, transparent=True)

fig = plotCategoriesPyChart(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q13_pie"+".png"), dpi=300, transparent=True)

info_key = searchKeyByRegex(data, "Q14:")
fig = plotCategories(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q14"+".png"), dpi=300, transparent=True)

fig = plotCategoriesPyChart(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q14_pie"+".png"), dpi=300, transparent=True)

info_key = searchKeyByRegex(data, "Q15:")
fig = plotCategories(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q15"+".png"), dpi=300, transparent=True)

fig = plotCategoriesPyChart(data, info_key, categories=binary_categories)
fig.savefig(os.path.join(outfolder,"Q15_pie"+".png"), dpi=300, transparent=True)

# #where did you find out about imwe?
keys = searchKeysByRegex(data, "Q18")
sources_df = data[keys]

source_categorie ={
    "Q18_0": "previous IMWes",
    "Q18_1": "Facebook",
    "Q18_2": "From a friend",
    "Q18_3": "Scout leader",
    "Q18_4": "Scout event",
    "Q18_5": "Scouting magazine",
    "Q18_6": "Scout center, office etc.",
    "Q18_7": "Other, please specify ",
    }

sources_df = sources_df.rename(columns=source_categorie)
sources = dict()
for key in sources_df.keys():
    sources[key] = sources_df[key].count()
sources = pd.DataFrame.from_dict(sources, 'index')
sources_counted = sources.drop("Other, please specify ").sort_index()

fig = plotCategorizedIndexDf(sources_counted.sort_values(by=0), 0, title = "source")
fig.savefig(os.path.join(outfolder,"Q18"+".png"), dpi=300, transparent=True)

fig = plotPyChart(sources_counted.values.flatten() ,sources_counted.index, "Source")
fig.savefig(os.path.join(outfolder,"Q18_pie"+".png"), dpi=300, transparent=True)

#Handles others
others = sources_df["Other, please specify "].dropna()
for alternative in others:
    row = sources_df.query(sources_df["Other, please specify "] == alternative)
    print("\n\n"+alternative+"\n\n", row.dropna(axis=1).values)
