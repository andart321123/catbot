import asyncio
import logging
import sys
import os
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

number_of_cats = len(glob('./cats/*'))
users = {}


def get_cats_list() -> list:
    return list(map(lambda i: i.replace('./cats\\', ''), glob('./cats/*')))

cats_list = get_cats_list()

def is_admin(message) -> bool:
    return True if int(ADMIN_ID) == message.chat.id else False


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if is_admin(message):
        await message.answer(f"Режим администратора - {hbold(message.from_user.full_name)}!", reply_markup=admin_kb)
    else:
        await message.answer(f"Привет, {hbold(message.from_user.full_name)}!", reply_markup=user_kb)


@dp.message(F.text)
async def text(message: types.Message) -> None:
    text = ' '.join(message.text.split()[1:-1])

    if is_admin(message) and text == 'СПИСОК КОШЕК':
        for cat in cats_list:
            del_cat_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔼 УДАЛИТЬ 😿', callback_data=cat)]])
            await message.answer_photo(FSInputFile(f'cats/{cat}'), cat, reply_markup=del_cat_kb)
            
    else:
        if message.chat.id not in users:
                users[message.chat.id] = {'cats': []}

        cat = choice(cats_list)

        while cat in users[message.chat.id]['cats']:
            if len(users[message.chat.id]['cats']) == number_of_cats:
                users[message.chat.id]['cats'] = []

            cat = choice(cats_list)

        users[message.chat.id]['cats'].append(cat)
        print(users)

        await message.answer_photo(FSInputFile(f'cats/{cat}'))


@dp.message(F.photo)
async def add_cat(message):
    global number_of_cats, cats_list
    cat = message.photo[-1]

    await bot.download(cat, f'cats/cat{number_of_cats + 1}.jpg')
    await message.reply('Загружено!')
    cats_list = get_cats_list()
    number_of_cats += 1

@dp.callback_query()
async def del_cat(callback) -> None:
    global cats_list

    os.remove(f'cats/{callback.data}')
    cats_list = get_cats_list()

    await callback.answer(text='Удалено!', show_alert=True)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
