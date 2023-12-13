import asyncio
import sys
# from dotenv import load_dotenv
import os
import subprocess
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hunderline
    
import progress.bar as bb
from time import sleep

# load_dotenv()
# TOKEN = os.getenv("TOKEN")
# USER_NAME = os.getenv("USER_NAME")
# ADMIN_ID = os.getenv("ADMIN_ID")
TOKEN = '5666112017:AAGruxX_aPjqLUL8Y48hiqE05OBC2PVtKho'
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

l = list(range(10))

def progress_bar(length, pos):
    return f'[{"@"*pos}{"😸"*(length-pos)}]'

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"{hunderline('Hello')}, {hbold(message.from_user.full_name)}!")


@dp.message()
async def text(message: types.Message) -> None:
    await message.answer(progress_bar(10, 5))
	# 
	# bbb(bb.ChargingBar('ChargingBar'))


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


