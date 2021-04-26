import asyncio
from aiogram import executor
from tortoise import Tortoise
import aioschedule

from tg_bot.load_all import bot
from tg_bot.modules.API_to_DB import update_regions, update_categories, update_forms


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()
    # inst_bot.logout()


async def on_startup(dp):
    print("!!!!!!!!!!!!!1STARTING!!!!!!!!!!!!!!!!!!")
    asyncio.create_task(scheduler())


async def scheduler():
    aioschedule.every(1).minutes.do(update_regions)
    aioschedule.every(1).minutes.do(update_categories)
    aioschedule.every(1).minutes.do(update_forms)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

from tg_bot.dialogs.chats.handlers import dp
from tg_bot.dialogs.admin.handlers import dp
executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
