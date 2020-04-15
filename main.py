import glob

import TelegramConversations
from Models.Book import Book
from Models.Lesson import Lesson
from Models.Question import Question
from Models.Reading import Reading
from Models.Word import add_word, all_words
from Models.WordOccur import WordOccur


def import_data():
    prefix_path = "Files/Books/"
    book_names = glob.glob(prefix_path + "*")
    for book_name in book_names:
        Book(book_name.split('/')[-1])
        lesson_names = glob.glob(book_name + "/*")
        for lesson_name in lesson_names:
            lesson = Lesson(book_name.split('/')[-1], lesson_name.split('/')[-1])
            reading_names = glob.glob(lesson_name + "/*")
            for reading_name in reading_names:
                Reading(lesson, reading_name.split('/')[-1])
                with open(reading_name) as file:
                    for line in file:
                        word_array = line.split(';')
                        assert len(word_array) == 3
                        add_word(word_array[1], WordOccur(book_name.split('/')[-1], lesson_name.split('/')[-1],
                                                          reading_name.split('/')[-1], int(word_array[0])),
                                 [word_name.strip() for word_name in word_array[2].split(',')])


import_data()

print(Question(1, 1, ["Inside Reading 4"], ["Unit 7", "Unit 8"]).__dict__)

print(all_words['principle'].__dict__)

TelegramConversations.start_telegram_bot()
