from time import time
import asyncio

import aiohttp
import xml.etree.ElementTree as ET
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.core.redis import redis_client


async def fetch_xml_data(url: str) -> ET.Element:
    """Retrieve XML from a URL"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            xml_content = await response.text()
            root = ET.fromstring(xml_content)
            return root


async def update_rates() -> None:
    """Get all of the rates from cbr.ru and save them into redis"""

    url = "https://cbr.ru/scripts/XML_daily.asp"
    root = await fetch_xml_data(url)

    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode").text
        value = valute.find("VunitRate").text
        value = value.replace(",", ".")
        redis_client.set(f"rates:{char_code}", value)


async def schedule_updates():
    """
    Run a scheduler for updating the rates every day.
    Also runs one update immediately.
    """

    # Run immediately
    asyncio.create_task(update_rates())

    scheduler = AsyncIOScheduler()
    scheduler.add_job(update_rates, IntervalTrigger(days=1))
    scheduler.start()
