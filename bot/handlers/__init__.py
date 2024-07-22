from aiogram import Dispatcher

from bot.handlers import start_handler, rates_handler


def add_handlers(dp: Dispatcher):
    """Adds handlers from `handlers/` folder to provided dispatcher."""

    dp.include_router(start_handler.router)
    dp.include_router(rates_handler.router)
