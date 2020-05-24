from ai_dialogflow import reply_ai_dialogflow
#from bs4 import BeautifulSoup
from handlers import *
import logging
#from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from settings import TG_TOKEN, TG_API_URL
from utility import *
#from utility import get_keyboard
#import requests
from random import choice


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def sms(bot, update):
    """
    функция принимает два обязательных параметра (сообщение, которое пришло от платформы Telegram, и
    экземпляр бота, с помощью которого мы им управляем)
    функция будет вызвана пользователем при отправке команды /start
    внутри функции будет описана логика ответов при ее вызове
    :param bot:
    :param update:
    :return:
    """
    user = search_or_save_user(mdb, bot.effective_user, bot.message)
    print(user)

    # print(bot.effective_user)
    # print()
    # print(bot.message)
    # print()
    print(f'"{bot.message.chat.first_name}" отправил(а) команду /start, что мне делать?') #вывод сообщения в консоль при отправки команды /start
    #my_keyboard = ReplyKeyboardMarkup([['Анекдот']], resize_keyboard=True)  # добавляем кнопки
    smile = emojize(choice(SMILE), use_aliases=True)  # для ответа добавили emoji
    bot.message.reply_text(f'Привет, {bot.message.chat.first_name}! \nЯ бот с ИИ от DialogFlow и еще пока плохо разговариваю, но быстро учусь{smile}',
                           reply_markup = get_keyboard()) #отправляем ответ И подключаем клавиатуру
    #print(bot.message)

def parrot(bot, update):
    print(f'"{bot.message.chat.first_name}" отправил сообщение "{bot.message.text}"') #выводим в консоль текст отправленный пользователем
    #bot.message.reply_text(bot.message.text) #отправляем пользователю обратно его текст
    smile = emojize(choice(SMILE), use_aliases=True)  # для ответа добавили emoji
    bot.message.reply_text(reply_ai_dialogflow(bot.message.text)+smile)

def main():
    my_bot = Updater(TG_TOKEN, TG_API_URL, use_context=True)
    logging.info('Start bot')
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    # dispatcher принимает от платформы Telegram входящее сообщение
    # add_handler передает его в обработчик CommandHandler.
    # CommandHandler подписанный на реагирование определенных событий выполняет следуюущие действия:
    # когда нажмут команду /start, переходит к вызову функции sms()
    #my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Начать'), sms)) #обработка текста кнопки
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Котики 🏞'), send_meme))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote)) #обработка текста кнопки
    #my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Пообщаться с ИИ'),
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, get_contact))  # обработчик полученного контакта
    my_bot.dispatcher.add_handler(MessageHandler(Filters.location, get_location))  # обработчик полученной геопозиции
    my_bot.dispatcher.add_handler(CallbackQueryHandler(inline_button_pressed))
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Заполнить анкету'), anketa_start)],
                                                      states={
                                                          "user_name": [MessageHandler(Filters.text, anketa_get_name)],
                                                          "user_age": [MessageHandler(Filters.text, anketa_get_age)],
                                                          "evaluation": [MessageHandler(Filters.regex('1|2|3|4|5'),
                                                                                        anketa_get_evaluation)],
                                                          "comment": [MessageHandler(Filters.regex('Пропустить'),
                                                                                     anketa_exit_comment),
                                                                      MessageHandler(Filters.text, anketa_comment)]
                                                      },
                                                      fallbacks=[MessageHandler(
                                Filters.text | Filters.video | Filters.photo | Filters.document, dontknow)]))
    # ConversationHandler — позволяет строить (описывать) диалоги со сложной логикой.
    # У каждого ConversationHandler есть:
    # entry_points — запускает данный диалог, точка входа.
    # states — шаги диалога, у каждого шага есть название и обработчик на который этот шаг реагирует.
    # fallbacks — выход из диалога или можно использовать при некорректном вводе информации пользователем.
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))  # обработка только текстовых сообщений
    my_bot.start_polling()
    my_bot.idle()

if __name__ == '__main__':
    main()

#main()