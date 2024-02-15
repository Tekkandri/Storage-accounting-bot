import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from database import sqlite_db
from create import bot
from messages.messages import MESSAGES
from utils.states import FSMstates
from keyboards.keyboards import confirm_markup,common_and_continue_markup, common_markup, \
    get_admin_markup, category_markup, main_admin_markup
from config import PASSWORD

admin = Router()

def is_num(msg: str) -> bool:
    try:
        int(msg)
        return True
    except ValueError:
        return False

@admin.message(Command("admin"))
async def admin_pass(msg: Message, state: FSMContext):
    await state.set_state(FSMstates.ADMIN_PASS_STATE)
    await bot.send_message(chat_id=msg.from_user.id,
                           text="Введите пароль для доступа")

@admin.message(FSMstates.ADMIN_PASS_STATE)
async def main_admin_menu(msg: Message, state: FSMContext):
    if msg.text == PASSWORD:
        await state.set_state(FSMstates.ADMIN_STATE)
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Возможные действия:",
                               reply_markup=main_admin_markup)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Пароль неверный")

@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="back_to_main_menu")
async def main_admin_menu(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Возможные действия:",
                           reply_markup=main_admin_markup)
    await cb.answer()

@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="check_categories")
async def choose_category(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Выберите категорию товара:",
                           reply_markup=get_admin_markup())
    await cb.answer()

@admin.callback_query(FSMstates.GET_PRICE, F.data=="continue")
async def choose_category(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.ADMIN_STATE)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Выберите категорию товара:",
                           reply_markup=get_admin_markup())
    await cb.answer()

@admin.callback_query(FSMstates.ADMIN_STATE, F.data.endswith("::cat"))
async def get_new_price(cb: CallbackQuery, state: FSMContext):
    await state.update_data(category=cb.data.split("::")[0])
    await state.set_state(FSMstates.CATEGORY)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Выберите действие",
                           reply_markup=category_markup)
    await cb.answer()

@admin.callback_query(FSMstates.CATEGORY, F.data=="change_price")
async def change_price(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.GET_PRICE)
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES["price"])
    await cb.answer()

@admin.message(FSMstates.GET_PRICE)
async def confirm_price(msg: Message, state: FSMContext):
    if is_num(msg.text):
        await state.update_data(price=int(msg.text))
        user_data = await state.get_data()
        await bot.send_message(chat_id=msg.from_user.id,
                               text=f"Категория: {user_data['category']}\r\nЦена за единицу:{str(user_data['price'])}",
                               reply_markup=confirm_markup)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Введите число правильно")

@admin.callback_query(FSMstates.GET_PRICE, F.data=="confirm_action")
async def set_to_db(cb: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    sqlite_db.set_new_price(user_data['category'], user_data['price'])
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Запись обновлена",
                           reply_markup=common_and_continue_markup)
    await cb.answer()

#---------delete purchase----------
@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="delete")
async def delete_purchase(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.DELETE_PURCHASE_STATE)
    sqlite_db.get_all()
    document = FSInputFile("Выгрузка.xlsx")
    await bot.send_document(chat_id=cb.from_user.id,
                            document=document,
                            caption="Если необходимо, отредактируйте файл и отправьте в чат")
    os.remove("Выгрузка.xlsx")
    await cb.answer()

@admin.message(FSMstates.DELETE_PURCHASE_STATE, F.document)
async def set_new_db(msg: Message):
    # try:
        await bot.download(msg.document,
                       destination=f"./database/{msg.document.file_id}.xlsx")
        sqlite_db.set_new_db(f"./database/{msg.document.file_id}.xlsx")
        await bot.send_message(chat_id=msg.from_user.id,
                           text="Запись обновлена",
                           reply_markup=common_markup)
        os.remove(f"./database/{msg.document.file_id}.xlsx")
    # except:
    #     await bot.send_message(chat_id=msg.from_user.id,
    #                            text="Некорректный файл")
#-----------------------------------
#----------change balance----------
@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="change_balance_hist")
async def delete_purchase(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.CHANGE_BALANCE_HIST)
    sqlite_db.get_all_balance_hist()
    document = FSInputFile("Выгрузка баланс.xlsx")
    await bot.send_document(chat_id=cb.from_user.id,
                            document=document,
                            caption="Если необходимо, отредактируйте файл и отправьте в чат")
    os.remove("Выгрузка баланс.xlsx")
    await cb.answer()

@admin.message(FSMstates.CHANGE_BALANCE_HIST, F.document)
async def set_new_db(msg: Message):
    # try:
        await bot.download(msg.document,
                       destination=f"./database/{msg.document.file_id}.xlsx")
        sqlite_db.set_new_balance_db(f"./database/{msg.document.file_id}.xlsx")
        await bot.send_message(chat_id=msg.from_user.id,
                           text="Запись обновлена",
                           reply_markup=common_markup)
        os.remove(f"./database/{msg.document.file_id}.xlsx")
    # except:
    #     await bot.send_message(chat_id=msg.from_user.id,
    #                            text="Некорректный файл")

@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="change_current_balance")
async def get_new_current_balance(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Введите новую сумму:")
    await state.set_state(FSMstates.CHANGE_CUR_BALANCE)
    await cb.answer()

@admin.message(FSMstates.CHANGE_CUR_BALANCE)
async def set_new_current_balance(msg: Message, state: FSMContext):
    if is_num(msg.text):
        sqlite_db.set_new_balance(int(msg.text))
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Баланс обновлён",
                               reply_markup=common_markup)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Отправьте корректное число")
#-----------------------------------
#---------add new category----------
@admin.callback_query(FSMstates.ADMIN_STATE, F.data=="add_category")
async def add_category(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Отправьте название категории:")
    await state.set_state(FSMstates.GET_CATEGORY_NAME)
    await cb.answer()

@admin.message(FSMstates.GET_CATEGORY_NAME)
async def get_category_name(msg: Message, state: FSMContext):
    sqlite_db.add_category(msg.text)
    await state.update_data(category=msg.text)
    await bot.send_message(chat_id=msg.from_user.id,
                           text=MESSAGES["price"])
    await state.set_state(FSMstates.GET_PRICE)

#---------delete category----------
@admin.callback_query(FSMstates.CATEGORY, F.data=="delete_category")
async def delete_category(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sqlite_db.delete_category(data["category"])
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Категория удалена",
                           reply_markup=common_and_continue_markup)
    await state.set_state(FSMstates.GET_PRICE)
    await cb.answer()