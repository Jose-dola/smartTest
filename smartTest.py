import pandas as pd
import random
import subprocess
import os
from pypdf import PdfReader, PdfWriter

dict = {
    '-1': -1, # for managing nan
    ''  : -1, # for managing nan
    'a' : 0,
    'b' : 1,
    'c' : 2,
    'd' : 3,
    'e' : 4,
    'f' : 5,
    'g' : 6,
    'h' : 7,
    'i' : 8,
    'j' : 9,
    'k' : 10,
    'l' : 11,
    'm' : 12,
    'n' : 13,
    '1' : 0,
    '2' : 1,
    '3' : 2,
    '4' : 3,
    '5' : 4,
    '6' : 5,
    '7' : 6,
    '8' : 7,
    '9' : 8,
    '10': 9,
    '11': 10,
    '12': 11,
    '13': 12,
    '14': 13
}

## function to modify correct column of the dataframe changing a,b,c... or 0,2,3... to 0,1,2... if necessary
#def modify_row_normalizingCorrect(row):
#    row['correct'] = int(dict[str(row['correct']).strip()])
#    return row

# exam csv to dataframe
def exam_to_df(examCSV:str):
    df = pd.read_csv(examCSV,sep=';',header=None)
#    df.columns = ['question'] + ['answer ' + str(i) for i in range(len(df.columns)-2)] + ['correct']
#    df = df.apply(modify_row_normalizingCorrect, axis=1)
    df.columns = ['question'] + ['answer ' + str(i) for i in range(len(df.columns)-1)] 
    df['correct']=0
    return df 

# Function shuffle answers in the dataframe
def modify_row_shuffleAnswers(row):
    indexs = list(range(len(row)-2))
    goodIndex = row['correct']
    random.shuffle(indexs)
    newRow = row.copy()
    for i in range(len(indexs)):
        newRow['answer ' + str(i)] = row['answer ' + str(indexs[i])]
        if indexs[i] == goodIndex:
            newRow['correct'] = i
    return newRow

# Function to randomize a dataframe from a random seed
def shuffle_df(df:pd.DataFrame,randomSeed:int):
    # randomizing questions
    df = df.sample(frac=1,random_state=randomSeed)
    # randomizing answers
    random.seed(randomSeed)
    df = df.apply(modify_row_shuffleAnswers, axis=1)
    return df 

# Function to generate the latex code for an exam from:
# - numberOfquestions: number of questions
# - dataframe: pandas dataframe with the exam information
# - tex: string with the latex template,
# - format: string with the format specifications,
# - randomSeed: random seed for the shuffling process,
# using randomSeed for randomizing questions and answers
# returns the tex code as a string
def csvToTex(numberOfquestions:int, dataframe:pd.DataFrame, tex:str, format:str, randomSeed:int):
    
    # make a copy in memory of the main dataframe
    df = dataframe.copy()
 
    # shuffle questions and answers
    df = shuffle_df(df,randomSeed)
    
    # Generate latex code from dataframe rows
    questions_tex = '\n'
    n = 0
    for index, row in df.iterrows():
        if n == numberOfquestions:
            break
        n += 1
        questions_tex = questions_tex + r'\item ' + str(row['question']) + '\n' + r'\begin{enumerate}[label=\alph*)]' + '\n'
        for answer in row[1:-1]:
            questions_tex = questions_tex + r'\item ' + str(answer) + '\n'
        questions_tex = questions_tex + r'\end{enumerate}'
        questions_tex = questions_tex + '\n'
    
    # replacing formatting elements in the tex file
    for formatingItem in format:
        aux = formatingItem.split(':',1)
        element = '!!'+aux[0]
        text = aux[1].split('\n')[0]
        tex = tex.replace(element,text.strip())
    tex = tex.replace('!!CODE',str(randomSeed))
    tex = tex.replace('!!QUESTIONS',questions_tex)
    return tex

# function to run pdflatex to generate a pdf file from a latex code in a string
def textToPdf(tex:str, pdfname:str):
    # writing the output tex file
    with open('aux.tex', "w") as file:
        file.write(tex)
    # Runing pdflatex subprocess (from system)
    # Command to run pdflatex on a .tex file
    command = ["pdflatex", "-interaction=nonstopmode", "aux.tex"]
    # Running the command
    result = subprocess.run(command, capture_output=True, text=True)
#    # Output the result (stdout and stderr)
#    print("STDOUT:", result.stdout)
#    print("STDERR:", result.stderr)
#    # Check if pdflatex ran successfully
#    if result.returncode == 0:
#        print("LaTeX document compiled successfully.")
#    else:
#        print("Error in LaTeX compilation.")
    # removing all generated files but the pdf
    os.rename('aux.pdf',pdfname)
    os.remove('aux.aux')
    os.remove('aux.log')
    os.remove('aux.tex')
    return result

# function to generate a pdf file with n exams. Each exam has a random order in questions and answers.
# Input:
# - numberOfquestions: number of questions
# - n: the number of files to generate
# - examCSV: the exam csv file
# - examFormatTXT: text file with the format (headers, title, etc.)
# - templateTEX: the template latex file
def csv_to_n_exams_pdf(numberOfquestions:int, n:int, examCSV:str, examFormatTXT:str, templateTEX:str, examsPDF:str):
    # exam csv file to dataframe and normalizing correct column
    df = exam_to_df(examCSV)
    # file main.tex to string
    with open(templateTEX, 'r') as file:
        tex = file.read()
    # file examenFormat.txt to string lines
    with open(examFormatTXT, 'r') as file:
        format = file.readlines()
        format = format[1:]
    #########
    # Generating the n diferent exams
    #########
    random.seed()
    # Creates a PdfWriter object for the final file
    pdf_writer = PdfWriter()
    for i in range(n):
        texFull = csvToTex(numberOfquestions, df, tex, format, random.randint(0,999999))
        filename = 'aux.pdf'
        result = textToPdf(texFull,filename)
        if result.returncode == 0:
            # pdf genereted succesfully
            print("PDF",i+1,"generated succesfully")
        else:
            # something went wrong
            os.remove(filename) 
            raise ValueError(f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        pdf_reader = PdfReader(filename)
        # Add each page to the file PDF to the writer
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        # removing the auxiliar pdf file
        os.remove(filename) 
        #print("PDF",i+1,"generated")
    # Save the final pdf file
    with open(examsPDF, "wb") as output_pdf:
        pdf_writer.write(output_pdf)
    
############################
### CORRECTION FUNCTIONS ###
############################

# function to score penalizing for bad answers
def score_penalizing(goodAnswers, badAnswers, numberOfQuestions, numberOfAnswers):
    return 10*(goodAnswers-badAnswers/(numberOfAnswers-1))/numberOfQuestions

# function to score with no penalization for bad answers
def score_no_penalizing(goodAnswers, numberOfQuestions):
    return 10*goodAnswers/numberOfQuestions

# This function adds two columns to the answers csv file (at the begining),
# the first column is the score penalizing for bad answers
# the second column is the score without penalization
# input:
# - examCSV: exam csv file
# - answersCSV: answers csv file
# - codeColumn: the number of column where the code (random seed) is. If it is
# at the first column it should be 1, second column should be 2, and so on
# - firstAnswerColumn: the number of column where the answers start. If the first answer is
# at th first column it should be 1, etc.
# - scoredAnswersCsvFileName: desired name for the generated csv file with the scores
# the function creates a new csv file named scoredAnswersCsvFileName
def run_correction(examCSV, answersCSV, codeColumn, firstAnswerColumn, scoredAnswersCsvFileName):
    # answers csv to dataframe 
    df_answers = pd.read_csv(answersCSV, sep=',')
    df_answers = df_answers.fillna('-1')
    # exam csv to dataframe
    df_exam = exam_to_df(examCSV)
    #df_exam = smartTest.shuffle_df(df_exam, codeColumn)
    # making the correction
    scores_penal = []
    scores_no_penal = []
    numberOfGoodAnswers = []
    numberOfWrongAnswers = []
    numberOfBlankAnswers = []
    for index, row in df_answers.iterrows():
        df_exam_shuffled = shuffle_df(df_exam, int(row.iloc[codeColumn-1]))
        goodAnswers = 0
        badAnswers = 0
        i=0
        for answer in row[firstAnswerColumn-1:firstAnswerColumn-1+len(df_exam)]:
            formatedAnswer = int(dict[str(answer).strip()])
            correctAnswer  = int(df_exam_shuffled.iloc[i]['correct']) 
            if formatedAnswer != -1:
                if formatedAnswer == correctAnswer:
                    goodAnswers += 1
                else:
                    badAnswers += 1 
            i+=1
        numberOfGoodAnswers.append(goodAnswers)
        numberOfWrongAnswers.append(badAnswers)
        numberOfBlankAnswers.append(len(df_exam_shuffled)-goodAnswers-badAnswers)
        scores_penal.append(score_penalizing(goodAnswers, badAnswers, len(df_exam_shuffled), len(df_exam.columns)-2))
        scores_no_penal.append(score_no_penalizing(goodAnswers, len(df_exam_shuffled)))
    df_answers.insert(len(df_answers.columns), 'number_of_good_answers', numberOfGoodAnswers)
    df_answers.insert(len(df_answers.columns), 'number_of_wrong_answers', numberOfWrongAnswers)
    df_answers.insert(len(df_answers.columns), 'number_of_blank_answers', numberOfBlankAnswers)
    df_answers.insert(0, 'score_no_penalizing', scores_no_penal)
    df_answers.insert(0, 'score_penalizing', scores_penal)
    df_answers.to_csv(scoredAnswersCsvFileName, index=False)
    print("DONE!")

# The same as run_correction but cosidering tha the number of questions per exam is less than
# the total number of questions 
# input:
# - nquestions: number of questions per exam
# - examCSV: exam csv file
# - answersCSV: answers csv file
# - codeColumn: the number of column where the code (random seed) is. If it is
# at the first column it should be 1, second column should be 2, and so on
# - firstAnswerColumn: the number of column where the answers start. If the first answer is
# at th first column it should be 1, etc.
# - scoredAnswersCsvFileName: desired name for the generated csv file with the scores
# the function creates a new csv file named scoredAnswersCsvFileName
def run_correction_reducingNumberOfQuestionsPerExam(nquestions, examCSV, answersCSV, codeColumn, firstAnswerColumn, scoredAnswersCsvFileName):
    # answers csv to dataframe 
    df_answers = pd.read_csv(answersCSV, sep=',')
    df_answers = df_answers.fillna('-1')
    # exam csv to dataframe
    df_exam = exam_to_df(examCSV)
    #df_exam = smartTest.shuffle_df(df_exam, codeColumn)
    # making the correction
    scores_penal = []
    scores_no_penal = []
    numberOfGoodAnswers = []
    numberOfWrongAnswers = []
    numberOfBlankAnswers = []
    for index, row in df_answers.iterrows():
        df_exam_shuffled = shuffle_df(df_exam, int(row.iloc[codeColumn-1]))
        goodAnswers = 0
        badAnswers = 0
        i=0
        for answer in row[firstAnswerColumn-1:firstAnswerColumn-1+len(df_exam)]:
            formatedAnswer = int(dict[str(answer).strip()])
            correctAnswer  = int(df_exam_shuffled.iloc[i]['correct']) 
            if formatedAnswer != -1:
                if formatedAnswer == correctAnswer:
                    goodAnswers += 1
                else:
                    badAnswers += 1 
            i+=1
        numberOfGoodAnswers.append(goodAnswers)
        numberOfWrongAnswers.append(badAnswers)
        numberOfBlankAnswers.append(int(nquestions)-goodAnswers-badAnswers)
        scores_penal.append(score_penalizing(goodAnswers, badAnswers, int(nquestions), len(df_exam.columns)-2))
        scores_no_penal.append(score_no_penalizing(goodAnswers, int(nquestions)))
    df_answers.insert(len(df_answers.columns), 'number_of_good_answers', numberOfGoodAnswers)
    df_answers.insert(len(df_answers.columns), 'number_of_wrong_answers', numberOfWrongAnswers)
    df_answers.insert(len(df_answers.columns), 'number_of_blank_answers', numberOfBlankAnswers)
    df_answers.insert(0, 'score_no_penalizing', scores_no_penal)
    df_answers.insert(0, 'score_penalizing', scores_penal)
    df_answers.to_csv(scoredAnswersCsvFileName, index=False)
    print("DONE!")

# The same as run_correction_reducingNumberOfQuestionsPerExam but writing the results (scores) of each student
# in the apropiate row according to a given file
# input:
# - nquestions: number of questions per exam
# - examCSV: exam csv file (columns separated by ;)
# - answersCSV: answers csv file (columns separated by ,)
# - studentsCSV: students csv file, where the scores will be written (columns separated by ;)
# - answersCol: the column number in answersCSV file to match students between answersCSV file
# and studentsCSV file. If it is at the first column it should be 1, second column should be 2, and so on
# - studentsCol: the column number in studentsCSV file to match students between answersCSV file
# and studentsCSV file. If it is at the first column it should be 1, second column should be 2, and so on
# - codeColumn: the number of column where the code (random seed) is. If it is
# at the first column it should be 1, second column should be 2, and so on
# - firstAnswerColumn: the number of column where the answers start. If the first answer is
# at th first column it should be 1, etc.
# - scoredAnswersCsvFileName: desired name for the generated csv file with the scores
# the function creates a new csv file named scoredAnswersCsvFileName. The content and the rows order is
# according to studentsCSV file, the scores are added according to the answers given in te answersCSV file
# -1 in the scores means that the student did not do the exam, i.e., there is no answer for this student
# in the answersCSV file (no match between columnAnswers and columnStudents)
def run_correction_students_file(nquestions, examCSV, answersCSV, studentsCSV, answersCol, studentsCol, codeColumn, firstAnswerColumn, scoredAnswersCsvFileName):
    # answers csv to dataframe 
    df_answers = pd.read_csv(answersCSV, sep=',')
    df_answers = df_answers.fillna('-1')
    df_students = pd.read_csv(studentsCSV, sep=';')
    # exam csv to dataframe
    df_exam = exam_to_df(examCSV)
    # making the correction
    studentsMatchingColumn = df_students.iloc[:,studentsCol-1]
    scores_penal = [-1 for i in range(len(df_students))]
    scores_no_penal = [-1 for i in range(len(df_students))]
    numberOfGoodAnswers = [-1 for i in range(len(df_students))]
    numberOfWrongAnswers = [-1 for i in range(len(df_students))]
    numberOfBlankAnswers = [-1 for i in range(len(df_students))]
    for index, row in df_answers.iterrows():
        df_exam_shuffled = shuffle_df(df_exam, int(row.iloc[codeColumn-1]))
        goodAnswers = 0
        badAnswers = 0
        i=0
        for answer in row[firstAnswerColumn-1:firstAnswerColumn-1+len(df_exam)]:
            formatedAnswer = int(dict[str(answer).strip()])
            correctAnswer  = int(df_exam_shuffled.iloc[i]['correct']) 
            if formatedAnswer != -1:
                if formatedAnswer == correctAnswer:
                    goodAnswers += 1
                else:
                    badAnswers += 1 
            i+=1
        # finding the students in the students dataframe
        matchingCell = row.iloc[answersCol-1]
        matchingIndexList = studentsMatchingColumn.index[studentsMatchingColumn == matchingCell].to_list()
        if len(matchingIndexList) == 0:
            raise ValueError(f"There is no student equal to {matchingCell} in the students csv file")
        if len(matchingIndexList) > 1:
            raise ValueError(f"There is more than one student equal to {matchingCell} in the students csv file")
        #print(f"matchingCell: {matchingCell}")
        #print(f"matchingIndexList: {matchingIndexList}")
        #print(f"len(matchingIndexList): {len(matchingIndexList)}")
        matchingIndex =  matchingIndexList[0]
        # adding the scores
        numberOfGoodAnswers[matchingIndex] = goodAnswers
        numberOfWrongAnswers[matchingIndex] =  badAnswers
        numberOfBlankAnswers[matchingIndex] = int(nquestions)-goodAnswers-badAnswers
        scores_penal[matchingIndex] = score_penalizing(goodAnswers, badAnswers, int(nquestions), len(df_exam.columns)-2)
        scores_no_penal[matchingIndex] = score_no_penalizing(goodAnswers, int(nquestions))
    df_students.insert(len(df_students.columns), 'number_of_good_answers', numberOfGoodAnswers)
    df_students.insert(len(df_students.columns), 'number_of_wrong_answers', numberOfWrongAnswers)
    df_students.insert(len(df_students.columns), 'number_of_blank_answers', numberOfBlankAnswers)
    df_students.insert(len(df_students.columns), 'score_no_penalizing', scores_no_penal)
    df_students.insert(len(df_students.columns), 'score_penalizing', scores_penal)
    df_students.to_csv(scoredAnswersCsvFileName, sep=';', index=False)
    print("DONE!")