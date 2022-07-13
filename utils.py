import re
import requests
import json

from aiogram import types

import database as db


BUTTONS = [
    types.InlineKeyboardButton(text="Обновить ♻️", callback_data="update_stats"),
    types.InlineKeyboardButton(
        text="Сменить кошелёк ⚙️", callback_data="change_wallet"
    ),
]


def get_hashrate(wallet: str) -> str:
    stats_url = "https://stats.ezil.me/current_stats/"

    r = requests.get(stats_url + wallet)
    data = json.loads(r.text)
    cur_hashrate = data["eth"]["current_hashrate"] // 1000000

    return f"{cur_hashrate} MH/s"


def get_balance(wallet: str) -> str:
    balance_url = "https://billing.ezil.me/v2/accounts/"

    r = requests.get(balance_url + wallet)
    data = json.loads(r.text)
    for i in data["balances"]:
        if i["coin"] == "eth":
            balance = i["amount"]
            break

    return f"{balance:.{4}f} ETH | {balance*get_price():.{0}f}$ | {balance*get_price(currency='RUB'):.{0}f}₽"


def get_price(token: str = "ETH", currency: str = "USD") -> float:
    prices_url = "https://billing.ezil.me/rates"

    r = requests.get(prices_url)
    data = json.loads(r.text)

    return data[token][currency]


def check_state(user_id: int, state: str) -> bool:
    result = db.fetchone("users", user_id, "state")
    return state in result


def wallet_correct(wallet: str) -> bool:
    eth_zil_pattern = r"0x\w{40}\.zil\w{39}"
    eth_pattern = r"0x\w{40}"

    eth_zil_match = re.fullmatch(eth_zil_pattern, wallet)
    eth_match = re.fullmatch(eth_pattern, wallet)

    return True if (eth_zil_match or eth_match) else False
