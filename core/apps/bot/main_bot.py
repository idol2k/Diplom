import psycopg2
import webbrowser
from core.settings import TOKEN_BOT
from aiogram import Bot, types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot=bot, storage=storage)

conn = psycopg2.connect(
    dbname="telegram_pizza", user="Viper", password="", host="127.0.0.1", port="5432"
)
cur = conn.cursor()


@dp.message_handler(commands=["register"])
async def register_user(message: types.Message):
    try:

        user_id = message.chat.id
        cur.execute(
            "INSERT INTO bot_users (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (user_id, ""),
        )
        conn.commit()

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Каталог пицц")
        button2 = KeyboardButton("Настройки")
        button3 = KeyboardButton("Справка")
        button4 = KeyboardButton("Корзина")
        markup.row(button1, button4)
        markup.row(button2, button3)

        await bot.send_message(
            user_id, "Можете заказывать покушоц :)", reply_markup=markup
        )
    except Exception as err:
        print(err, "1")


@dp.message_handler(commands=["start"])
async def welcome(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    cur.execute("SELECT id FROM bot_users WHERE id = %s", (user_id,))
    user_exists = cur.fetchone()
    if message.text == "/start" and not user_exists:

        await bot.send_message(
            user_id, text="Добро пожаловать! Для регистрации введите команду /register"
        )
    else:

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = KeyboardButton("Каталог пицц")
        button2 = KeyboardButton("Настройки")
        button3 = KeyboardButton("Справка")
        button4 = KeyboardButton("Корзина")
        markup.row(button1, button4)
        markup.row(button2, button3)
        await bot.send_message(
            user_id, "Привет, можете заказывать покушать!", reply_markup=markup
        )


@dp.message_handler(lambda x: x.text == "Корзина")
async def show_cart(message: types.Message):
    reply = types.InlineKeyboardMarkup()
    reply = types.InlineKeyboardMarkup()
    reply.add(types.InlineKeyboardButton(text="Купить", callback_data="buy"))
    reply.add(types.InlineKeyboardButton(text="Удалить", callback_data="delete"))
    user_id = str(message.chat.id)
    cur.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
    cart_items = cur.fetchall()
    if cart_items:
        for item in cart_items:
            await bot.send_message(
                user_id,
                f"Пицца: {item[1]}\nРазмер: {item[4]}\nЦена: {item[2]}",
                reply_markup=reply,
            )
    else:
        await bot.send_message(user_id, "Ваша корзина пуста.")


@dp.callback_query_handler(lambda call: call.data.lower() == "buy")
async def buy(call):
    webbrowser.open("https://t.me/IDOL2k")


@dp.callback_query_handler(lambda call: call.data.lower() == "delete")
async def delete(call):
    id_user = str(call.message.chat.id)
    cur.execute("DELETE FROM orders WHERE user_id = %s", (id_user,))
    conn.commit()
    msg_id = await bot.send_message(call.message.chat.id, text="Пицца удалена!")
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=msg_id.message_id - 1
    )


@dp.message_handler(lambda message: message.text == "Назад")
async def back_on_list(message: types.Message):
    await goodsChapter(message, state="FSMContext")


@dp.message_handler(lambda message: message.text == "Назад в меню")
async def back_on_list(message: types.Message):
    await welcome(message, state="FSMContext")


@dp.message_handler(content_types="photo")
async def get_photo(message):
    await bot.send_message(
        message.chat.id, "У меня нет возможности просматривать фото :("
    )


@dp.message_handler(lambda x: x.text == "Каталог пицц")
async def goodsChapter(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Пепперони")
    button2 = types.KeyboardButton("Гавайская")
    button3 = types.KeyboardButton("Цыпленок кари")
    button4 = types.KeyboardButton("Бургер-пицца")
    button5 = types.KeyboardButton("Назад в меню")
    markup.row(button1, button2)
    markup.row(button3, button4)
    markup.row(button5)
    await bot.send_message(
        chat_id=message.chat.id,
        text="Вот все товары, которые сейчас находятся в продаже:",
        reply_markup=markup,
    )


@dp.message_handler(
    lambda x: x.text in ["Пепперони", "Гавайская", "Цыпленок кари", "Бургер-пицца"]
)
async def pizza(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await goodsChapter(message, state)
        return

    pizza_name = message.text
    cur.execute(
        "SELECT ingredients FROM bot_pizza WHERE pizza_name = %s", (pizza_name,)
    )
    ingredients = cur.fetchone()

    if ingredients:
        ingredient_list = ingredients[0].split(",")
        ingredient_text = "\n".join(ingredient_list)
        await bot.send_message(message.chat.id, text=f"Ингредиенты:\n{ingredient_text}")

    async with state.proxy() as data:
        data["pizza"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Выбрать размер")
    button2 = types.KeyboardButton("Назад")
    markup.row(button1, button2)

    await bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@dp.message_handler(lambda message: message.text == "Выбрать размер")
async def change(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="small")
    button2 = types.KeyboardButton(text="medium")
    button3 = types.KeyboardButton(text="large")
    markup.row(button1, button2, button3)
    await bot.send_message(
        message.chat.id, text=f"Выберите желаемый размер пиццы!", reply_markup=markup
    )


@dp.message_handler(lambda message: message.text in ["small", "medium", "large"])
async def change_size(message: types.Message, state: FSMContext):
    size = message.text
    async with state.proxy() as data:
        data["size"] = message.text

    cur.execute("SELECT price FROM bot_pizza WHERE size = %s", (size,))
    cur.fetchone()

    conn.commit()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text="Добавить в корзину")
    markup.row(button1)
    await bot.send_message(
        message.chat.id, text=f"Размер пиццы изменен!", reply_markup=markup
    )


@dp.message_handler(lambda message: message.text == "Добавить в корзину")
async def get_info_order(message: types.Message, state: FSMContext):
    pizza_name = message.text
    async with state.proxy() as data:
        pizza = data["pizza"]
        size = data["size"]
    cur.execute(
        "SELECT ingredients FROM bot_pizza WHERE pizza_name = %s", (pizza_name,)
    )
    cur.fetchone()
    cur.execute(
        "SELECT * FROM bot_pizza WHERE pizza_name = %s and size = %s",
        (
            pizza,
            size,
        ),
    )
    pizza_info = cur.fetchone()
    cur.execute(
        "INSERT INTO orders (user_id, pizza_name, product_price, size) VALUES (%s, %s, %s, %s) ON CONFLICT DO "
        "NOTHING",
        (message.chat.id, pizza_info[1], pizza_info[3], pizza_info[2]),
    )
    conn.commit()

    await bot.send_message(message.chat.id, text=f"Успешно добавлено!")
    await goodsChapter(message, state)


@dp.message_handler(lambda message: message.text == "Настройки")
async def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Настройки #1")
    button2 = types.KeyboardButton("Настройки #2")
    button3 = types.KeyboardButton("Назад в меню")
    markup.row(button1, button2)
    markup.row(button3)
    await bot.send_message(
        message.chat.id,
        "Раздел настроек. Выбери один из вариантов:",
        reply_markup=markup,
    )


@dp.message_handler(lambda message: message.text == "Справка")
async def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Написать разработчику")
    button2 = types.KeyboardButton("Назад в меню")
    markup.row(button1, button2)
    await bot.send_message(
        message.chat.id,
        "Раздел справки. Здесь ты можешь написать моему разработчику.",
        reply_markup=markup,
    )


@dp.message_handler()
async def info(message):
    if message.text == "Написать разработчику":
        webbrowser.open("https://t.me/IDOL2k")
    elif message.text == "Настройки #1":
        await bot.send_message(message.chat.id, "Настройки номер 1...")

    elif message.text == "Настройки #2":
        await bot.send_message(message.chat.id, "Настройки номер 2...")
