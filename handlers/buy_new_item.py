from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database import sqlite_db
from create import bot
from utils.states import FSMstates
from keyboards.keyboards import confirm_markup, common_markup, \
    common_and_continue_markup, confirm_and_continue_markup, build_item_markup
from messages.messages import MESSAGES


new_item = Router()

def is_num(msg: str) -> bool:
    try:
        int(msg)
        return True
    except ValueError:
        return False

@new_item.callback_query(F.data=="buy_new_item")
async def choose_category(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.BUY_NEW_ITEM)
    await state.update_data(cb_data=[],
                            count=[],
                            other=[],
                            sum=[])
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES["category"],
                           reply_markup=build_item_markup())
    await cb.answer()

@new_item.callback_query(FSMstates.GET_COUNT,F.data=="continue")
async def add_category(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.BUY_NEW_ITEM)
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES["category"],
                           reply_markup=build_item_markup())
    await cb.answer()

@new_item.callback_query(FSMstates.BUY_NEW_ITEM, F.data.endswith("::cat"))
async def get_count(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.GET_COUNT)
    user_data = await state.get_data()
    user_data['cb_data'].append(cb.data.split("::")[0])
    user_data['other'].append(False)
    user_data["sum"].append("0")
    await state.update_data(cb_data=user_data['cb_data'],
                            other=user_data['other'],
                            sum=user_data['sum'])
    await bot.send_message(chat_id=cb.from_user.id,
                           text=MESSAGES["count"])
    await cb.answer()

@new_item.callback_query(FSMstates.BUY_NEW_ITEM, F.data=="other")
async def get_other_items(cb: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Отправьте содержание всех покупок")
    await state.set_state(FSMstates.GET_OTHER_ITEMS)
    await cb.answer()

@new_item.message(FSMstates.GET_OTHER_ITEMS)
async def get_other_items_count(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["cb_data"].append(msg.text)
    user_data["other"].append(True)
    await state.update_data(cb_data=user_data['cb_data'],
                            other=user_data['other'])
    await bot.send_message(chat_id=msg.from_user.id,
                           text="Отправьте сумму купленного товара")
    await state.set_state(FSMstates.GET_OTHER_ITEMS_SUM)

@new_item.message(FSMstates.GET_COUNT)
async def confirm_count(msg: Message, state: FSMContext):
    if is_num(msg.text):
        user_data = await state.get_data()
        user_data['count'].append(int(msg.text))
        await state.update_data(count=user_data['count'])
        all_purchases = 0
        for i in range(len(user_data['cb_data'])):
            if user_data["other"][i]:
                all_purchases+=int(user_data["sum"][i])
            else:
                price = sqlite_db.get_price(user_data['cb_data'][i]) * user_data['count'][i]
                all_purchases += price
        await bot.send_message(chat_id=msg.from_user.id,
                               text=f"Категории: {', '.join(user_data['cb_data'])}\r\n"
                                    f"Количество: {', '.join([str(i) for i in user_data['count']])}\r\n"
                                    f"Сумма: {all_purchases} ₽",
                               reply_markup=confirm_and_continue_markup)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Введите число правильно")

@new_item.callback_query(FSMstates.GET_COUNT, F.data=="confirm_action")
async def get_auto(cb: CallbackQuery, state: FSMContext):
    await state.set_state(FSMstates.GET_AUTO)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Введите номер автомобиля:\n"
                                "Если вы покупаете только товары из категории 'Другие' - ставьте прочерк")
    await cb.answer()

@new_item.message(FSMstates.GET_AUTO)
async def confirm_data(msg: Message, state: FSMContext):
    await state.update_data(auto=msg.text)
    user_data = await state.get_data()
    all_purchases = 0
    for i in range(len(user_data['cb_data'])):
        if user_data["other"][i]:
            all_purchases += int(user_data["sum"][i])
        else:
            price = sqlite_db.get_price(user_data['cb_data'][i]) * user_data['count'][i]
            all_purchases += price
    await bot.send_message(chat_id=msg.from_user.id,
                           text=f"Категории: {','.join(user_data['cb_data'])}\r\nКоличество: "
                                f"{', '.join([str(i) for i in user_data['count']])}\r\n"
                                f"Сумма: {all_purchases} ₽\r\n"
                                f"Номер автомобиля: {user_data['auto']}",
                           reply_markup=confirm_markup)

@new_item.callback_query(FSMstates.GET_AUTO, F.data=="confirm_action")
async def set_to_db(cb: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    balance = sqlite_db.get_balance()
    all_purchases = 0
    for i in range(len(user_data['cb_data'])):
        if user_data["other"][i]:
            all_purchases+=int(user_data["sum"][i])
            sqlite_db.set_new_purchase(user_data['cb_data'][i], user_data['count'][i], user_data["sum"][i], user_data['auto'], 0)
        else:
            price = sqlite_db.get_price(user_data['cb_data'][i]) * user_data['count'][i]
            all_purchases += price
            sqlite_db.set_new_purchase(user_data['cb_data'][i], user_data['count'][i], price, user_data['auto'],1)
    sqlite_db.set_new_balance(balance - all_purchases)
    await bot.send_message(chat_id=cb.from_user.id,
                           text="Запись успешна",
                           reply_markup=common_markup)
    await state.clear()
    await cb.answer()

#---------other items---------

@new_item.message(FSMstates.GET_OTHER_ITEMS_SUM)
async def get_other_items_sum(msg: Message, state: FSMContext):
    if is_num(msg.text):
        user_data = await state.get_data()
        user_data["sum"].append(msg.text)
        await state.update_data(sum=user_data["sum"])
        await bot.send_message(chat_id=msg.from_user.id,
                               text=MESSAGES["count"])
        await state.set_state(FSMstates.GET_COUNT)
    else:
        await bot.send_message(chat_id=msg.from_user.id,
                               text="Введите число правильно")
