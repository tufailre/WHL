from lessons import *
import lessons
import telebot
from telebot import types
import sqlite3
from lessons import add
from keyboa import Keyboa




bot = telebot.TeleBot('5681429877:AAF3G38XJRR2mTYPJJzAQwFh1F4mj4ax-Bk')

lessons_db = sqlite3.connect("lessons.db")
cur = lessons_db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS lessons(name TEXT, id TEXT)""")

current_lesson = ""
current_word = ""
current_translation = ""


# print(get_translation("Pensare"))
@bot.message_handler(commands=["start"], content_types=["text"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
    settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
    new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
    timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
    help = types.KeyboardButton("❓ПОМОЩЬ❓")
    markup.row(lessons_show, settings)
    markup.row(new_lesson)
    markup.row(timer, help)
    bot.send_message(message.chat.id, text="WLH bot", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def func(message):
    if message.text == "🔙В ГЛАВНОЕ МЕНЮ🔙":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
        settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
        new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
        timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(lessons_show, settings)
        markup.row(new_lesson)
        markup.row(timer, help)
        bot.send_message(message.chat.id, text="Main menu", reply_markup=markup)

    if message.text == "📚ПРОСМОТРЕТЬ УРОКИ📚":
        all_lessons = get_all_lessons(message.chat.id)
        if len(all_lessons) != 0:
            keyboard = Keyboa(items=all_lessons, front_marker="", back_marker="")
            bot.send_message(message.chat.id, "🗒ВАШИ УРОКИ🗒", reply_markup=keyboard())
            bot.send_message(message.chat.id, "Нажмите на нужный вам урок, что бы начать выполнение или изменить его")
            # bot.register_next_step_handler(msg, creating_new_lesson)
        else:
            bot.send_message(message.chat.id, "У вас нет ни одного урока")

    if message.text == "➕СОЗДАТЬ НОВЫЙ УРОК➕":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        cancel = types.KeyboardButton("❌ОТМЕНА❌")
        markup.add(cancel)
        msg = bot.send_message(message.chat.id, 'Введите название', reply_markup=markup)
        bot.register_next_step_handler(msg, creating_new_lesson)

    if message.text == "🛠НАСТРОЙКИ🛠":
        bot.send_message(message.chat.id, "Настроек пока нет ( ")

    if message.text == "ПОСТАВИТЬ ТАЙМЕР":
        bot.send_message(message.chat.id, "Таймера пока нет ( ")

    if message.text == "❓ПОМОЩЬ❓":
        keyboard = types.InlineKeyboardMarkup()

        helpbtn = types.InlineKeyboardButton(text="Амир", url="tg://user?id=520110611")
        keyboard.add(helpbtn)
        bot.send_message(message.chat.id, text="По всем вопросом сюда", reply_markup=keyboard)
    if message.text == "❌УДАЛИТЬ СЛОВО❌":
        delete_word(current_word, current_lesson, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lesson_delete = types.KeyboardButton("❌УДАЛИТЬ СЛОВО❌")
        add_a_word = types.KeyboardButton("➕ДОБАВИТЬ СЛОВО➕")
        main_menu = types.KeyboardButton("🔙В ГЛАВНОЕ МЕНЮ🔙")
        markup.row(add_a_word, lesson_delete)
        markup.row(main_menu)
        bot.send_message(message.chat.id, f'❌Слово успешно удалено!❌\nСЛОВО: \t{current_word} - {current_translation}',
                         reply_markup=markup)
    if message.text == "➕ДОБАВИТЬ СЛОВО➕":
        msg = bot.send_message(message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(msg, word_add_word)
    if message.text == "📚ПРОСМОТРЕТЬ УРОК📚":
        all_words1 = get_all_words_in_lesson(current_lesson, message.chat.id)
        all_words = []
        for i in all_words1:
            a = get_translation(i, message.chat.id)
            i += f" - {a}"
            all_words.append(i)
        print(all_words)
        if len(all_words) != 0:
            keyboard = Keyboa(items=all_words, front_marker="", back_marker="")
            bot.send_message(message.chat.id, f"🗒УРОК: {current_lesson}", reply_markup=keyboard())
            #bot.send_message(message.chat.id, "Нажмите на нужное вам слово, что бы удалить его")
            # bot.register_next_step_handler(msg, creating_new_lesson)
        else:
            bot.send_message(message.chat.id, f"У вас нет ни одного слова в уроке {current_lesson}")


def creating_new_lesson(name):
    global current_lesson
    all = get_all_lessons(name.chat.id)
    if name.text in all:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
        settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
        new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
        timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(lessons_show, settings)
        markup.row(new_lesson)
        markup.row(timer, help)
        bot.send_message(name.chat.id, "Урок с таким именем уже существует, попробуйте создать урок еще раз",
                         reply_markup=markup)
    elif name.text == "❌ОТМЕНА❌":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
        settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
        new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
        timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(lessons_show, settings)
        markup.row(new_lesson)
        markup.row(timer, help)
        bot.send_message(name.chat.id, "✅ДЕЙСТВИЕ ОТМЕНЕНО✅",
                         reply_markup=markup)
    else:
        lessons.add(name.text, name.chat.id)
        current_lesson = name.text
        print(name.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lesson_delete = types.KeyboardButton("❌УДАЛИТЬ УРОК❌")
        add_a_word = types.KeyboardButton("➕ДОБАВИТЬ СЛОВО➕")
        main_menu = types.KeyboardButton("🔙В ГЛАВНОЕ МЕНЮ🔙")
        # timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        # help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(add_a_word, lesson_delete)
        markup.row(main_menu)
        # markup.row(timer, help)
        msg = bot.send_message(name.chat.id, f'✅Имя успешно задано!✅\nУРОК: \t{name.text}', reply_markup=markup)
        bot.register_next_step_handler(msg, inlesson)


def inlesson(message):
    if message.text == "❌УДАЛИТЬ УРОК❌":
        delete_lesson(current_lesson, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
        settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
        new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
        timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(lessons_show, settings)
        markup.row(new_lesson)
        markup.row(timer, help)
        bot.send_message(message.chat.id, f'❌Урок успешно удален!❌\nУРОК: \t{current_lesson}',
                         reply_markup=markup)
    if message.text == "➕ДОБАВИТЬ СЛОВО➕":
        msg = bot.send_message(message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(msg, word_add_word)
    if message.text == "🔙В ГЛАВНОЕ МЕНЮ🔙":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lessons_show = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОКИ📚")
        settings = types.KeyboardButton("🛠НАСТРОЙКИ🛠")
        new_lesson = types.KeyboardButton("➕СОЗДАТЬ НОВЫЙ УРОК➕")
        timer = types.KeyboardButton("ПОСТАВИТЬ ТАЙМЕР")
        help = types.KeyboardButton("❓ПОМОЩЬ❓")
        markup.row(lessons_show, settings)
        markup.row(new_lesson)
        markup.row(timer, help)
        bot.send_message(message.chat.id, text="Main menu", reply_markup=markup)


def word_add_word(message):
    global current_word
    current_word = message.text
    msg = bot.send_message(message.chat.id, 'Введите перевод слова:')
    bot.register_next_step_handler(msg, word_add_trans)


def word_add_trans(message):
    global current_translation
    current_translation = message.text
    add_word(current_lesson, current_word, current_translation, message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lesson_delete = types.KeyboardButton("❌УДАЛИТЬ СЛОВО❌")
    add_a_word = types.KeyboardButton("➕ДОБАВИТЬ СЛОВО➕")
    main_menu = types.KeyboardButton("🔙В ГЛАВНОЕ МЕНЮ🔙")
    markup.row(add_a_word, lesson_delete)
    markup.row(main_menu)
    bot.send_message(message.chat.id, f'✅Слово успешно добавлено!✅\n{current_word} - {current_translation}',
                     reply_markup=markup)
    if message.text == "❌УДАЛИТЬ СЛОВО❌":
        delete_word(current_word, current_lesson, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lesson_delete = types.KeyboardButton("❌УДАЛИТЬ СЛОВО❌")
        add_a_word = types.KeyboardButton("➕ДОБАВИТЬ СЛОВО➕")
        main_menu = types.KeyboardButton("🔙В ГЛАВНОЕ МЕНЮ🔙")
        markup.row(add_a_word, lesson_delete)
        markup.row(main_menu)
        bot.send_message(message.chat.id, f'❌Слово успешно удалено!❌\nСЛОВО: \t{current_word} - {current_translation}',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def lesson_opening(call):
    global current_lesson
    if call.message:
        # call.data
        current_lesson = call.data
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #lesson_delete = types.KeyboardButton("❌УДАЛИТЬ УРОК❌")
        lesson_change = types.KeyboardButton("📚ПРОСМОТРЕТЬ УРОК📚")
        add_a_word = types.KeyboardButton("➕ДОБАВИТЬ СЛОВО➕")
        #start_lesson = types.KeyboardButton("НАЧАТЬ ВЫПОЛНЕНИЕ")
        main_menu = types.KeyboardButton("🔙В ГЛАВНОЕ МЕНЮ🔙")
        markup.row(add_a_word, lesson_change)
        #markup.row(start_lesson)
        markup.row(main_menu)
        #markup.row(lesson_delete, main_menu)
        bot.send_message(call.message.chat.id, f'УРОК: \t{current_lesson}',
                         reply_markup=markup)
        print("DADADADRTDrtDRDRTDRTDTRA")


bot.polling(none_stop=True)
