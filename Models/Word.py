import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Models.WordOccur import WordOccur
import csv
import sys

all_words = {}
dictionary = {}

csv.field_size_limit(sys.maxsize)
with open('Files/dictionary.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    for row in reader:
        if row[0].lower() in dictionary:
            dictionary[row[0].lower()].append(row[1])
        else:
            dictionary[row[0].lower()] = [row[1]]


def add_word(name, occur=None, synonyms=None):
    if synonyms is None:
        synonyms = []
    if name not in all_words:
        meanings = []
        if name.lower() in dictionary:
            meanings = dictionary[name.lower()]
        Word(name, meanings, synonyms)
    if occur is not None:
        all_words[name].occurs.add(occur.get_tuple())


def get_random_word(not_synonym_with=None):
    forbidden_list = []
    if not_synonym_with is not None:
        forbidden_list = [not_synonym_with] + all_words[not_synonym_with].synonyms
    name = random.choice(list(filter(lambda word_name: word_name not in forbidden_list, list(all_words.keys()))))
    return name


def get_words(books, lessons):
    return list(
        filter(lambda word_name: any((oc[0] in books and oc[1]) in lessons for oc in all_words[word_name].occurs),
               list(all_words.keys())))


class Word:
    def __init__(self, name, meanings, synonyms):
        self.name = name
        self.meanings = meanings
        self.synonyms = synonyms
        self.occurs = set()  # type: {tuple}
        all_words[name] = self

    def get_descriptions(self):
        text = self.name + "\n\n"
        if len(self.meanings) > 0:
            text += 'meanings:\n' + ', '.join(self.meanings) + '\n\n'
        if len(self.synonyms) > 0:
            text += 'synonyms:\n' + ', '.join(self.synonyms) + "\n\n"
        if len(self.occurs) > 0:
            text += 'occurs:\n' + '\n'.join([' -> '.join(x) for x in self.occurs]) + "\n"
        return text

    def get_message(self):
        text = self.get_descriptions()
        return text, [[InlineKeyboardButton(text='⬅️️', callback_data='prev'),
                      InlineKeyboardButton(text='➡️', callback_data='next')]]
