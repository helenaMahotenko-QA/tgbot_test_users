# подключение библиотек
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: вставить свой токен
TOKEN = 'Вставьте свой токен'
bot = TeleBot(TOKEN, parse_mode='html')
# указываем язык - русский
faker = Faker('ru_RU') 

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    sti=open('welcome.webp','rb')
    bot.send_sticker(message.chat.id,sti)
    bot.send_message(
        chat_id=message.chat.id,
        text="Приветстсвую тебя, усталый QA!\nЕсли твое правое полушарие отказывается работать, Воображариум поможет тебе сгенерировать данные тестовых пользователей.\nПросто выбери число и я создам их для тебя! 👇🏻",
        reply_markup=main_menu_reply_markup
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # определяем количество тестовых пользователей
    # или отправляем ошибку
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    else:
        hmm=open('again.webp','rb')
        bot.send_sticker(message.chat.id,hmm)
        bot.send_message(chat_id=message.chat.id, text="Давай попробуем ещё раз. Дыши, пусть энергия течёт, подумай о Земле, об океане, о новых друзьях... и просто нажми на одну из кнопочек 1, 2, 5 или 10 👇🏻")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        user_info.pop('sex')
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=False,
        ensure_ascii=False,
        default=str
    )

    # отправляем результат
    mag=open('magic.webp','rb')
    bot.send_sticker(message.chat.id,mag)
    import time
    time.sleep(4)
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Вуаля! Поздравляю, у тебя теперь есть {payload_len} воображаемых друзей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Моё воображение всегда к твоим услугам! Если нужно больше друзей, можешь выбрать еще раз 👇🏻"),  
    reply_markup=main_menu_reply_markup
    
# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
