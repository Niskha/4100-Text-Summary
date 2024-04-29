"""
Write a program that takes in a text file and identify (a) number of words (b) number of
paragraphs. Your program should be able to determine if the text file was in English or
Spanish
"""

# Title: Text Summary
# Author: Denys Kupyna, Caroline Warner, Maryam Simpson
# Date: 4/28/2024

import functions as func
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox



class TextSummaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Class Variables
        self.file_path = None
        self.word_count = 0
        self.paragraph_count = 0
        self.language = None
        self.eng_conf = 0
        self.spa_conf = 0
        # Create Main GUI
        self.title("Text Summary")
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        # Set window size and location
        self.geometry(f"{int(width/2)}x{int(height/2)}+{int(width/4)}+{int(height/4)}")

        # Set window color
        self.configure(bg="#2e2e2e")

        # Create File Name Label
        self.file_path_label = tk.Label(self, text=str(self.file_path), bg="#2e2e2e", fg="white")
        self.file_path_label.pack(padx=5, pady=(int(height/8), 5))

        # Create File Selector
        file_button = tk.Button(self, text="Select Text File", command=self.file_select)
        file_button.pack(side='top')

        # Create Analyze Button
        self.analyze_button = tk.Button(self, text="Analyze Text", command=self.analyze_text, state="disabled")
        self.analyze_button.pack(side='top', pady=5)

        # Create Statistics Labels
        self.word_count_label = tk.Label(self, text="Word Count: " + str(self.word_count), bg="#2e2e2e", fg="white")
        self.word_count_label.pack(side="top", pady=(20, 5))
        self.paragraph_count_label = tk.Label(self, text="Paragraph Count: " + str(self.paragraph_count), bg="#2e2e2e", fg="white")
        self.paragraph_count_label.pack(side="top", pady=5)
        self.language_label = tk.Label(self, text="Language: " + str(self.language), bg="#2e2e2e", fg="white")
        self.language_label.pack(side="top", pady=5)
        self.english_confidence_label = tk.Label(self, text=f"English Confidence: {str(self.eng_conf)}%", bg="#2e2e2e", fg="white")
        self.english_confidence_label.pack(side="top", pady=5)
        self.spanish_confidence_label = tk.Label(self, text=f"Spanish Confidence: {str(self.spa_conf)}%", bg="#2e2e2e", fg="white")
        self.spanish_confidence_label.pack(side="top", pady=5)

    def file_select(self):
        # Open file dialog to select a file
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not self.file_path:
            self.analyze_button.config(state="disabled")
            return  # User canceled
        self.file_path_label.config(text=str(self.file_path))
        # Enable the analyze button
        self.analyze_button.config(state="normal")
    def analyze_text(self):

        english_wordlist = func.load_common_words("english_top1k.txt")
        spanish_wordlist = func.load_common_words("spanish_top1k.txt")
        language, eng_score, spa_score, known_word_count = func.calculate_language_score(func.load_text_file(
            self.file_path), english_wordlist, spanish_wordlist)
        try:
            eng_confidence, spanish_confidence = func.calculate_confidence_intervals(eng_score, spa_score,
                                                                                     known_word_count)
            self.eng_conf, self.spa_conf = func.confidence(eng_confidence, spanish_confidence)
        except ZeroDivisionError as e:
            self.eng_conf = 0
            self.spa_conf = 0
            tk.messagebox.showerror(title="ZeroDivisionError", message=f"{e}\nMaybe no words were recognized?"
                                                                       f" Try a more varied text file.")



        self.word_count, self.paragraph_count = func.analyze_text_file(self.file_path)
        if language == 0:
            self.language = "English"
        elif language == 1:
            self.language = "Spanish"
        elif language == -1:
            self.language = "Error Determining Language"

        # Update labels with new values
        self.word_count_label.config(text="Word Count: " + str(self.word_count))
        self.paragraph_count_label.config(text="Paragraph Count: " + str(self.paragraph_count))
        self.language_label.config(text="Language: " + str(self.language))
        self.english_confidence_label.config(text=f"English Confidence: {self.eng_conf}%")
        self.spanish_confidence_label.config(text=f"Spanish Confidence: {self.spa_conf}%")


if __name__ == '__main__':
    app = TextSummaryApp()
    app.mainloop()
    pass
