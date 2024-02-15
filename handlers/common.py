from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from create import bot
from keyboards.keyboards import start_markup
from messages.messages import MESSAGES

common = Router()

#---------common commands---------
@common.callback_query(F.data=="exit")
@common.message(Command("start"))
async def start_command(msg: Message, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=msg.from_user.id,
                           text=MESSAGES["hello"],
                           reply_markup=start_markup)

@common.message(Command("cancel"))
async def cancel_command(msg: Message, state: FSMContext):
    await state.clear()
    await bot.send_message(chat_id=msg.from_user.id,
                           text=MESSAGES["cancel"])
    await start_command(msg, state)