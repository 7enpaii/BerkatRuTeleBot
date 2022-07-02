from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from berkatBot import HOST, post, index
from category_data import categories_data

def post_kb(link):
  buttonBack = InlineKeyboardButton('☚', callback_data='back')
  buttonNext = InlineKeyboardButton('☛', callback_data='next')
  buttonLink = InlineKeyboardButton('Перейти', url=link)
  navBtn = InlineKeyboardMarkup().add(buttonLink, buttonBack, buttonNext)
  return navBtn

def category_kb(order):
  buttons = ReplyKeyboardMarkup(resize_keyboard=True)
  
  if order == 'main':
    for i in categories_data:
      button1 = KeyboardButton(i)
      buttons.row(button1)

  else:
    for i in categories_data[order]:
      button1 = KeyboardButton(i)
      buttons.row(button1)
  
  return buttons
      

