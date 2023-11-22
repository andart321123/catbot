import asyncio
import logging
import sys
import os
from json import load, dump
from glob import glob
from random import randint, choice
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold
from buttons import *

TOKEN = os.getenv("CAT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


dp = Dispatcher()
message_type = ''

number_of_cats = len(glob('./cats/*'))
users = {}
if not os.path.exists('admins.json'):
    with open('admins.json', 'w') as f:
        dump({'root': ADMIN_ID, 'admins': []}, f)


with open('admins.json') as f:
    admins = load(f)

print('&', admins)

def get_cats_list() -> list:
    return list(map(lambda i: i.replace('./cats\\', ''), glob('./cats/*')))

cats_list = get_cats_list()

def is_admin(message) -> bool:
    id = str(message.chat.id)
    if admins['root'] == id:
        return 'root'
    elif id in admins['admins']:
        return 'admin'



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if is_admin(message) == 'admin' or is_admin(message) == 'root':
        await message.answer(f"Режим администратора - {hbold(message.from_user.full_name)}!", reply_markup=admin_kb if is_admin(message)=='admin' else root_kb)
    else:
        await message.answer(f"Привет, {hbold(message.from_user.full_name)}! Чтобы добавить свои фотографии, отправляй мне их {hbold('ПО ОДНОЙ!!!!!!')}", reply_markup=user_kb)


@dp.message(F.text)
async def text(message: types.Message) -> None:
    global message_type
    print('text wert')

    text = ' '.join(message.text.split()[1:-1])

    if message.text.isdigit():
        print('!!!')
    

        if is_admin(message) == 'root' and message_type == 'add_admin':
            admins['admins'].append(message.text)
            with open('admins.json', 'w') as f:
                dump(admins, f)
            await message.reply('Добавлено!!!')

        print(admins)

    elif (is_admin(message) == 'root' or is_admin(message) == 'admin') and text == 'СПИСОК КОШЕК':
        print('###')
        await message.answer(f'Всего {number_of_cats} котов!')
        for cat in cats_list:
            del_cat_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔼 УДАЛИТЬ 😿', callback_data=cat)]])
            await message.answer_photo(FSInputFile(f'cats/{cat}'), reply_markup=del_cat_kb)

    elif is_admin(message) == 'root' and text == 'АДМИНИСТРАТОРЫ':
        print('@@@')
        await message.answer('root=' + admins['root'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить', callback_data='add_admin')]]))
        for admin in admins['admins']:
            await message.answer(admin, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Удалить', callback_data=f'del_admin_id_{admin}')]]))
            
    else:
        print('$$$$')
        if message.chat.id not in users:
            users[message.chat.id] = {'cats': cats_list.copy()}

        cat = users[message.chat.id]['cats'].pop(users[message.chat.id]['cats'].index(choice(users[message.chat.id]['cats'])))

        if len(users[message.chat.id]['cats']) == 0:
            users[message.chat.id]['cats'] = cats_list.copy()

        print(users)

        await message.answer_photo(FSInputFile(f'cats/{cat}'))


@dp.message(F.photo)
async def add_cat(message):
    global number_of_cats, cats_list
    cats = message.photo

    for cat in cats:
        print('number_of_cats: ', number_of_cats)
        cat_file = f'cats/cat{number_of_cats + 1}.jpg'
        await bot.download(cat, cat_file)
        number_of_cats += 1
    
    cats_list = get_cats_list()
    
    if is_admin(message) != 'root':
        await bot.send_message(5724447197, text='Новые коты загружены!!!')

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
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
