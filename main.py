import telebot
import re
import json

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

BookMarkBot = telebot.TeleBot("", parse_mode=None)

@BookMarkBot.message_handler(commands=['start'])
def send_welcome(message):
	BookMarkBot.send_message(message.chat.id, "Приветствую, я бот для сохранения интересных вкладок по темамтикам, чтобы не забивать браузер. /help для ознакомления с функционалом.")

@BookMarkBot.message_handler(commands=['help'])
def show_options(message):
	BookMarkBot.send_message(message.chat.id, f"Список команд:\n\n"
                                      "/show НазваниеТемы - вывести список ссылок принадлежащих теме\n\n"
                                      "/add Тематика -u https://example.com - добавить ссылку. В случае если заданная тематика не существует, то создается новая темаитка с соответствующим названием.\n\n"
                                      "/delete Тематика НомерСсылки - Удаляет ссылку под выбранным номером из выбранной тематики\n\n"
                                      "/deleteTheme ИмяТематики - удаление тематики. Удаление тематики происходит вместе с удалением всех ее ссылок"
                                      "/showThemes - Показывает все темы в которых есть ссылки"
                                      "/showAll - Показывает все темы и все ссылки, которые в них содержатся")

@BookMarkBot.message_handler(commands=['add'])
def add_theme(message):
    if (re.fullmatch('^\/add (\w+)\s\-u\s(\w+):\/\/([\w\-\.]+)', message.text)
    or
       re.fullmatch('^\/add (\w+)\s\-u\s(\w+)://([\w\-\.]+)(/(\w+).(\w+))+', message.text)
    ):
        if(re.fullmatch('^\/add (\w+)\s\-u\s(\w+):\/\/([\w\-\.]+)', message.text)):
            category = re.search("\s\w+", message.text)[0].replace(" ", "")
            link = re.search(" -u \w+:\/\/\w+.\w+", message.text)[0].replace(' -u ', '')

            theme = Theme(category, link)
            add_data(theme)

            print('added:')
            data = read_all()
            print(data)
            print()

        if(re.fullmatch('^\/add \w+ -u \w+:\/\/\w+.\w+(/\w+.\w+)+', message.text)):
            category = re.search("\s\w+", message.text)[0].replace(" ", "")
            link = re.search(' -u \w+:\/\/\w+.\w+(/\w+.\w+)+',
                              message.text)[0].replace(' -u ', '')

            theme = Theme(category, link)
            add_data(theme)

            print('added:')
            data = read_all()
            print(data)
            print()
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /add Тематика -u https://example.com")

@BookMarkBot.message_handler(commands=['show'])
def show_links(message):
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
                                     'Темы с таким названием не существует')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /show Тематика ")

@BookMarkBot.message_handler(commands=['delete'])
def delete_link(message):
    if (re.fullmatch('^\/delete \w+ \d+', message.text)):
        category = re.search(' \w+ ', message.text)[0].replace(' ', '')
        number = re.search('\d+', message.text)[0].replace(message.text, message.text)
        data = read_all()

        if (data.get(category) is not None):
            if ((last_number(data, category) - 1) >= int(number)):
                print(data.get(category))
                for i in range(int(number), len(data.get(category))):
                    data.get(category)[str(i)] = data.get(category)[str(i + 1)]

                del data.get(category)[str(len(data.get(category)))]
                write_all(data)
            else:
                BookMarkBot.send_message(message.chat.id,
                                         'Ссылки с таким номером не существует.'
                                         'для получения списка ссылок используйте '
                                         '/show Название темы')
        else:
            BookMarkBot.send_message(message.chat.id,
                                     'Темы с таким названием не существует')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nвозможно вы имели ввиду /delete Тематика НомерСсылки или /deleteTheme Тематика ")

@BookMarkBot.message_handler(commands=['deleteTheme'])
def delete_theme(message):
    if (re.fullmatch('^\/deleteTheme \w+', message.text)):
        category = re.search(' \w+', message.text)[0].replace(' ', '')
        data = read_all()
        if (data.get(category) is not None):
            links = data.get(category)
            print(links)
            data.pop(category)
            write_all(data)
        else:
            BookMarkBot.send_message(message.chat.id,
                                     'Темы с таким названием не существует')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nВведены некорректные данные, \nвозможно вы имели ввиду /delete Тематика НомерСсылки или /deleteTheme Тематика ")

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
                BookMarkBot.send_message(message.chat.id, 'Темы отсутствуют, для создания темы используйте /add')


            print('themes showed:')
            print(themes)
            print()
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /show Тематика ")

@BookMarkBot.message_handler(commands=['showAll'])
def show_all(message):
    if (re.fullmatch('^\/showAll', message.text)):
        data = read_all()
        new_message = message

        themes = 'Список тем: \n'
        for key, value in data.items():
            themes += str(1) + ') ' + str(key) + '\n'

        if (themes != 'Список тем: \n'):
            BookMarkBot.send_message(message.chat.id, 'Я перед условием')
            if(data is not None and len(data) == 0):
                BookMarkBot.send_message(message.chat.id, 'Я вошел в условие')
                print('Showed Content:')
                for key, value in data.items():
                    BookMarkBot.send_message(message.chat.id, 'Я вошел в цикл')
                    new_message.text = '/show ' + str(key)
                    show_links(new_message)

        else:
            BookMarkBot.send_message(message.chat.id, 'Темы отсутствуют, для создания темы используйте /add')
    else:
        BookMarkBot.send_message(message.chat.id, "Введены некорректные данные, \nшаблон команды /show Тематика ")




@BookMarkBot.message_handler(func=lambda message: True)
def unknown_command(message):
	BookMarkBot.reply_to(message, "К сожалению такой команды я не знаю :(   "
                                  "Используй /help для ознакомления со списком команд")



BookMarkBot.infinity_polling()