from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура главного меню
kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('📜Статистика')],
    [KeyboardButton('🆘Помощь')]
])

# Клавиатура выбора периода статистики
kb_statistic = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('📜 Дневная'), KeyboardButton('📜 Месячная')],
    [KeyboardButton('📜 Годовая'), KeyboardButton('🏠Главное меню')]
])

# Клавиатура для перехода в главное меню
kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main.add(KeyboardButton('🏠Главное меню'))
