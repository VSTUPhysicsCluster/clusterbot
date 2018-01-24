#!/usr/bin/env python3
import telebot
import json

from sensor import Sensor


if __name__ == '__main__':
    config = json.load(open('config.json'))
    bot = telebot.TeleBot(config["token"])
    sensor = Sensor("/dev/ttyUSB0")
    while True:
        sensor.update()
        bot.send_message(config["public"], str(sensor))
