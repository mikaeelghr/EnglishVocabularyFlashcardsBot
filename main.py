import getopt
import glob
import os
import sys

import TelegramConversations
from Models.Book import Book
from Models.Lesson import Lesson
from Models.Reading import Reading
from Models.Word import add_word
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


def main(argv):
    proxy = ''
    bot_token = None
    try:
        opts, args = getopt.getopt(argv, "h:p:t:", ["proxy=", "token="])
    except getopt.GetoptError:
        print('main.py -p <proxy> -t <bot_token>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: main.py -p <proxy> -t <bot_token>\nexample: python3 main.py '
                  '-p http://127.0.0.1:37864/ -t 270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0')
            sys.exit()
        elif opt in ("-p", "--proxy"):
            proxy = arg
        elif opt in ("-t", "--token"):
            bot_token = arg
    if bot_token is None:
        print('bot token is necessary,\n'
              'usage: main.py -p <proxy> -t <bot_token>\nexample: python3 main.py '
              '-p http://127.0.0.1:37864/ -t 270485614:AAHfiqksKZ8WmR2zSjiQ7_v4TMAKdiHm9T0')
        sys.exit(2)

    if proxy is not None:
        os.environ['http_proxy'] = proxy
        os.environ['HTTP_PROXY'] = proxy
        os.environ['https_proxy'] = proxy
        os.environ['HTTPS_PROXY'] = proxy

    import_data()

    TelegramConversations.start_telegram_bot(bot_token)


if __name__ == "__main__":
    main(sys.argv[1:])
