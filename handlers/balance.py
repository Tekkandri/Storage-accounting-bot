import datetime
import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from database import sqlite_db
from create import bot
from utils.states import FSMstates
from keyboards.keyboards import new_balance_markup, common_markup
from config import PASSWORD, tz

balance = Router()

def is_num(msg: str) -> bool:
    try:
        int(msg)
        return True
    except ValueError:
        return False

@balance.callback_query(F.data=="balance_info")
async def get_balance_info(cb: CallbackQuery):
    cur_balance = sqlite_db.get_balance()
    hist_balance = sqlite_db.get_balance_hist(datetime.datetime.now(tz=tz).month, datetime.datetime.now(tz=tz).year)["data"][0]
    document = FSInputFile(f"Баланс {datetime.datetime.now(tz=tz).date()}.xlsx")
    await bot.send_document(chat_id=cb.from_user.id,
                            document=document,
                            caption=f"""Ваш баланс {cur_balance} руб.\r\nИстория пополнений:{hist_balance}""",
                            reply_markup=common_markup)
    os.remove(f"Баланс {datetime.datetime.now(tz=tz).date()}.xlsx")
    await cb.answer()

@balance.callback_query(F.data=="top_up")
async def balance_pass(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.BALANCE_PASS_STATE)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Введите пароль для доступа")
    await cb.answer()

@balance.message(FSMstates.BALANCE_PASS_STATE)
async def top_up_balance(msg: Message, state: FSMContext):
    if msg.text==PASSWORD:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Введите сумму")
        await state.set_state(FSMstates.GET_NUM)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Пароль неверный")

@balance.message(FSMstates.GET_NUM)
async def get_num_from_message(msg: Message, state: FSMContext):
    if is_num(msg.text):
        await state.update_data(sum=int(msg.text))
        await bot.send_message(chat_id=msg.from_user.id,
                         text=f"Сумма: {msg.text} руб.",
                         reply_markup=new_balance_markup)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                         text="Введите число правильно")

@balance.callback_query(FSMstates.GET_NUM, F.data=="confirm_top_up")
async def confirm_top_up(cb: CallbackQuery, state:FSMContext):
    new_balance = sqlite_db.get_balance() + (await state.get_data())["sum"]
    sqlite_db.set_new_balance(new_balance)
    sqlite_db.set_balance_hist_line((await state.get_data())["sum"])
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Успешное пополнение",
                           reply_markup=common_markup)
    await state.clear()
    await cb.answer()