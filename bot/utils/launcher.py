import os
import glob
import asyncio
import argparse
from itertools import cycle

from pyrogram import Client
from better_proxy import Proxy

from bot.config import settings
from bot.utils import logger
from bot.core.tapper import run_tapper
from bot.core.registrator import register_sessions
from data import Data


start_text = """

███╗   ███╗███████╗███╗   ███╗███████╗███████╗██╗██████╗  ██████╗ ████████╗
████╗ ████║██╔════╝████╗ ████║██╔════╝██╔════╝██║██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║█████╗  ██╔████╔██║█████╗  █████╗  ██║██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██╔══╝  ██║██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║███████╗██║ ╚═╝ ██║███████╗██║     ██║██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═════╝  ╚═════╝    ╚═╝                                                                           
"""


def get_proxies() -> list[Proxy]:
    
    
    proxies = []

    with open(file='proxies.txt', encoding='utf-8-sig') as file:
        for line in file:
            proxy = line.strip()  # Remove leading/trailing whitespace
            parts = proxy.split('|')  # Split the line by '|'
            if len(parts) == 2:
                proxies.append(proxy)
    return proxies


async def get_tg_clients() -> list[Data]:

    proxies = get_proxies()
    tg_clients = []
    for proxy in proxies:
        parts = proxy.split('|')
        client = Data(
            name=parts[0],
            proxy=Proxy.from_str(proxy=parts[1]).as_url,
            json_name=parts[0]
        )
        tg_clients.append(client)

    return tg_clients


async def process() -> None:
    tg_clients = await get_tg_clients()
    for client in tg_clients:
        print(f'Proxy: {client.proxy}, JSON Name: {client.json_name}')
    await run_tasks(tg_clients=tg_clients)


async def run_tasks(tg_clients: list[Data]):
    tasks = [asyncio.create_task(run_tapper(tg_client=tg_client, proxy=tg_client.proxy))
        for tg_client in tg_clients]
    await asyncio.gather(*tasks)
