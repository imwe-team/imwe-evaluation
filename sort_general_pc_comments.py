#!/usr/bin/env python2
"""Plot Ages

Usage:
 sort_general_pc_comments.py [options]

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
outfolder   ="./txt/pcs/"
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
comments = questions[questions.Type == "Comments"]

data = definePCgroup(data, col_name="group")

questions = comments['Question']
writeSortedQuestionsToTxt(data, questions, outfolder, "group")
