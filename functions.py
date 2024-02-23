#  Write a program in any language of your choice that will read a text file (or text input from keyboard).
#  The text entry/file must contain at least 500 words.


# Title: Programming Assignment
# Author: Denys Kupyna
# Date: 2/14/2024
import Programming_Assignment as p

text_file_name = ''
raw_array = []


def error_box(string):
    p.tkinter.messagebox.showerror(title='Error', message=string)


def set_text(array, t_text):
    # set text logic
    word = t_text.split()
    raw_array.clear()
    raw_array.append(t_text)
    array.append(word)
    wc = word_count(array)
    # if word count is below 500 send an error box and empty the array
    if wc < 500:
        error_box("Word count must be above 500\nCurrent word count: " + str(wc))
        array.clear()
    # logging/debugging
    print("Clean array:\t")
    print(array)
    print("Raw array:\t")
    print(raw_array)

def set_text_file(array, t_text):
    # file io for setting text
    array.clear()
    t_text.delete('1.0', 'end')
    filetypes = (
        ('text files', '*.txt'),
        ('all files', "*.*")
    )
    filename = p.fd.askopenfilename(
        title='Open file',
        initialdir='/',
        filetypes=filetypes
    )
    if filename == "":
        p.si(title='File not found', message='Error: file not found')
    else:
        p.si(title='File Search',
             message=("Selected file:\n" + filename)
             )
    global text_file_name
    text_file_name = filename
    try:
        with open(text_file_name, 'r') as file:
            for line in file:
                word = line.split()
                array = array + word
                global raw_array
                raw_array.append(line)
    except FileNotFoundError:
        print("File not found or not selected.")
    if array:
        for i in reversed(range(len(array))):
            t_text.insert(1.0, array[i]+" ")


# returns an int
def word_count(array):
    wordcount = 0
    if array[0]:
        wordcount = len(array[0])
    return wordcount


# returns an int
def count_whitespace(array):
    count = 0
    for line in array:
        count = count + line.count(" ")
    return count


# returns an int
def count_sentence(array):
    count = 0
    for line in array:
        count += line.count(". ")
    return count


# returns a dict
def stop_words(array):
    stop_words = {'the': 0, 'a': 0, 'some': 0, 'by': 0, 'any': 0, 'or': 0, 'and': 0}
    for key in stop_words:
        stop_words[key] = array[0].count(key)
    return stop_words


# returns a dict of spam words and their occurrences
def find_spam(array, spam_array):
    spam_dicts = {}
    # create a dict for every spam word in order to be able to get counts of every word
    for word in spam_array[0]:
        spam_dicts[word] = array[0].count(word)
    return spam_dicts


def spam_warning(spam_dict):
    for word in spam_dict:
        print(word)
        print(spam_dict[word])
        if spam_dict[word] > 0:

            return True


def process_text(parent, array, spam_array):
    # Check if spam has been set
    if not spam_array:
        error_box("The spam filter must have an entry and be set.")
        return
    if not array:
        error_box("The text box must have a valid entry and be set.")
        return
    # Open new window
    info = p.Toplevel(parent)
    info.geometry("300x600")
    info.title("Process results")

    # Whitespace Count
    whitespace = p.ttk.Label(info, text="Whitespaces:\t"+str(count_whitespace(raw_array)))
    whitespace.pack()
    # Sentence Count
    sentence = p.ttk.Label(info, text="Sentence Count:\t"+str(count_sentence(raw_array)))
    sentence.pack()
    # Stop Words
    p.ttk.Label(info, text="Stop Words:").pack()
    stopwords = stop_words(array)
    for word in stopwords:
        p.ttk.Label(info, text=str(word)+": "+str(stopwords[word])).pack()
    # Spam Words
    p.ttk.Label(info, text='Spam Words:').pack()
    spamwords = find_spam(array, spam_array)
    for word in spamwords:
        p.ttk.Label(info, text=str(word)+": "+str(spamwords[word])).pack()
    print(spam_warning(spamwords))
    if spam_warning(spamwords):
        p.ttk.Label(info, text="Spam filter triggered. Possible Spam.").pack()
    info.mainloop()
