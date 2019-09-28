# - *- coding: utf- 8 - *-
import pyowm
import telebot

bot = telebot.TeleBot('983678348:AAGdTxtshkkJq27AImV9uzdTi6pG1d1kAoU')
owm = pyowm.OWM('6131acf6384443764bc43c96311b8898')

degree_sign= u'\N{DEGREE SIGN}'

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAADAgADrQIAAjZ2IA6ZtuZmWWWEYBYE')
    bot.send_message(message.chat.id, 'Привет, я умею показывать погоду, напиши название своего города и я попытаюсь его найти')

@bot.message_handler(content_types=['text'])
def send_text(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()

        windSpeed = w.get_wind()['speed']
        temperature = w.get_temperature('celsius')['temp']
        temperatureMax = w.get_temperature('celsius')['temp_max']

        forecast = owm.three_hours_forecast(message.text)
        isCloudy = forecast.will_have_clouds()
        isRainy = forecast.will_have_rain()

        cloudStatus = '\nВ ближайшее время на улице будет облачно\n' if isCloudy else '\nНа улице сейчас ясно\n'
        rainStatus = 'Возможны осадки, захватите зонтик ;)\n' if isRainy else 'Осадков не ожидается\n'

        bot.send_message(message.chat.id,
        'Температура воздуха в городе ' +
        message.text + ': ' + str(temperature) + degree_sign +'C\n' +
        '\nВетер: ' + str(windSpeed) + ' метра(ов) в секунду\n' +
        '\nМаксимальная температура воздуха сегодня: ' + str(temperatureMax) + degree_sign +'C\n' +
        cloudStatus + rainStatus + '\nХорошего дня!')
        bot.send_sticker(message.chat.id, 'CAADAgADJgAD5KDOB8Xr45EDQlBHFgQ')
    except:
        bot.send_sticker(message.chat.id, 'CAADAgADswIAAjZ2IA49CvVS7mL1aBYE')
        bot.send_message(message.chat.id, 'Прости, но я не смог найти город: ' + message.text + '\nпопробуй написать его название на английском')

bot.polling()
