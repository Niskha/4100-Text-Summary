#  Write a program in any language of your choice that will read a text file (or text input from keyboard).
#  The text entry/file must contain at least 500 words.


# Title: Programming Assignment
# Author: Denys Kupyna
# Date: 2/14/2024

# this is required for the program to run
import functions as func
# tkinter for GUI, obviously required
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo as si
import tkinter.messagebox
# Keep this here even though IDE says its unused, it is being used in the function.py
from tkinter import Toplevel
# global variables
spam_file_name = ""
spam = []
text_array = []


# select the file to use as spam filter, delimited by spaces
def spam_select():
    global spam
    spam.clear()
    text.delete("1.0", "end")
    filetypes = (
        ('text files', '*.txt'),
        ('all files', "*.*")
    )
    filename = fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes
    )
    if filename == "":
        si(title='File not found', message='Error: file not found')
    else:
        si(title='File Search',
           message=("Selected file:\n"+filename)
           )
    global spam_file_name
    spam_file_name = filename
    # Spam file parsing
    try:
        with open(spam_file_name, 'r') as file:
            for line in file:
                word = line.split()
                spam = spam + word
    except FileNotFoundError:
        print("File not found or not selected.")
    if spam:
        # print the contents of the spam list onto the text box and clear the spam list
        for i in reversed(range(len(spam))):
            text.insert(1.0, spam[i]+" ")
        spam.clear()


# the button to set the spam filter
def set_text_spam():
    text_contents = text.get("1.0", "end-1c")
    spam.clear()
    word = text_contents.split()
    spam.append(word)
    # logging/debugging
    print(spam)


if __name__ == '__main__':
    # Spam filter array
    spam = []
    text_array = []
    # Root window setup
    root = tkinter.Tk()
    root.resizable(True, True)
    root.geometry("900x600")
    root.title("Text Search")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Main window setup
    main = tkinter.Frame(root)
    main.grid(column=0, row=0, sticky="N,W,E,S")
    main.columnconfigure(0, weight=1)
    main.columnconfigure(1, weight=1)
    main.columnconfigure(2, weight=1)
    main.columnconfigure(3, weight=1)
    main.rowconfigure(0, weight=1)
    main.rowconfigure(1, weight=1)
    main.rowconfigure(2, weight=1)
    main.rowconfigure(3, weight=1)
    main.rowconfigure(4, weight=1)

    # spam filter file setup
    ttk.Label(main, text='Spam filter file:').grid(column=0, row=0, sticky="N")
    text = tkinter.Text(main, width=30, height=10)
    spam_button = ttk.Button(main, text='Set as spam filter', command=set_text_spam)
    spam_button.grid(column=1, row=1, sticky="NWE")
    text.grid(column=1, row=0, columnspan=2, sticky="NSWE")
    file = ttk.Button(
        main,
        text='Open File',
        command=spam_select
        )
    file.grid(column=2, row=1, sticky='NWE')

    # text file setup !!! Most of the functions for this are in the functions.py file
    ttk.Label(main, text='Text File:').grid(column=0, row=2, sticky="N")
    t_text = tkinter.Text(main, width=30, height=10)
    text_button = ttk.Button(main, text='Set as Text',
                             command=lambda: func.set_text(text_array, t_text.get("1.0", "end-1c"))
                             )
    text_button.grid(column=1, row=3, sticky="NWE")
    t_text.grid(column=1, row=2, columnspan=2, sticky="NSWE")
    t_file = ttk.Button(
        main,
        text='Open File',
        command=lambda: func.set_text_file(text_array, t_text)
    )
    t_file.grid(column=2, row=3, sticky='NWE')
    process_button = ttk.Button(main,
                                text='Process Text',
                                command=lambda: func.process_text(main, text_array, spam))
    process_button.grid(column=1, row=4, columnspan=2)

    # configure grid
    for child in main.winfo_children():
        child.grid_configure(padx=5, pady=5)

    # run app
    root.mainloop()
