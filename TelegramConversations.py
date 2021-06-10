import copy
import logging
from random import randrange


from Models.Book import get_books
from Models.Question import Question
from Models.Word import all_words, dictionary, Word, add_word, get_words

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

# Enable logging
from Models.Lesson import all_lessons, get_lessons

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, SELECT_BOOKS, SELECT_LESSONS, IN_MESSAGES = range(4)
START_A_NEW_QUIZ_MESSAGE = 'Start a new Quiz ✏️'
SHOW_ME_THE_FLASH_CARDS = 'Show me the flashcards 🎴'
ALL_BOOKS = 'All books'
ALL_UNITS = 'All units'
PROBLEMS_COUNT = 25
QUIZ_STARTED = 'Quiz started\n\nSend /cancel to start again'
FLASHCARDS_STARTED = 'Here is your flashcards\nSend /cancel to start again'


def start(update, context):
    keys = copy.deepcopy(list(context.user_data.keys()))
    for key in keys:
        del context.user_data[key]
    if update.message.text == START_A_NEW_QUIZ_MESSAGE or update.message.text == SHOW_ME_THE_FLASH_CARDS:
        context.user_data['choice'] = update.message.text
        reply_keyboard = []
        for book_name in get_books():
            reply_keyboard.append([book_name])
        reply_keyboard.append([ALL_BOOKS])
        update.message.reply_text(
            "Select the books",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SELECT_BOOKS

    reply_keyboard = [[START_A_NEW_QUIZ_MESSAGE, SHOW_ME_THE_FLASH_CARDS]]

    update.message.reply_text(
        "Hey,\n" +
        "Using this bot, you can easily memorize new words " +
        "by different methods such as flash cards and multiple choice quizzes,",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return START


def select_books(update, context):
    reply_keyboard = []
    if update.message.text == ALL_BOOKS:
        context.user_data['books'] = get_books()
    else:
        context.user_data['books'] = [update.message.text]
    for lesson_name in get_lessons(context.user_data['books']):
        reply_keyboard.append([lesson_name])
    reply_keyboard.append([ALL_UNITS])

    user = update.message.from_user
    logger.info("select_books of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Select the units',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SELECT_LESSONS


def select_lessons(update, context):
    if update.message.text == ALL_UNITS:
        context.user_data['units'] = get_lessons(context.user_data['books'])
    else:
        context.user_data['units'] = [update.message.text]

    context.user_data['current_mid'] = 0
    context.user_data['messages'] = []
    if context.user_data['choice'] == START_A_NEW_QUIZ_MESSAGE:
        for i in range(0, PROBLEMS_COUNT):
            context.user_data['messages'].append(
                Question(i + 1, randrange(0, 2), context.user_data['books'], context.user_data['units']))
        update.message.reply_text(text=QUIZ_STARTED, reply_markup=ReplyKeyboardRemove())
    elif context.user_data['choice'] == SHOW_ME_THE_FLASH_CARDS:
        for word_name in get_words(context.user_data['books'], context.user_data['units']):
            context.user_data['messages'].append(all_words[word_name])
        update.message.reply_text(text=FLASHCARDS_STARTED, reply_markup=ReplyKeyboardRemove())
    else:
        return error(update, context)
    user = update.message.from_user
    logger.info("select_lessons of %s: %s", user.first_name, update.message.text)

    text, reply_markdown = context.user_data['messages'][context.user_data['current_mid']].get_message()
    update.message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(reply_markdown))

    return IN_MESSAGES


def edit_selection(update, context):
    text = update.callback_query.data
    context.user_data['messages'][context.user_data['current_mid']].user_choice = text.split(';')[1]
    text, reply_markdown = context.user_data['messages'][context.user_data['current_mid']].get_message()
    query = update.callback_query
    query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(reply_markdown))


def iterate_message(update, context):
    text = update.callback_query.data
    if text == 'next':
        context.user_data['current_mid'] += 1
    else:
        context.user_data['current_mid'] -= 1
    text, reply_markdown = context.user_data['messages'][context.user_data['current_mid']].get_message()
    query = update.callback_query
    query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(reply_markdown))


def finish_message(update, context):
    score = 0
    text = ""
    for question in context.user_data['messages']:
        if question.user_choice == question.answer:
            score += 4
        elif question.user_choice is not None:
            score -= 1
        text = text + question.get_descriptions()
    text = "your final score: " + str(score) + "\n\nquestions:\n\n" + text + "\n\n\n send /start to start again"
    query = update.callback_query
    query.edit_message_text(text=text, reply_markup=None)
    return START


def show_meaning(update, context):
    text = update.message.text.lower()
    if text not in all_words and text in dictionary:
        add_word(text)
    if text in all_words:
        update.message.reply_text(all_words[text].get_descriptions())
    else:
        update.message.reply_text("can't find such word in dictionary")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def start_telegram_bot(bot_token):
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conversation_handler = ConversationHandler(
        per_user=True,
        entry_points=[CommandHandler('start', start), MessageHandler(
            Filters.regex('^(' + START_A_NEW_QUIZ_MESSAGE + '|' + SHOW_ME_THE_FLASH_CARDS + ')$'), start)],

        states={
            START: [
                CommandHandler('start', start),
                MessageHandler(
                    Filters.regex('^(' + START_A_NEW_QUIZ_MESSAGE + '|' + SHOW_ME_THE_FLASH_CARDS + ')$'),
                    start), MessageHandler(Filters.all, show_meaning)
            ],

            SELECT_BOOKS: [
                MessageHandler(Filters.regex('^(' + ALL_BOOKS + '|' + '|'.join(get_books()) + ')$'), select_books),
                CommandHandler('cancel', start), MessageHandler(Filters.all, show_meaning)],

            SELECT_LESSONS: [
                MessageHandler(Filters.regex('^(' + ALL_UNITS + '|' + '|'.join(get_lessons(get_books())) + ')$'),
                               select_lessons),
                CommandHandler('cancel', start), MessageHandler(Filters.all, show_meaning)],

            IN_MESSAGES: [
                CallbackQueryHandler(edit_selection, pattern='^(select;.*)$'),
                CallbackQueryHandler(iterate_message, pattern='^(next|prev)$'),
                CallbackQueryHandler(finish_message, pattern='^(finish)$'),
                CommandHandler('cancel', start), MessageHandler(Filters.all, show_meaning)],
        },

        fallbacks=[CommandHandler('cancel', start)]
    )

    dp.add_handler(conversation_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
