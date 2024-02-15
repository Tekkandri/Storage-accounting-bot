from aiogram.types import BotCommand
from create import bot

async def set_commands():
    commands = [
        BotCommand(command="admin",
                   description="Админ-панель"),
        BotCommand(command="start",
                   description="Начало работы"),
        BotCommand(command="cancel",
                   description="Сбросить"),
    ]

    await bot.set_my_commands(commands)