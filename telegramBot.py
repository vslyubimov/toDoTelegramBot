import telebot
from PIL import Image
from telebot import types
from pathlib import Path
import dataBaseHandler


file = open(Path().absolute() / 'token.txt')
TOKEN = file.read()


bot = telebot.TeleBot(TOKEN)

""" Команда /start """
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, "Привет, я TODO-list. В меня можно отправлять сообщения, "
                                           "которые я сохраню и верну."
                                           "Также можешь прикрепить фоточку с текстиком :3"
                                           "А ещё ты можешь вызвать /help для большего понимания ситуации ;)")


""" /add + *текст* """
@bot.message_handler(commands=['add'], content_types=['text'])
def add_text_handler(message):

    # сделаю слайс, вырезав /add

    message.text = message.text[5:]
    input_text = message.text

    id = int(str(dataBaseHandler.number_of_tasks((str(message.from_user.id))))) + 1
    new_task = (id, message.from_user.id, input_text, 'NULL')
    dataBaseHandler.add_elements(new_task)
    bot.send_message(message.from_user.id, 'Записано')


""" /add + *фотография* + *caption* """
@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    """проверка на наличие /add в caption. если есть, считываем фоточку"""
    try:
        if str(message.caption[0:4]) == "/add":
            file = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file.file_path)
            filename = message.photo[1].file_id


            src = (Path().absolute() / "photos" / filename).with_suffix(".jpg")
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            id = int(str(dataBaseHandler.number_of_tasks(str(message.from_user.id)))) + 1
            new_element = (id, message.from_user.id, message.caption[4:], str(src))
            dataBaseHandler.add_elements(new_element)
            bot.send_message(message.chat.id,'Данные успешно сохранены')
        else:
            bot.send_message(message.chat.id, 'А где данные?')
    except TypeError as err:
        bot.send_message(message.chat.id, 'Используй /add *данные*')



""" Команда /help """
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, "Ты можешь отправить мне команды: \n"
                                           "Новая задача (/add *текст или фото + текст*) \n"
                                           "Удалить задачу <#> (/delete *номер задачи*) \n"
                                           "Список задач (/all) \n"
                                            "Кнопки (/buttons)")


""" Команда /all """
@bot.message_handler(commands=['all'])
def show_all_handler(message):
    bot.send_message(message.from_user.id, "Список: \n")
    rows = dataBaseHandler.return_database(str(message.from_user.id))
    out = ''
    for row in rows:
        out = str(row[0]) + " || " + str(row[1])
        print(out)
        image_adress = row[2]
        if image_adress == 'NULL':
            bot.send_message(message.from_user.id, out)
        else:
            photo = open(str(row[2]), 'rb')
            bot.send_photo(message.from_user.id, photo, out)



#ниже пример выполнения кнопки
""" команда button """
@bot.message_handler(commands=['buttons'])
def button_handler(message):

    # or add KeyboardButton one row at a time:
    markup = types.ReplyKeyboardMarkup()

    item_start = types.KeyboardButton('/start')
    #item_add = types.KeyboardButton('/add')
    item_all = types.KeyboardButton('/all')
    #item_delete = types.KeyboardButton('/delete')
    item_help = types.KeyboardButton('/help')

    markup.row(item_start, item_all, item_help)
    bot.send_message(message.from_user.id, "Выбери команду:", reply_markup=markup)


""" команда id пользователя """
@bot.message_handler(commands=['user_id'])
def user_id_handler(message):
    user_id = message.from_user.id
    print(type(user_id))
    print(user_id)


""" команда delete """
@bot.message_handler(commands=['delete'], content_types=['text'])
def delete_element_handler(message):
    delete_id = message.text[8:]
    idtask = (delete_id, message.from_user.id)
    file_path = Path(dataBaseHandler.photopath(idtask))
    try:
        file_path.unlink()
    except OSError as e:
        print("Ошибка: %s : %s" % (file_path, e.strerror))
    dataBaseHandler.deltask(idtask)




""" Запустим нашего бота """
bot.polling(none_stop=True, interval=0, timeout=20)
