#!/usr/bin/env python3
import telebot
import json
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

from sensor import Sensor


if __name__ == '__main__':
    config = json.load(open('config.json'))
    bot = telebot.TeleBot(config['token'])
    sensor = Sensor('/dev/ttyUSB0')
    time_day = []
    temp_day = []
    while True:
        sensor.update()
        temp = sensor.temperature
        now = datetime.datetime.now()
        s1 = int(now.strftime('%H')); s2 = int(now.strftime('%M')); s3 = int(now.strftime('%S'))
        time_day.append(s1 * 3600 + s2 * 60 + s3)
        temp_day.append(float(temp))
        plt.plot(time_day, temp_day, marker = 'o')
        plt.savefig('Figure.png', dpi = 100)
        plt.clf()
        print temp
        if(temp > float(config['crit_temperature'])):
            temp_crit = []
            time_crit = []
            for i in range(30):
                sensor.update()
                temp_crit.append(s.temperature)
                time_crit.append(i)
                time.sleep(1)
            A = np.vstack([temp_crit, np.ones(len(temp_crit))]).T
            m, c = np.linalg.lstsq(A, temp_crit)[0]
            angle = np.tan(m)
            print angle, read.tan
            if(angle > float(config['tan'])):
                with open('Figure.png') as f:
                    bot.send_photo(config['channel'], f.read(), caption='Превышена допустимая температура')
        time.sleep(10)
