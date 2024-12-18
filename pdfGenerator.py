#! /bin/python3

import smartTest

n = int(input("How many exams do you want? \n"))
try:
  smartTest.csv_to_n_exams_pdf(n, 'exam.csv', 'examFormat.txt', 'template.tex', 'exams.pdf')
except ValueError as error:
  print(error,"\n\nSOMETHING WENT WRONG. See the log above")
exit()
