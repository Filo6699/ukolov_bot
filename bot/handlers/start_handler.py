from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message


router = Router()
start_message = """
*Хеллоу!*

Добро пожаловать в CurrencyBot.
Это бот для работы с валютами и их обменом.

`/rates` - Посмотреть все курсы валют
`/exchange` - Обменять одну валюту на другую

_Бот создан по ТЗ от ИП Уколов Артем Витальевич_
_Разработчик:_ [Filo](tg://user?id=1820156564)
"""


@router.message(Command(commands=["start"]))
async def start_handler(message: Message) -> None:
    """
    Handles `/start` command.
    """
    await message.answer(start_message)
