import asyncio
import logging
import sys
from glob import glob
from random import randint
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from buttons import *

TOKEN = '5666112017:AAGruxX_aPjqLUL8Y48hiqE05OBC2PVtKho'

dp = Dispatcher()

number_of_cats = len(glob('./cats/*'))

users = {}

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=user_kb)

@dp.message(F.text)
async def text(message: types.Message) -> None:
    if message.chat.id not in users:
        users[message.chat.id] = {'cats': []}
    try:
        cat = f'cat{randint(1, number_of_cats)}.jpg'

        while cat in users[message.chat.id]['cats']:
            if len(users[message.chat.id]['cats']) == number_of_cats:
                users[message.chat.id]['cats'] = []

            cat = f'cat{randint(1, number_of_cats)}.jpg'

        users[message.chat.id]['cats'].append(cat)
        print(users)

        await message.answer_photo(FSInputFile(f'cats/{cat}'))

    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

@dp.message(F.photo)
async def add_cat(message):
    global number_of_cats
    cat = message.photo[-1]
    
    await bot.download(cat, f'cats/cat{number_of_cats+1}.jpg')
    message.reply('Загружено!')
    number_of_cats += 1

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())