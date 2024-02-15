from create import dp, bot
from handlers import balance, buy_new_item, common, statistics, admin
from database import sqlite_db
import logging
import asyncio
from utils.commands import set_commands

async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                        filename="logg.log",
                        filemode="w")
    sqlite_db.start_sql()
    dp.startup.register(set_commands)
    dp.include_routers(common.common, balance.balance, buy_new_item.new_item, statistics.stat, admin.admin)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
