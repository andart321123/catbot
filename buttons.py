from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

user_buttons = [[KeyboardButton(text=' 😺КОШКИ! 🐈')]]

admin_buttons = [[KeyboardButton(text='😺 КОШКИ! 🐈')],
				 [KeyboardButton(text='📃 СПИСОК КОШЕК 😸')]]

admin_kb = ReplyKeyboardMarkup(keyboard=admin_buttons)
user_kb = ReplyKeyboardMarkup(keyboard=user_buttons)
