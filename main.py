import telebot
import re
import json

#скрестить delete и deleteTheme в одно засчет "перегрузки" чтобы упросить использование?

#Добавить возможно опционально писать заметку для ссылки при добавлнеии
#Добавить запуск вместе с экзешником телеграма и выключение вместе с выключением телеграмма
#Добавить кнопки для бота для удобства работы

print("active")
print()

def read_all():
    with open('data.json') as f:
        data = json.load(f)
    return data

def append_data(data, theme):
    if (data.get(theme.category) is None):
        #создание категории
        dict = {theme.category: {'1': theme.link}}
        data.update(dict)
        #print(data)

    else:
        #добавление ссылки
        dict = {last_number(data, theme.category): theme.link}
        data.get(theme.category).update(dict)
        #print(data)

def last_number(data, category):
    max = 1
    flag = True
    while(flag):
        if(data.get(category).get(str(max)) is None):
            flag = False
        else:
            max += 1
    return max

def write_all(data):
     with open('data.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)

def add_data(theme):
    data = read_all()
    append_data(data, theme)
    write_all(data)

class Theme:
    def __init__(self, category, link):
        self.category = category
        self.link = link

BookMarkBot = telebot.TeleBot("5678487785:AAEqnC9xjsKmvghEUWgxVGnzYvnf7SBOvcY", parse_mode=None)

@BookMarkBot.message_handler(commands=['start'])
def send_welcome(message):
	BookMarkBot.send_message(message.chat.id, "Приветствую, я бот для сохранения интересных вкладок по темамтикам, чтобы не засорять браузер. /help для ознакомления с функционалом.")

@BookMarkBot.message_handler(commands=['help'])
def help(message):
	BookMarkBot.send_message(message.chat.id, f"Вот список доступных команд:\n\n"
                                      "/show НазваниеТемы - выводит список всех ссылок из указанной тематики\n\n"
                                      "/add НазваниеТематики https://example.com - добавляет ссылку. Автоматически создает тематику, если она не существует\n\n"
                                      "/delete НазваниеТематики НомерСсылки - Удаляет ссылку из выбранной тематики по указанному номеру. Для ознакомления с ссылками тематики используйте /show\n\n"
                                      "/deleteTheme НазваниеТематики - Удаление тематики и всех ссылок, которые в ней содержатся\n\n"
                                      "/showThemes - Показывает все существующие тематики\n\n"
                                      "/showAll - Показывает все тематики и все ссылки, которые в них содержатся")

@BookMarkBot.message_handler(commands=['add'])
def add(message):
    if (re.fullmatch('\/add.+', message.text)):
        split_data = message.text.split(' ')
        if(len(split_data) == 3):
            category = split_data[1]
            link = split_data[2]

            theme = Theme(category, link)
            add_data(theme)

            BookMarkBot.send_message(message.chat.id, "Ссылка добавлена")

            print('added:')
            data = read_all()
            print(data)
            print()
        else:
            BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /add Тематика https://example.com")
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /add Тематика https://example.com")

@BookMarkBot.message_handler(commands=['show'])
def show(message):
    if (re.fullmatch('^\/show \w+', message.text)):
        category = re.search(' \w+', message.text)[0].replace(' ', '')
        data = read_all()
        if(data.get(category) is not None):
            links = data.get(category)
            data = read_all()
            listofthemes = str(category) + ':\n'

            for i in range(last_number(data, category) - 1):
                listofthemes += str(i + 1) + ') ' + data.get(category).get(str(i + 1)) + '\n'
            BookMarkBot.send_message(message.chat.id,
                                     listofthemes)

            print('showed:')
            print(listofthemes)
            print()


        else:
            BookMarkBot.send_message(message.chat.id,
                                     'к сожалению, тематики с таким названием не существует, для ознакомления со списком тематик используйте /showThemes')
    else:
        BookMarkBot.send_message(message.chat.id, "Не могу распознать команду, возможно вы имели ввиду:\n /show НазваниеТематики, если нет, то используйте /help для ознакомления со списком команд")

@BookMarkBot.message_handler(commands=['delete'])
def delete(message):
    if (re.fullmatch('^\/delete \w+ \d+', message.text)):
        data = read_all()
        split_data = message.text.split(' ')
        category = split_data[1]
        number = split_data[2]

        if (data.get(category) is not None):
            links = data.get(category)

            if (int(number) <= len(links) and int(number) > 0):
                for i in range(int(number), len(data.get(category))):
                    links[str(i)] = links[str(i + 1)]
                links.pop(str(len(links)))
                write_all(data)
                print('Deleted: ')
                print(data)

                BookMarkBot.send_message(message.chat.id,'Ссылка удалена')
            else:
                BookMarkBot.send_message(message.chat.id,
                                         'К сожалению cсылки с таким номером не существует, для ознакомления со списком ссылок используйте /show')
        else:
            BookMarkBot.send_message(message.chat.id,
                                     'К сожалению темы с таким названием не существует, для ознакомления со списком тематик используйте /showThemes')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nвозможно вы имели ввиду /delete, если нет, то используйте /help для ознакомления со списком всех команд")

@BookMarkBot.message_handler(commands=['deleteTheme'])
def delete_theme(message):
    if (re.fullmatch('^\/deleteTheme \w+', message.text)):
        category = re.search(' \w+', message.text)[0].replace(' ', '')
        data = read_all()
        if (data.get(category) is not None):
            links = data.get(category)
            data.pop(category)
            write_all(data)
            print('deleted: ')
            print(links)

            BookMarkBot.send_message(message.chat.id, "Тема удалена")
        else:
            BookMarkBot.send_message(message.chat.id,
                                     'К сожалению темы с таким названием не существует, для ознакомления со списком тематик используйте /showThemes')
    else:
        BookMarkBot.send_message(message.chat.id, "Не могу распознать команду, \nвозможно вы имели ввиду /deleteTheme НазваниеТематики, если нет, то используйте /help для ознакомления со списком всех команд")

@BookMarkBot.message_handler(commands=['showThemes'])
def show_themes(message):
    if (re.fullmatch('^\/showThemes', message.text)):
        data = read_all()
        if(data is not None and data != '{}'):
            number = 1
            themes = 'Список тем: \n'
            for key, value in data.items():
                themes += str(number) + ') ' + str(key) + '\n'
                number += 1

            if(themes != 'Список тем: \n'):
                BookMarkBot.send_message(message.chat.id, themes)
            else:
                BookMarkBot.send_message(message.chat.id, 'К сожалению, темы отсутствуют, для создания темы используйте /add')


            print('themes showed:')
            print(themes)
            print()
    else:
        BookMarkBot.send_message(message.chat.id, "Не могу распознать команду, возможно вы имели ввиду: \nшаблон команды /show Тематика ")

@BookMarkBot.message_handler(commands=['showAll'])
def show_all(message):
    if (re.fullmatch('^\/showAll', message.text)):
        data = read_all()
        new_message = message
        themes = 'Список тем: \n'
        for key, value in data.items():
            themes += str(1) + ') ' + str(key) + '\n'
        if (themes != 'Список тем: \n'):
            if(data is not None and len(data) != 0):
                print('Showed Content:')
                for key, value in data.items():
                    new_message.text = '/show ' + str(key)
                    show(new_message)
        else:
            BookMarkBot.send_message(message.chat.id, 'К сожалению, темы отсутствуют, для создания темы используйте /add')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /show Тематика ")

@BookMarkBot.message_handler(func=lambda message: True)
def unknown_command(message):
	BookMarkBot.reply_to(message, "К сожалению такой команды я не знаю :(   "
                                  "Используй /help для ознакомления со списком команд")

BookMarkBot.infinity_polling()