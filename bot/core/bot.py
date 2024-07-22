import asyncio
import logging
import sys

from decouple import config as env
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.services.fetch_rates import schedule_updates
from bot.handlers import add_handlers


TOKEN = env("BOT_TOKEN")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    add_handlers(dp)
    await schedule_updates()
    await dp.start_polling(bot)


def run_bot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
