from random import random, shuffle
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from Models.Word import all_words, get_random_word

SYNONYM_QUESTION, NOT_SYNONYM_QUESTION = range(2)
SYNONYM_QUESTION_FORMAT = 'Which of the following is synonym of "{}"?'
NOT_SYNONYM_QUESTION_FORMAT = 'Which of the following is not synonym of "{}"?'

QUESTION_OPTIONS_COUNT = 4


class Question:
    def __init__(self, question_number, question_type, allowed_books, allowed_lessons):
        self.question_number = question_number
        if question_type == NOT_SYNONYM_QUESTION:
            word_name = random.choice(
                list(filter(lambda word: any(
                    (occur[0] in allowed_books and occur[1] in allowed_lessons) for occur in
                    all_words[word].occurs) and len(all_words[word].synonyms) >= QUESTION_OPTIONS_COUNT - 1,
                            list(all_words.keys()))))
            self.text = NOT_SYNONYM_QUESTION_FORMAT.format(word_name)
            shuffle(all_words[word_name].synonyms)
            self.answer = get_random_word(word_name)
            self.options = all_words[word_name].synonyms[:QUESTION_OPTIONS_COUNT - 1] + [self.answer]
        elif question_type == SYNONYM_QUESTION:
            word_name = random.choice(
                list(filter(lambda word: any(
                    (occur[0] in allowed_books and occur[1] in allowed_lessons) for occur in
                    all_words[word].occurs) and len(all_words[word].synonyms) >= 1, list(all_words.keys()))))
            self.text = SYNONYM_QUESTION_FORMAT.format(word_name)
            shuffle(all_words[word_name].synonyms)
            self.answer = all_words[word_name].synonyms[0]
            self.options = [self.answer]
            while len(self.options) < QUESTION_OPTIONS_COUNT:
                random_word = get_random_word(word_name)
                if random_word not in self.options:
                    self.options.append(random_word)
        shuffle(self.options)
        self.user_choice = None

    def get_descriptions(self):
        text = str(self.question_number) + ": " + self.text + "\n"
        i = 0
        for option in self.options:
            i += 1
            changed_option = str(chr(ord('A') + i - 1)) + ": " + option
            if option == self.answer:
                changed_option = '✅ ' + changed_option
            elif option == self.user_choice:
                changed_option = '❌ ' + changed_option
            text += changed_option + "\n"
        return text + "\n\n"

    def get_message(self):
        text = "Question number: " + str(self.question_number) + "\n\n" + self.text + "\n"
        i = 0
        reply_markdown = []
        for option in self.options:
            i += 1
            if self.user_choice == option:
                option = '✅ ' + option
            if i % 2 == 0:
                reply_markdown[-1].append(InlineKeyboardButton(text=option, callback_data='select;' + option))
            else:
                reply_markdown.append([InlineKeyboardButton(text=option, callback_data='select;' + option)])
        reply_markdown.append([InlineKeyboardButton(text='⬅️️', callback_data='prev'),
                               InlineKeyboardButton(text='➡️', callback_data='next')])
        reply_markdown.append([InlineKeyboardButton(text='Finish 🏁️', callback_data='finish')])
        return text, reply_markdown
