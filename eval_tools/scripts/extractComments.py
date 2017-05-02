import pandas as pd
import numpy as np
import click
import eval_tools as et

default_path = {
    'pc_txt' : "/Users/jbuss/Documents/VCP/imwe/evaluation2017/data/pc/2017pc_txt.xlsx",
    'team_txt' : "/Users/jbuss/Documents/VCP/imwe/evaluation2017/data/team/2017team_txt.xlsx",
    'questions' : "/Users/jbuss/Documents/VCP/imwe/evaluation2017/data/QuestionsConfig.xlsx",
    'output' : "/Users/jbuss/Documents/VCP/imwe/evaluation2017/data/output/"
}

@click.command()
@click.argument('pc_txt',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.argument('team_txt',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.argument('questions',
                type=click.Path(exists=True, dir_okay=False,
                                file_okay=True, readable=True)
                )
@click.option('-o', '--output', type=click.Path(exists=False, dir_okay=True))
def main(pc_txt, team_txt, questions, output):
    '''
    Script to sort and extract the comments fields from the imwe evalutaion

    Parameters:

    ===========

    PC_TXT: Path to xlsx with PC answers

    TEAM_TXT: Path to xlsx with team answers

    QUESTIONS: Path to xlsx file containing a table "Common" telling the question names
    '''

    df_pc_txt = et.io.readTxtExcelFileToDf(pc_txt)
    df_team_txt = et.io.readTxtExcelFileToDf(team_txt)
    df_questions = et.io.readConfigXlsxToDf(questions)

    # Correct pc questions
    df_pc_txt = et.tools.correctGenders(df_pc_txt)
    df_pc_txt = et.tools.definePCgroup(df_pc_txt, col_name="pc_group")

    comments = df_questions[df_questions.Type == 'Comments']

    for index, question  in comments.iterrows():
        et.io.writeCommentsToTxt(output, df_pc_txt, df_team_txt, question, groups="pc_group")

if __name__ == "__main__":
    main()
