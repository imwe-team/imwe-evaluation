from os import path
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import re
from matplotlib.backends.backend_pdf import PdfPages

from eval_tools.tools import getQNumber, convertNanToStr, shortenWhitespace, searchKeyByRegex

def readTxtExcelFileToDf(path, droprow=0, **kwargs):
    df = pd.read_excel(path, **kwargs)
    df.drop(df.index[droprow], inplace=True)
    return df

def readNumExcelFileToDf(path, **kwargs):
    df = pd.read_excel(path, **kwargs)
    return df

def readConfigXlsxToDf(path, sheetname="Common", **kwargs):
    df = pd.read_excel(path, sheet_name=sheetname, **kwargs)
    return df

def writeSortedQuestionsToTxt(data, questions, outfolder, groups="group"):
    for question in questions:
        writeSortedQuestionToTxt(data, question, outfolder, groups)

def writeSortedQuestionToCsv(data, question, outfolder, groups="group"):
    print(question)
    q_num = getQNumber(question)
    open(path.join(outfolder, q_num+".txt"), 'w')
    with open(path.join(outfolder, q_num+".txt"), 'a') as f:
        f.write(question)
        for group in data[groups].value_counts().keys():
            if data[question][data[groups] == group].dropna().count() == 0:
                print("skipping")
                continue
            f.write("\n\n")
            f.write(group+": \n")

            d = data[question][data[groups] == group].dropna()
            d.to_csv(f, header=False, index=False, mode="a")

def writeCommentsToTxt(outfolder, pc_data=None, team_data=None, question=None, groups="group"):
    if question.Group == 'PC':
        q = question['PC']
        pref = '_pc'
    elif question.Group == 'Both':
        q = question['PC']
        pref = ''
    elif question.Group == 'Team':
        q = question['Team']
        pref = '_team'
    else:
        print("no group")
    q_num = getQNumber(q)

    out_file=path.join(outfolder, q_num+pref+".txt")
    print(out_file)

    open(out_file, 'w')
    with open(out_file, 'a') as f:
        f.write(q.split(": ")[1])
        if (not pc_data is None and question.PC in pc_data):
            writePcCommentsToFile(pc_data, question.PC, f, groups)
        if (not team_data is None and question.Team in team_data):
            writeTeamCommentsToFile(team_data, question.Team, f)

def writePcCommentsToFile(data, key, f_file, groups="group"):
    '''
    Write the given Pc comments to the given file
    '''
    pc_categories = convertNanToStr(data[groups].unique())
    for pc_group in sorted(pc_categories):
        comments = data[key][data[groups] == pc_group].dropna()
        if len(comments) > 0:
            f_file.write(("\n\n"+str(pc_group)+":"))
            for comment in comments:
                comment = shortenWhitespace(comment)
                f_file.write(("\n"+comment))

def writeTeamCommentsToFile(data, key, f_file):
    '''
    Write the given Team comments to the given file
    '''
    name_question = searchKeyByRegex(data, "Q1")
    # searchKeyByRegex(data, "Q1")
    names = data[name_question].unique()
    f_file.write("\n\nTeam Answers:")
    for name in sorted(names):
        name_mask = data[name_question] == name
        comments = data[key][name_mask].dropna()
        if len(comments) > 0:
            f_file.write(("\n\n"+str(name)+": "))
            for comment in comments:
                comment = shortenWhitespace(comment)
                f_file.write(comment)


def ensureDir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
