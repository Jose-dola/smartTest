#! /bin/python3

import smartTest

examCSV = str(input("give me the name of the exam csv file (the same which was used with de pdfGenerator):\n")).strip()
nquestions = str(input("give me the number of questions per exam:\n")).strip()
answersCSV = str(input("give me the name of the answers csv file:\n")).strip()
studentsCSV = str(input("give me the name of the students csv file:\n")).strip()
answersCol = int(input("give me the column number in the answers CSV file for matching answers and students csv tables. First column should be 1, second column should 2 and so on:\n"))
studentsCol = int(input("give me the column number in the students CSV file for matching answers and students csv tables. First column should be 1, second column should 2 and so on:\n"))
scoredAnswersCSV = str(input("give me the name that you wish for the CSV file generated by this program with the scores:\n")).strip()
codeColumn = int(input("give me the column number of the exam code. First column should be 1, second column should 2 and so on:\n"))
firstAnswersColumn = int(input("give me the column number of the first answers. First column should be 1, second column should 2 and so on:\n"))
smartTest.run_correction_students_file(nquestions, examCSV, answersCSV, studentsCSV, answersCol, studentsCol, codeColumn, firstAnswersColumn, scoredAnswersCSV)
