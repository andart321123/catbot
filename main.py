import os
from json import load, dump
from glob import glob
from random import choice

import requests
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold

from buttons import *
from lib import *

TOKEN = os.getenv("CAT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

dp = Dispatcher()
message_type = ''
users = {}
number_of_cats = len(glob('./cats/*'))

if not os.path.exists('admins.json'):
    with open('admins.json', 'w') as f:
        dump({'root': ADMIN_ID, 'admins': []}, f)

with open('admins.json') as f:
    admins = load(f)


def get_cats_list() -> list:
    return list(map(lambda i: i.replace('./cats\\', ''), glob('./cats/*')))


cats_list = get_cats_list()


def is_admin(message) -> str:
    user_id = str(message.from_user.id)
    if admins['root'] == user_id:
        return 'root'
    elif user_id in admins['admins']:
        return 'admin'


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if is_admin(message) == 'admin' or is_admin(message) == 'root':
        await message.answer(f"Режим администратора - {hbold(message.from_user.full_name)}!", reply_markup=admin_kb if is_admin(message)=='admin' else root_kb)
    else:
        await message.answer(f'''Привет, {hbold(message.from_user.full_name)}!
Чтобы добавить свои фотографии, отправляй мне их!''', reply_markup=user_kb)


@dp.message(F.text)
async def text(message: types.Message) -> None:
    global message_type, users
    text = ' '.join(message.text.split()[1:-1])

    if message.text.isdigit():
        if is_admin(message) == 'root' and message_type == 'add_admin':
            admins['admins'].append(message.text)
            with open('admins.json', 'w') as f:
                dump(admins, f)
            await message.reply('Добавлено!!!')

        print(admins)

    elif (is_admin(message) == 'root' or is_admin(message) == 'admin') and text == 'СПИСОК КОШЕК':
        await message.answer(f'Всего {number_of_cats} котов!')
        for cat in cats_list:
            del_cat_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔼 УДАЛИТЬ 😿', callback_data=cat)]])
            await message.answer_photo(FSInputFile(f'cats/{cat}'), reply_markup=del_cat_kb)

    elif is_admin(message) == 'root' and text == 'АДМИНИСТРАТОРЫ':
        await message.answer('root=' + admins['root'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_admin')]]))
        for admin in admins['admins']:
            await message.answer(admin, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data=f'del_admin_id_{admin}')]]))
    
    elif text == 'ШЛЁПА И ПЕЛЬМЕНИ':
        await message.reply('t.me/test_321123bot/shlepa')
    
    elif text == 'НОВОСТИ':
        if message.from_user.id not in users:
            users[message.from_user.id] = {'cats': cats_list.copy(), 'articles': [], 'news_page': 0}
        if len(users[message.from_user.id]['articles']) == 0:
            users[message.from_user.id]['news_page'] += 1
            users[message.from_user.id]['articles'] = get_articles(users[message.from_user.id]['news_page']).copy()
            
        article = users[message.from_user.id]['articles'].pop(0)
        await message.answer_photo(article['img'], hbold(article["header"]) + '\n' + article['text'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Читать далее', url=article['link'])]]))

    else:
        if message.from_user.id not in users:
            users[message.from_user.id] = {'cats': cats_list.copy(), 'articles': get_articles(1), 'news_page': 1}

        cat = users[message.from_user.id]['cats'].pop(users[message.from_user.id]['cats'].index(choice(users[message.from_user.id]['cats'])))

        if len(users[message.from_user.id]['cats']) == 0:
            users[message.from_user.id]['cats'] = cats_list.copy()

        await message.answer_photo(FSInputFile(f'cats/{cat}'))


@dp.message(F.photo)
async def add_cat(message):
    global cats_list, number_of_cats

    photos = message.photo

    cats_list += f'cats/cat{number_of_cats}.jpg'
    number_of_cats += 1
    await bot.download(photos[-1], f'cats/cat{number_of_cats}.jpg')

@dp.callback_query()
async def del_cat_and_admin(callback) -> None:
    global cats_list, admins, message_type

    if 'cat' in callback.data:
        os.remove(f'cats/{callback.data}')
        cats_list = get_cats_list()
        await callback.answer(text='Удалено!', show_alert=True)

    elif callback.data[:13] == 'del_admin_id_':
        del admins['admins'][admins['admins'].index(callback.data[13:])]
        with open('admins.json', 'w') as f:
            dump(admins, f)
        await callback.answer(text='Удалено!', show_alert=True)

    elif callback.data == 'add_admin':
        await callback.answer(text='Введи id нового администратора!')
        message_type = 'add_admin'


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
