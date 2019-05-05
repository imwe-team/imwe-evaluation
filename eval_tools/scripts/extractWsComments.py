import pandas as pd
import numpy as np
from os import path
import click
import eval_tools as et
from eval_tools.tools import getQNumber, convertNanToStr, shortenWhitespace, searchKeyByRegex

@click.command()
@click.argument('pc_txt',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.argument('ws_question')
@click.argument('team_txt',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.argument('questions',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.argument('output', type=click.Path(exists=False, dir_okay=False, file_okay=True))
def main(pc_txt, ws_question, team_txt, questions, output):
    '''
    Script to sort and extract the workshop related comment fields from the imwe evalutaion

    Parameters:

    -----------

    PC_TXT: Path to xlsx with PC answers
    
    WS_QUESTION: number of the workshop question e.g. Q20

    TEAM_TXT: Path to xlsx with team answers

    QUESTIONS: Path to xlsx file containing a table "Common" telling the question names
    '''

    df_pc_txt = et.io.readTxtExcelFileToDf(pc_txt)
    df_team_txt = et.io.readTxtExcelFileToDf(team_txt)
    df_questions = et.io.readConfigXlsxToDf(questions)

    # Correct pc questions
    df_pc_txt = et.tools.correctGenders(df_pc_txt)

    categories_mask = np.logical_and(df_questions.Type == 'Categories', df_questions.PC == searchKeyByRegex(df_pc_txt,str(ws_question)  ))
    WsCategories = df_questions[categories_mask]
    WsComments = df_questions[df_questions.Type == 'WsComments']

    with open(output, 'w') as f:
        for name, group in df_pc_txt.groupby(searchKeyByRegex(df_pc_txt,str(ws_question)    )):
            print(name)
            f.write(name)
            f.write("\n\nPCs:")
            for i, row in group[WsComments.PC].iterrows():
                if len(row.values) > 1:
                    print("alert")
                comment = shortenWhitespace(str(row.values[0]))
                if not comment == 'nan':
                    f.write("\n"+comment)
            f.write("\n\nTeamer:" )
            mask = df_team_txt[WsCategories.Team] == name
            for index, row in df_team_txt[mask.values].iterrows():
                comment = shortenWhitespace(str(row[searchKeyByRegex(df_team_txt,'Q1')]))
                f.write("\n\n"+comment+": ")
                f.write(str(row[WsComments.Team].values[0]))
            f.write("\n\n")

if __name__ == "__main__":
    main()
