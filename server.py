# main.py
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# Хардкодим токен прямо здесь
API_TOKEN = '6886721825:AAGXSUyM9eNOS09tUPAvU-Oe4x_fMWx2E1o'

from messages import PROBLEM_MESSAGE, HELP_MESSAGE, NOT_TEXT_MESSAGE, BAD_TEXT_MESSAGE
from keyboards import kb, kb_statistic

# Импорт утилит и базы данных
from utils import Filter, STATISTIC_TIME
from sqlite import db_create
from utils_db import db_is_ready, get_limit, set_limit, set_cost, get_statistic, del_cost

# Настройка логирования
file_log = logging.FileHandler("log.log")
console_out = logging.StreamHandler()
logging.basicConfig(handlers=(file_log, console_out),
                    level=logging.ERROR,
                    format="%(asctime)s %(levelname)s |  %(lineno)d %(funcName)s: %(message)s")

# Создание объектов бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Выполнение при запуске
async def on_startup(_):
    await db_create()
    print('___Бот запустился!___')

# Обработка команды 'start'
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    try:
        await db_is_ready(message)
        await cmd_help_kb(message=message)
        await cmd_main_kb(message=message)
    except Exception as e:
        await message.answer(text=PROBLEM_MESSAGE, reply_markup=kb)

# Обработка кнопки 'Главное меню'
@dp.message_handler(Text(equals='🏠Главное меню'))
async def cmd_main_kb(message: types.Message) -> None:
    await message.answer(text="📝Напишите мне свои расходы", reply_markup=kb)
    await message.delete()

# Обработка кнопки 'Статистика'
@dp.message_handler(Text(equals='📜Статистика'))
async def cmd_statistic_kb(message: types.Message) -> None:
    await message.answer(text="☑️Выбери нужную статистику", reply_markup=kb_statistic)
    await message.delete()

# Обработка кнопки 'Помощь'
@dp.message_handler(Text(equals='🆘Помощь'))
async def cmd_help_kb(message: types.Message) -> None:
    await message.answer(text=HELP_MESSAGE, parse_mode="HTML", reply_markup=kb)

# Обработка сообщений для установки лимита на расходы
@dp.message_handler(lambda message: Filter.is_handler_limit(message.text))
async def cmd_set_limit(message: types.Message) -> None:
    await set_limit(message)

# Обработка сообщений для сохранения расходов
@dp.message_handler(lambda message: Filter.is_handler_cost(message.text))
async def cmd_set_cost(message: types.Message) -> None:
    await set_cost(message)

# Обработка сообщений для удаления расходов
@dp.message_handler(lambda message: message.text.startswith('/del'))
async def cmd_del_cost(message: types.Message) -> None:
    await del_cost(message)

# Обработка сообщений для отправки статистики
@dp.message_handler(lambda message: message.text in STATISTIC_TIME)
async def cmd_send_statistic(message: types.Message) -> None:
    await get_statistic(message)
    await message.delete()

# Обработка невалидных сообщений
@dp.message_handler(content_types=types.ContentType.ANY)
async def cmd_exceptions(message: types.Message) -> None:
    text = BAD_TEXT_MESSAGE if message.text else NOT_TEXT_MESSAGE
    await message.reply(text=text, reply_markup=kb)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)









