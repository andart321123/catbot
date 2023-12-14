from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_buttons = [[KeyboardButton(text=' 😺КОШКИ! 🐈')], [KeyboardButton(text='😼 ШЛЁПА И ПЕЛЬМЕНИ 🕹️')],
				[KeyboardButton(text='📰 НОВОСТИ 📝')]]

admin_buttons = [[KeyboardButton(text='😺 КОШКИ! 🐈'), KeyboardButton(text='📃 СПИСОК КОШЕК 😸')],
				 [KeyboardButton(text='😼 ШЛЁПА И ПЕЛЬМЕНИ 🕹️')],
				 [KeyboardButton(text='📰 НОВОСТИ 📝')]]

root_buttons = admin_buttons.copy()
root_buttons[2].append(KeyboardButton(text='🙀 АДМИНИСТРАТОРЫ 🐶'))

root_kb = ReplyKeyboardMarkup(keyboard=root_buttons)
admin_kb = ReplyKeyboardMarkup(keyboard=admin_buttons)
user_kb = ReplyKeyboardMarkup(keyboard=user_buttons)
