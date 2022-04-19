import requests
import datetime
from config import open_weather_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram. utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привет, напише мне название города, я пришлю инфу о погоде!')


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B'
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_weather = int(data['main']['temp'])
        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'Посмотри в окно!'
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        len_of_day = sunset_timestamp - sunrise_timestamp

        await message.reply(f'*** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} ***\n'
              f'Погода в городе: {city}\nТемпература: {cur_weather} C° {wd}\n'
              f'Влажность: {humidity} %\nДавление : {pressure} мм.рт.ст\nВетер : {wind_speed} м/с\n'
              f'Восход солнца: {sunrise_timestamp}\nЗаход солнца: {sunset_timestamp}\n'
              f'Продолжительность дня: {len_of_day}\n'
              f'*** Хорошего дня! \U0001F60A ***'
              )
    except:
        await message.reply('\U00002620 Проверьте название города! \U00002620')

if __name__ == '__main__':
    executor.start_polling(dp)
