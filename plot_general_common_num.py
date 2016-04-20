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

pc_file     ="data/2016_PCs_txt.xlsx"
team_file   ="data/2016_Team_txt.xlsx"
q_file      = dict(
                io  = "data/2016/Questions.xls",
                sheetname = "common" )
data = pd.read_excel(pc_file)
team_data = pd.read_excel(team_file)

data.drop(data.index[0], inplace=True)
team_data.drop(team_data.index[0], inplace=True)

questions = pd.read_excel(**q_file)
questions["qnPc"]     = questions.PCs.apply(lambda x: str(x).split(":")[0]+":")
questions["qnTeam"]   = questions.Team.apply(lambda x: str(x).split(":")[0]+":")

num_questions = questions[questions.Type != "Comments"]
ratings = num_questions[questions.Type == "Rating"]

data = definePCgroup(data, col_name="group")

#ws = data.groupby(searchKeyByRegex(data, "Q21:"))

#for q_pc, q_team, q_type in zip(ratings.qnPc, ratings.qnTeam, ratings.Type):
#print(q_pc, q_team, q_type)
pc_key = searchKeyByRegex(data, "Q4:")
#team_key = searchKeyByRegex(team_data, q_team)
#print(pc_key, team_key, q_type)
fig = plt.figure()
ax = fig.add_subplot(111)
#data["cat"+pc_key] = pd.Categorical(data[pc_key].dropna(), categories=rating_categories)
grouped = data.groupby("group")[pc_key]
categories = dict()
for name,group in grouped:
    categories[name] = pd.Categorical(group.dropna(), categories=rating_categories)
    categories[name] = categories[name].value_counts()
categories = pd.DataFrame(categories)
categories.plot(kind="bar", stacked=True, ax=ax, rot=0)
#ax.set_xticklabels(rating_categories)

plt.show()


#
#
# num_imwes_key = searchKeysByRegex(data, "Q1:")
# data[num_imwes_key].hist()
#
# age_keys = searchKeysByRegex(data, "Q2:")
# key = age_keys[0]
# plotCategories2(data[key], categories=['< 18', '18-25', '26-30', '> 30'])
#
# #plotCategories(age_dist, key)
#
# gender_keys = searchKeysByRegex(data, "Q3:")
# key = gender_keys[0]
# data = correctGenders(data, key)
# gender_dist = data[key].dropna()
# gender_dist = countValuesByOccurency(gender_dist)
# plotCategories2(data[key], categories=['female', 'male'])
#
# key = searchKeysByRegex(data, "Q4:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# key = searchKeysByRegex(data, "Q6:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# key = searchKeysByRegex(data, "Q8:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# key = searchKeysByRegex(data, "Q10:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# key = searchKeysByRegex(data, "Q17:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# key = searchKeysByRegex(data, "Q22:")[0]
# plotCategories2(data[key], categories=rating_categories)
#
# num_imwes_key = searchKeysByRegex(data, "Q1:")
# data[num_imwes_key].hist()
#
# num_igs_key = searchKeysByRegex(data, "Q25:")
# data[num_igs_key].hist()
#
# num_migs_key = searchKeysByRegex(data, "Q27:")
# data[num_migs_key].hist()
