import asyncio
import logging
import sys
# from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hunderline

# load_dotenv()
# TOKEN = os.getenv("TOKEN")
# USER_NAME = os.getenv("USER_NAME")
# ADMIN_ID = os.getenv("ADMIN_ID")
TOKEN = '5666112017:AAGruxX_aPjqLUL8Y48hiqE05OBC2PVtKho'
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"{hunderline('Hello')}, {hbold(message.from_user.full_name)}!")


@dp.message()
async def text(message: types.Message) -> None:
    await message.send_copy(chat_id=message.chat.id)

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())