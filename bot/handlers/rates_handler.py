from random import choice, randint
from time import time as now

from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message

from bot.core.redis import (
    redis_client,
    get_all_rates,
    get_rate,
)


router = Router()


def float_to_str(value: float) -> str:
    """
    Better float to str, than str().
    
    Rounds up the float and removes zero's at the end, if present.
    """

    # rstrip'ы разделены, потому-что в случае "10.00" они бы скушали всё и вышло бы "1".
    return f"{value:.4f}".rstrip("0").rstrip(".")


@router.message(Command(commands=["rates"]))
async def rates_handler(message: Message) -> None:
    """
    Handles `/rates` command. Outputs stored rates of currencies from Redis.
    """

    rates = get_all_rates()
    output = "*Rates*\n\n"
    for charcode, unitval in rates.items():
        charcode = charcode[6:] # удаление "rates:"
        if charcode == "RUB":
            continue
        value = float_to_str(unitval)
        output += f"{charcode} = `{value}` RUB\n"

    await message.answer(output)


@router.message(Command(commands=["exchange"]))
async def exchange_handler(message: Message) -> None:
    """
    Handles `/exchange` command. Exchanges one currency into another.

    Usage: `/exchange <cur_from> <cur_to> <quantity>`
    """

    args = message.text.upper().split(" ")

    if len(args) != 4:
        await message.answer(
            "❌ *Incorrect usage*\n\nUsage: `/exchange <cur_from> <cur_to> <quantity>`"
        )
        return

    cur_from = get_rate(args[1])
    cur_to = get_rate(args[2])

    if cur_from == None:
        await message.answer(f"❌ {cur_from} is not a valid charcode.")
        return
    if cur_to == None:
        await message.answer(f"❌ {cur_to} is not a valid charcode.")
        return

    try:
        quantity = float(args[3])
    except ValueError:
        await message.answer("❌ Not a valid number")
        return
    quantity_str = float_to_str(quantity)

    exchanged_value = (cur_from * quantity) / cur_to
    exchanged_value_str = float_to_str(exchanged_value)

    answer = f"✅ Exchanged\n\n`{quantity_str}` {args[1]} = `{exchanged_value_str}` {args[2]}"
    await message.answer(answer)
