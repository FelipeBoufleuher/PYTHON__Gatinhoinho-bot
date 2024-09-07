import os
from dotenv import load_dotenv

import requests
from requests.auth import HTTPBasicAuth

import telebot
from telebot.util import quick_markup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
token = os.getenv('AUTH_TOKEN')

auth = HTTPBasicAuth('apikey', os.getenv('CAT_API_KEY'))

bot = telebot.TeleBot(token)


def get_kitty_pic():
    contents = requests.get(
        'https://api.thecatapi.com/v1/images/search', auth=auth).json()
    image_url = contents[0]['url']
    return image_url

def get_kitty_fact():
    contents = requests.get(
        'https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=1').json()
    fact = contents['text']
    if len(fact) < 10:
        return get_kitty_fact()
    return fact

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Get a kitty pic", callback_data="/nyan"),
        InlineKeyboardButton("Say hello to Gatinhoinho", callback_data="/hello"),
        InlineKeyboardButton("Get a kitty fact (or maybe not)", callback_data="/fact")
    )
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "/nyan":
        meow(call.message)
    elif call.data == "/fact":
        fact(call.message)
    elif call.data == "/hello":
        hello(call.message)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Welcome to the purrrfect bot!</b>', parse_mode='HTML', reply_markup=gen_markup())

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(
        message.chat.id, "\n<b>Hello my friend nya!!</b> \n\nMy name is <b>Gatinhoinho</b> and I'm a bot that can send you random cat pictures and facts! \n\nType /start to see the menu!", parse_mode='HTML'
    )
    with open('data/Sticker-gatinho.webp', 'rb') as sticker:  # Open GIF in binary mode
        bot.send_sticker(message.chat.id, sticker)
    start(message)

@bot.message_handler(commands=['meow'])
@bot.message_handler(regexp=r'meow')
def meow(message):
    url = get_kitty_pic()
    bot.send_message(message.chat.id, 'Nyan! Here is a kitty pic for you:')
    bot.send_photo(message.chat.id, url)
    start(message)

@bot.message_handler(commands=['fact'])
@bot.message_handler(regexp=r'fact')
def fact(message):
    fact = get_kitty_fact()
    bot.send_message(message.chat.id, ('<b>Here is a interesting fact for you:\n </b>' + fact + ' Nyan!'), parse_mode='HTML')
    start(message)

bot.infinity_polling()