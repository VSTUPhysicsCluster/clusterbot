#!/usr/bin/env python3
import telebot
import json
import time
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from sensor import Sensor


if __name__ == '__main__':
    config = json.load(open('config.json'))
    bot = telebot.TeleBot(config['token'])
    sensor = Sensor('/dev/ttyUSB0')
    time_day = []
    temp_day = []
    day = datetime.datetime.now().day
    while True:
        sensor.update()
        temp = sensor.temperature
        now = datetime.datetime.now()
        time_day.append(now)
        temp_day.append(float(temp))
        print(temp)
        if temp > float(config['warn_temperature']):
            temp_warn = []
            time_warn = np.arange(30)
            for i in range(30):
                sensor.update()
                temp_warn.append(sensor.temperature)
                time.sleep(1)
            p = np.polyfit(time_warn, temp_warn, deg=1)
            tang = p[0]

            plt.plot(time_warn, temp_warn, marker='o')
            plt.savefig('Figure.png', dpi=100)
            plt.clf()

            print(tang, config['tan'])
            if tang > float(config['tan']):
                with open('Figure.png', 'rb') as f:
                    bot.send_photo(config['channel'], f,
                                   caption='Температура растёт слишком быстро!')
                continue

        if temp > float(config['crit_temperature']):
            bot.send_message(config['channel'], "Превышена допустимая температура")

        if now.day != day:
            plt.plot(time_day, temp_day, marker='o')
            plt.savefig('Figure.png', dpi=100)
            plt.clf()
            time_day = []
            temp_day = []
            with open('Figure.png', 'rb') as f:
                bot.send_photo(config['channel'], f,
                               caption='Дневной отчёт')
            day = now.day
        time.sleep(10)
