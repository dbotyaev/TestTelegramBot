import apiai
import json
from settings import APIAI_TOKEN


def reply_ai_dialogflow(parrot_message):
    #print(parrot_message)
    # Токен API к Dialogflow
    request = apiai.ApiAI(APIAI_TOKEN).text_request()
    # На каком языке будет послан запрос
    request.lang = 'ru'
    # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.session_id = 'dbotyaevbot'
    # Посылаем запрос к ИИ с сообщением от юзера
    request.query = parrot_message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    # Разбираем JSON и вытаскиваем ответ
    response=''
    response = responseJson['result']['fulfillment']['speech']
    # Если есть ответ от бота - выдаём его,
    # если нет - бот его не понял
    print('ИИ DialogFlow ответил "'+response+'"')
    if response:
        return response
    else:
        return 'Это я еще не понимаю, перефразируйте ваше сообщение!'

# s=''
# while(s!='Выход'):
# s=input('Введите ваше сообщение: ')
# print(reply_ai_dialogflow(s))