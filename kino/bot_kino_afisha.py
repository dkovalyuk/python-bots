from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
import csv


file_name = 'films.csv'
headers = ['film', 'category', 'age'] 

# створює файл з поатковими даними
def create_posters():
    global file_name, headers

    films = [
        ['Матриця Воскресіння', 'бойовик', 16],
        ['Людина Павук ', 'пригоди', 12],
        ['Співай - 2', 'мультфільм', 6],
        ['Вічні', 'пригоди', 12]
    ]  

    with open(file_name, 'w', encoding='UTF8', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(films)



# відповідь на неіснуючу команду боту
def error_input(update, context):
    message = '''Введеної команди немає:
    /help - для перегляду доступних команд'''
    update.message.reply_text(message)



# обробка команди /start
def start(update, context):
    global file_name

    if not os.path.exists(file_name):
        #бот запускається вперше - потрібно створити файл і заповнити його даними
        create_posters()

    message = '''Вас вітає бот-кіноафіша:
    /help - для перегляду доступних команд'''

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text = message)



# обробка команди /help
def bot_commands(update, context):   
    message = '''Основні команди [та їх параметри]:
        /posters_list - перегляд фільмів в прокаті
        /posters_add [назва жанр вік] - додати фільм в прокат
        /posters_remove [назва] - зняти фільм з прокату'''

    chat = update.effective_chat
    context.bot.send_message(chat_id = chat.id, text = message) 



# обробка команди /posters_list - показуємо перелік фільмів в прокаті
def films_list(update, context):
    global file_name, headers

    message = 'Фільми в прокаті:'

    with open(file_name, 'r', encoding='UTF8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            film = "|{:<}|{:<}|{:>}|".format(row['film'], row['category'], row['age'])
            print(film)
            message += "\n" + film


    chat = update.effective_chat
    context.bot.send_message(chat_id = chat.id, text = message) 


# обробка команди /posters_add 007 бойовик 18 
# додаємо новий фільм в прокат
def films_add(update, context):
    global file_name, headers

    film_info = update.message.text
    film_info = film_info.split() 

    # тут передбачено, що назва фільму 1 слово. 
    # можна зробити більш кращий варіант, і сформувати назву фільму, обєднавши всі елементи списку film_info 
    # крім film_info[0] (назва команди), film_info[n-1] (віковий ценз), film_info[n-2] (жанр).
    # n - кількість елементів списку  
    
    film = dict()
    film['film'] = film_info[1]
    film['category'] = film_info[2]
    film['age'] = film_info[3]

    with open(file_name, 'a', encoding='UTF8', newline='') as file:
        writer = csv.DictWriter(file, headers)
        writer.writerow(film)

    message = '''Фільм додано в прокат. 
    /posters_list - для перегляду списку всіх фільмів'''

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text = message) 



# обробка команди /posters_remove Матриця 
# знімаємо  фільм з прокату 
def films_delete(update, context):
    global file_name, headers

    film_delete = update.message.text
    film_delete = film_delete.split() 
    
    #тут передбачено, що назва фільму 1 слово. 
    #можна зробити більш кращий варіант, і сформувати назву фільму, обєднавши всі елементи списку film_delete крім film_delete[0]. 
    film_name = film_delete[1]
    
    #ідея видалення: зчитати зміст файлу в список, крім фільму, який має бути видалений. Потім перезапис файлу інформацією зі списку. 
    films = []

    with open(file_name, 'r', encoding='UTF8',) as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['film'] == film_name:
                continue
            films.append([row['film'], row['category'], row['age']])   

    with open(file_name, 'w', encoding='UTF8', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(films)        

    message = '''Фільм знято з прокату. 
    /posters_list - для перегляду списку всіх фільмів'''

    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text = message) 


#створюємо класи для взаємодії з ботом
updater = Updater("5014971515:AAF9Fap0FkHvWqVCy_yu8K2jr_Nnn4yxCMA")
dispatcher = updater.dispatcher

#створюємо обробники подій (команд)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", bot_commands))
dispatcher.add_handler(CommandHandler("posters_list", films_list))
dispatcher.add_handler(CommandHandler("posters_add", films_add))
dispatcher.add_handler(CommandHandler("posters_remove", films_delete))

#все, що не потрапляє в команди бота
dispatcher.add_handler(MessageHandler(Filters.all, error_input))


updater.start_polling()
updater.idle()