import random
import webbrowser
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from django.conf import settings

answers = ['Я не понял, что ты хочешь сказать.', 'Извини, я тебя не понимаю.', 'Я не знаю такой команды.',
           'Мой разработчик не говорил, что отвечать в такой ситуации... >_<']

bot = AsyncTeleBot(settings.TOKEN_BOT)

@bot.message_handler(commands=['start'])
async def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🛍 Каталог пицц')
    button2 = types.KeyboardButton('⚙️ Настройки')
    button3 = types.KeyboardButton('📄 Справка')
    button4 = types.KeyboardButton('🗑 Корзина')
    markup.row(button1, button4)
    markup.row(button2, button3)

    if message.text == '/start':
        await bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! У меня ты сможешь купить '
                                                f'пиццу!', reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, 'Перекинул тебя в главном меню! Выбирай!', reply_markup=markup)


@bot.message_handler(content_types='photo')
async def get_photo(message):
    await bot.send_message(message.chat.id, 'У меня нет возможности просматривать фото :(')


@bot.message_handler()
async def info(message):
    if message.text == '🛍 Каталог пицц':
        await goodsChapter(message)
    elif message.text == '⚙️ Настройки':
        await settingsChapter(message)
    elif message.text == '📄 Справка':
        await infoChapter(message)
    elif message.text == '🔹 Пепперони':
        await pepperoni_pizza(message)
    elif message.text == 'Изменить размер':
        await infoSize(message)
    elif message.text == '🔹 Гавайская':
        await gavaii_pizza(message)
    elif message.text == 'Изменить размер':
        await infoSize(message)
    elif message.text == '🔹 Цыпленок кари':
        await chicken_kari_pizza(message)
    elif message.text == 'Изменить размер':
        await infoSize(message)
    elif message.text == '🔹 Бургер-пицца':
        await burger_pizza(message)
    elif message.text == 'Изменить размер':
        await infoSize(message)
    elif message.text == '25 сантиметров' or message.text == '30 сантиметров' or message.text == '35 сантиметров':
        await bot.send_message(message.chat.id, 'Размер вашей пиццы изменен :)')
    elif message.text == '⚙️ Настройки #1':
        await bot.send_message(message.chat.id, 'Настройки номер 1...')
    elif message.text == '⚙️ Настройки #2':
        await bot.send_message(message.chat.id, 'Настройки номер 2...')
    # elif message.text == '💳 Добавить в корзину'
    #     await pass
    elif message.text == '✏️ Написать разработчику':
        webbrowser.open('https://t.me/IDOL2k')
    elif message.text == '↩️ Назад':
        await goodsChapter(message)
    elif message.text == '↩️ Назад в меню':
        await welcome(message)
    else:
        await bot.send_message(message.chat.id, answers[random.randint(0, 3)])


async def goodsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('🔹 Пепперони')
    button2 = types.KeyboardButton('🔹 Гавайская')
    button3 = types.KeyboardButton('🔹 Цыпленок кари')
    button4 = types.KeyboardButton('🔹 Бургер-пицца')
    button5 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)

    await bot.send_message(message.chat.id, 'Вот все товары, которые сейчас находятся в продаже:', reply_markup=markup)


async def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('⚙️ Настройки #1')
    button2 = types.KeyboardButton('⚙️ Настройки #2')
    button3 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)
    markup.row(button3)

    await bot.send_message(message.chat.id, 'Раздел настроек. Выбери один из вариантов:', reply_markup=markup)


async def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('✏️ Написать разработчику')
    button2 = types.KeyboardButton('↩️ Назад в меню')
    markup.row(button1, button2)

    await bot.send_message(message.chat.id, 'Раздел справки. Здесь ты можешь написать моему разработчику.',
                           reply_markup=markup)


async def infoSize(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('25 сантиметров')
    button2 = types.KeyboardButton('30 сантиметров')
    button3 = types.KeyboardButton('35 сантиметров')
    button4 = types.KeyboardButton('↩️ Назад')
    markup.row(button1, button2)
    markup.row(button3, button4)

    await bot.send_message(message.chat.id, 'Здесь ты можешь изменить размер пиццы', reply_markup=markup)


async def pepperoni_pizza(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💳 Купить')
    button2 = types.KeyboardButton('Изменить размер')
    button3 = types.KeyboardButton('↩️ Назад')
    markup.row(button2)
    markup.row(button1, button3)

    await bot.send_message(message.chat.id, 'Томатный соус, пикатная пепперони, моцарелла.', reply_markup=markup)


async def gavaii_pizza(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💳 Купить')
    button2 = types.KeyboardButton('Изменить размер')
    button3 = types.KeyboardButton('↩️ Назад')
    markup.row(button2)
    markup.row(button1, button3)

    await bot.send_message(message.chat.id, 'Моцарелла, ананасы, цыпленок', reply_markup=markup)


async def chicken_kari_pizza(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💳 Купить')
    button2 = types.KeyboardButton('Изменить размер')
    button3 = types.KeyboardButton('↩️ Назад')
    markup.row(button2)
    markup.row(button1, button3)

    await bot.send_message(message.chat.id, 'Соус кари, томатный соус, цыпленок, красный лук, моцарелла, бекон',
                           reply_markup=markup)


async def burger_pizza(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('💳 Купить')
    button2 = types.KeyboardButton('Изменить размер')
    button3 = types.KeyboardButton('↩️ Назад')
    markup.row(button2)
    markup.row(button1, button3)

    await bot.send_message(message.chat.id,
                           'Томатный соус, моцарелла, ветчина, красный лук, томаты, огурчики, бургер соус, чеснок',
                           reply_markup=markup)
