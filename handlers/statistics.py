import datetime
import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from database import sqlite_db
from create import bot
from messages.messages import MESSAGES
from keyboards.keyboards import stat_markup, month_item_markup, common_markup, month_money_markup
from config import tz

stat = Router()

@stat.callback_query(F.data=="stat")
async def get_stat_info(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES["stat"],
                           reply_markup=stat_markup)
    await cb.answer()

@stat.callback_query(F.data=="month_item_stat")
async def choose_month_item_stat(cb: CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES['month_stat'],
                           reply_markup=month_item_markup)
    await cb.answer()

@stat.callback_query(F.data=="month_money_stat")
async def choose_month_money_stat(cb:CallbackQuery):
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES['month_stat'],
                           reply_markup=month_money_markup)
    await cb.answer()

@stat.callback_query(F.data=="day_item_stat")
async def get_day_item_stat(cb: CallbackQuery):
    data = sqlite_db.get_day_item_stat()
    text = ""
    document = FSInputFile(f"Дневная статистика {datetime.datetime.now(tz=tz).date()}.xlsx")
    for key, item in data.items():
        text +=f"# {key} -- {str(item[0])} -- {str(item[1])} руб.\n"
    await bot.send_document(chat_id=cb.from_user.id,
                            document=document,
                            caption=text,
                            reply_markup=common_markup)
    os.remove(f"Дневная статистика {datetime.datetime.now(tz=tz).date()}.xlsx")
    await cb.answer()

@stat.callback_query(F.data.endswith("_item"))
async def get_month_item_stat(cb: CallbackQuery):
    data = sqlite_db.get_month_item_stat(int(cb.data.split("_")[0]), int(cb.data.split("_")[1]))
    text = ""
    document = FSInputFile(f"Месячная статистика {datetime.datetime.now(tz=tz).date()}.xlsx")
    for key, item in data.items():
        text += f"# {key} -- {str(item[0])} -- {str(item[1])} руб.\n"
    await bot.send_document(chat_id=cb.from_user.id,
                            document=document,
                            caption=text,
                            reply_markup=common_markup)
    os.remove(f"Месячная статистика {datetime.datetime.now(tz=tz).date()}.xlsx")
    await cb.answer()

@stat.callback_query(F.data.endswith("_money"))
async def get_month_item_stat(cb: CallbackQuery):
    data = sqlite_db.get_balance_hist(int(cb.data.split("_")[0]), int(cb.data.split("_")[1]))
    await bot.send_message(chat_id=cb.from_user.id,
                           text=f"Общая сумма пополнений за месяц: {str(data['data'][1])} руб.",
                           reply_markup=common_markup)
    os.remove(f"Баланс {datetime.datetime.now(tz=tz).date()}.xlsx")
    await cb.answer()