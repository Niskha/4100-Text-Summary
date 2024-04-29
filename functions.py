"""
Functions for Text Summary App
"""
from scipy.stats import norm
import math


# Load the common words file list
def load_common_words(file_path):
    # Load common words from a file into a set
    with open(file_path, 'r') as file:
        common_words = {line.strip().lower() for line in file}
    return common_words


# Load the text file to be analyzed
def load_text_file(file_path):
    # Read the content of the text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


# Count the words in the text file
def count_words(text):
    # Split the text into words using whitespace as delimiter
    words = text.split()
    return len(words)


# Count the paragraphs in the text file
def count_paragraphs(text):
    # Split the text into paragraphs based on blank lines
    paragraphs = text.split('\n\n')
    # Filter out empty paragraphs that might occur from consecutive blank lines
    paragraphs = [para for para in paragraphs if para.strip()]
    return len(paragraphs)


# Use the count_words() and count_paragraphs() functions on a specific file
def analyze_text_file(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    # Count words and paragraphs
    word_count = count_words(text)
    paragraph_count = count_paragraphs(text)

    return word_count, paragraph_count


# Count the hits of the text file to the wordlists, used in calculate_language_score()
def count_matches(text, wordlist):
    # Split the text into words
    words = text.lower().split()
    # Count words that match any in the wordlist
    return sum(1 for word in words if word in wordlist)


# Determine the language. This is done by calculating
# english_count(for every word in the text that matches the english wordlist this is incremented)/known_word_count
# (words that are in either language lists) same for spanish_score/known_word_count, whichever is greater is selected
# as the language of the text
def calculate_language_score(text, english_words, spanish_words):
    # Count English and Spanish matches
    english_count = count_matches(text, english_words)
    spanish_count = count_matches(text, spanish_words)

    # Calculate known word count
    known_word_count = english_count + spanish_count

    # If there are no known words, can't determine
    if known_word_count == 0:
        return -1, 0, 0, 0

    # Calculate scores
    english_score = english_count / known_word_count
    spanish_score = spanish_count / known_word_count

    # Determine which score is greater
    if english_score > spanish_score:
        return 0, english_score, spanish_score, known_word_count
    elif spanish_score > english_score:
        return 1, english_score, spanish_score, known_word_count
    else:
        return -1, english_score, spanish_score, known_word_count


# Calculate the confidence intervals for
def wilson_confidence_interval(p, n, confidence_level=0.95):
    # Calculate z-score for the given confidence level
    z = norm.ppf((1 + confidence_level) / 2)

    # Wilson's formula
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator

    lower_bound = center - margin
    upper_bound = center + margin

    return lower_bound, upper_bound


def calculate_confidence_intervals(english_score, spanish_score, known_word_count, confidence_level=0.95):
    # Calculate confidence intervals for English and Spanish scores
    english_ci = wilson_confidence_interval(english_score, known_word_count, confidence_level)
    spanish_ci = wilson_confidence_interval(spanish_score, known_word_count, confidence_level)

    return english_ci, spanish_ci


def confidence(english_ci, spanish_ci):
    e_conf = int(((english_ci[0] + english_ci[1]) / 2) * 100)
    s_conf = int(((spanish_ci[0] + spanish_ci[1]) / 2) * 100)
    return e_conf, s_conf

