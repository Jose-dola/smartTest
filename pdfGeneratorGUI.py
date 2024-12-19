#! /bin/python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import smartTest

# global variables
exam_file_path = ""
format_file_path = ""
template_file_path = ""
PDFname = ""
numberOfExams = -1

# Function to handle exam file selection
def select_exam_file():
    global exam_file_path
    aux = filedialog.askopenfilename(
        title="Select the CSV file with the exam",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    if aux:
        label_exam_file.config(text=f"Selected File: {aux}")
        exam_file_path = aux


# Function to handle the format file selection
def select_format_file():
    global format_file_path
    aux = filedialog.askopenfilename(
        title="Select the text file with the format (title, headers, etc.)",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    if aux:
        label_format_file.config(text=f"Selected File: {aux}")
        format_file_path = aux

# Function to handle the template file selection
def select_template_file():
    global template_file_path
    aux = filedialog.askopenfilename(
        title="Select the latex template file",
        filetypes=(("latex files", "*.tex"), ("All Files", "*.*"))
    )
    if aux:
        label_template_file.config(text=f"Selected File: {aux}")
        template_file_path = aux

# Function to handle the action button
def run_pdf_creation():
    try:
        smartTest.csv_to_n_exams_pdf(numberOfquestions, numberOfExams, exam_file_path, format_file_path, template_file_path, PDFname)
        messagebox.showinfo("Goodbye", "DONE!")
        runpopup.destroy()  # Close the popup
        root.destroy() # Close root window. Exit the program
    except ValueError as error:
        run_error_popup(error)

# Error window popup()
def run_error_popup(error):
    errorpopup = tk.Toplevel(root)
    errorpopup.title("Something went wrong")
    #errorpopup.geometry("300x150")
    errorpopup.grab_set() # Make the popup modal (disables interaction with main window)
    # label
    labelpopup = tk.Label(errorpopup, text='Something went wrong during the pdf creation. Find the log below.', font=("Arial", 12), padx = 10)
    labelpopup.pack(pady=20)
    # Create a Frame to contain the Text and Scrollbar
    frame = tk.Frame(errorpopup)
    frame.pack(expand=1, fill='both')
    # Create the Text widget
    text = tk.Text(frame, wrap=tk.WORD)
    text.pack(side='left', expand=1, fill='both')
    # Create the Scrollbar and link it to the Text widget
    scrollbar = tk.Scrollbar(frame, command=text.yview)
    scrollbar.pack(side='right', fill='y')
    text.config(yscrollcommand=scrollbar.set)
    # Insert long text
    text.insert(tk.END, str(error))
    # close button
    button_error_close = tk.Button(errorpopup, text="Close", font=("Arial", 12), command=errorpopup.destroy)
    button_error_close.pack(side="right", padx=20, pady=20)

# Window to verify options and run pdf creation
def run_popup():
    global exam_file_path
    global format_file_path
    global numberOfExams
    global numberOfquestions
    if entry_number.get() == "":
        messagebox.showinfo("Error","You must fill the number of exams field")
        return
    try:
        numberOfExams = int(entry_number.get())
    except ValueError:
        messagebox.showinfo("Error","You must fill the number of exams field with a valid integer number")
        return
    try:
        numberOfquestions = int(entry_number_questions.get())
    except ValueError:
        messagebox.showinfo("Error","You must fill the number of exams field with a valid integer number")
        return
    if numberOfExams <= 0:
        messagebox.showinfo("Error","You must fill the number of exams field with a valid integer number")
        return
    global PDFname
    if entry_pdf.get() == "":
        messagebox.showinfo("Error","You must fill the PDF file name field")
        return
    PDFname = entry_pdf.get() + ".pdf"
    if exam_file_path == "":
        messagebox.showinfo("Error","You must select an exam CSV file")
        return
    if format_file_path == "":
        messagebox.showinfo("Error","You must select a format file")
        return
    if template_file_path == "":
        messagebox.showinfo("Error","You must select a template file")
        return
    # Add a label with the user options
    global runpopup  # Declare popup as global so we can access it in other functions
    runpopup = tk.Toplevel(root)
    runpopup.title("Confirmation")
    #runpopup.geometry("300x150")
    runpopup.grab_set() # Make the popup modal (disables interaction with main window)
    string_labelpopup = "Your selected these options: \n\n"
    string_labelpopup += f"NUMBER OF EXAMS: {numberOfExams} \n"
    string_labelpopup += f"NUMBER OF QUESTIONS: {numberOfquestions} \n"
    string_labelpopup += f"PDF NAME: {PDFname} \n"
    string_labelpopup += f"EXAM CSV FILE PATH: {exam_file_path} \n"
    string_labelpopup += f"FORMAT TXT FILE PATH: {format_file_path} \n"
    string_labelpopup += f"LATEX TEMPLATE FILE PATH: {template_file_path} \n"
    labelpopup = tk.Label(runpopup, text=string_labelpopup, font=("Arial", 12), justify="left", padx = 10)
    labelpopup.pack(pady=20)
    # Add buttons
    button_runPdfCreation = tk.Button(runpopup, text="Run PDF creation", font=("Arial", 12), command=run_pdf_creation)
    button_runPdfCreation.pack(side="right", padx=20, pady=20)
    button_cancel = tk.Button(runpopup, text="Cancel", font=("Arial", 12), command=runpopup.destroy)
    button_cancel.pack(side="left", padx=20, pady=20)

# Create the main window
root = tk.Tk()
root.title("smart test PDF generator")
#root.geometry("400x300")  # Set the size of the window

# Label and entry for number of exams input
label_number = tk.Label(root, text="How many exams do you want? (Enter a number)", font=("Arial", 12))
label_number.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_number = tk.Entry(root, font=("Arial", 12))
entry_number.grid(row=0, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

# Label and entry for number of exams input
label_number_questions = tk.Label(root, text="How may questions per exam? (Enter a number)", font=("Arial", 12))
label_number_questions.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_number_questions = tk.Entry(root, font=("Arial", 12))
entry_number_questions.grid(row=2, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)

# Label and entry for pdf string input
label_pdf = tk.Label(root, text="Enter the desired name for the generated PDF file:", font=("Arial", 12))
label_pdf.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_pdf = tk.Entry(root, font=("Arial", 12))
entry_pdf.grid(row=4, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

# Button for exam file selection
button_exam_file = tk.Button(root, text="Select exam file", font=("Arial", 12), command=select_exam_file)
button_exam_file.grid(row=6, column=0, padx=10, pady=10, sticky="w")
# Label to display the selected file
label_exam_file = tk.Label(root, text="No file selected", font=("Arial", 10), wraplength=350, fg="gray")
label_exam_file.grid(row=6, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)

# Button for format file selection
button_format_file = tk.Button(root, text="Select format file", font=("Arial", 12), command=select_format_file)
button_format_file.grid(row=8, column=0, padx=10, pady=10, sticky="w")
# Label to display the selected file
label_format_file = tk.Label(root, text="No file selected", font=("Arial", 10), wraplength=350, fg="gray")
label_format_file.grid(row=8, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=9, column=0, columnspan=2, sticky="ew", pady=5)

# Button for template file selection
button_template_file = tk.Button(root, text="Select latex template file", font=("Arial", 12), command=select_template_file)
button_template_file.grid(row=10, column=0, padx=10, pady=10, sticky="w")
# Label to display the selected file
label_template_file = tk.Label(root, text="No file selected", font=("Arial", 10), wraplength=350, fg="gray")
label_template_file.grid(row=10, column=1, padx=10, pady=10, sticky="w")

sep = ttk.Separator(root, orient="horizontal")
sep.grid(row=11, column=0, columnspan=2, sticky="ew", pady=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.grid(row=12, column=0, columnspan=2, sticky="e")
# Button to submit the pdf string
button_run = tk.Button(button_frame, text="RUN PDF CREATION", font=("Arial", 12), command=run_popup)
button_run.grid(row=0, column=1, padx=10, pady=10, sticky="e")
# Button to exit
button_exit = tk.Button(button_frame, text="EXIT", font=("Arial", 12), command=root.destroy)
button_exit.grid(row=0, column=0, padx=10, pady=10, sticky="e")

# Run the application
root.mainloop()

