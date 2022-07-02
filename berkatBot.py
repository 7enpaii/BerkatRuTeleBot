import logging
from config import TOKEN
from berkatParse import Berkat
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from post_template import get_post
from keyboards import *
from info_text import *
from category_data import categories_data

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


	

post = ''
index = 1
search_title = ''
page = 1
main_category = ''
search_category = False
HOST = 'https://berkat.ru'


def searching_ad(value, page=1):
  site = Berkat(
      HOST,
      f'https://berkat.ru/search/board?q={value}&type=words&date=all&page={page}'
  )
  return site.parse_search()

def searching_category(value, page=1):
  site = Berkat(
    HOST,
    f'https://berkat.ru{value}?page={page}'
  )
  return site.parse_search()



@dp.message_handler(commands=['start'])
async def send_welcom(message: types.Message):
  await message.answer(start_command)


@dp.message_handler(commands=['help'])
async def send_welcom(message: types.Message):
  await message.answer(help_command)

@dp.message_handler(commands=['categories'])
async def send_welcom(message: types.Message):
  btn = category_kb('main')
  await message.answer('К А Т Е Г О Р И И: ', reply_markup=btn)

#обрабатывает нажатие на inline button
@dp.callback_query_handler(lambda call: True)
async def process_callback(call: types.CallbackQuery):
  global index, post
  if call.data == 'back':
    await call.answer(cache_time=60)
    if index >= 1:  
      index -= 1
      btn = post_kb(post[index][3])
      await call.message.answer(f'{get_post(post, index)}', reply_markup=btn)


  elif call.data == 'next':
    await call.answer(cache_time=60)
    if index <= len(post):
      index += 1
      btn = post_kb(post[index][3])
      await call.message.answer(f'{get_post(post, index)}', reply_markup=btn)
      
@dp.message_handler()
async def echo(message: types.Message):
    global index, post, search_title, page, main_category, search_category
    number = 2332
    if message.text[0] == '*':
      search_category = False
      search_title = message.text[1: len(message.text)]
      post = searching_ad(search_title)
      await message.answer(f'Найдено |  {len(post)}  | объявлений на 1 стр')

    elif message.text.isdigit():
      try:
        index = int(message.text) - 1
        btn = post_kb(post[index][3])
        await message.reply(get_post(post, index), reply_markup=btn)
      except Exception:
        await message.answer('Не коректный пост !')


    elif message.text[0] == '$':
        if search_title:
          page = message.text[1: len(message.text)]
          if page.isdigit() and not search_category:
            post = searching_ad(search_title, page)
            await message.answer(f'Найдено |  {len(post)}  | объявлений на {message.text} странице')

          elif page.isdigit() and search_category:
              post = searching_category(search_title, page)
              await message.answer(f'Найдено |  {len(post)}  | объявлений на стр.{message.text[1: len(message.text)]}')

          else:
            await message.answer('Нет такой страницы или ты ввел помимо числа что-то')
        else:
          await message.answer('Вы еще не выполнили поиск!')


    elif message.text[0] == '-':
      btn = category_kb(message.text)
      main_category = message.text
      await message.answer(f'Вы в Категории {message.text}', reply_markup=btn)
    

    elif message.text[0: 2] == '➤ ':
      try:
        search_category = True
        search_title = categories_data[main_category][message.text]
        post = searching_category(search_title)
        await message.answer(f'Найдено |  {len(post)}  | объявлений \n{message.text} \n\nстр.{page}')
      except Exception:
        await message.answer('Вы еще не выбрали главную категорию\nвыбрите ее /categories')

    elif message.text[0] == '#':
      number = message.text

    elif message.text[0] == '!':
      await message.answer(number)

    else:
        await message.answer('Я не обрабатываю простую строку!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
