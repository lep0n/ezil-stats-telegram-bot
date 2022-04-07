import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from utils import *

import database as db


logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.callback_query_handler(text="update_stats")
async def send_updated_stats(call: types.CallbackQuery):
    """Handle update_stats inline button"""

    wallet = db.fetchone('users', call.message.chat.id, 'wallet')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*BUTTONS)

    await call.message.answer(
        f"<b>Ваш баланс:</b> {get_balance(wallet)}\n\n"
        f"<b>Текущий хешрейт:</b> {get_hashrate(wallet)}\n\n"
        f"📊 <b>ETH:</b> {get_price('ETH', 'USD'):.{0}f}$ | {get_price('ETH', 'RUB'):.{0}f}₽",
        reply_markup=keyboard)


@dp.callback_query_handler(text="change_wallet")
async def send_change_wallet(call: types.CallbackQuery):
    """Handle change_wallet inline button"""
    
    db.update("users", call.message.chat.id, {
        "state": "wait_wallet"
    })

    await call.message.answer("Отправьте новый адрес кошелька, который Вы хотите привязать.")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """Send welcome message and request wallet if this is a new user"""

    if {"user_id": message.chat.id} not in db.fetchall("users", ["user_id"]):
        db.insert("users", {
            "user_id": message.chat.id,
            "state": "wait_wallet"
        })

        await message.answer(
            f"Привет!👋\n"
            f"Отправьте адрес кошелька, который Вы используете на ezil.me")

    else:
        wallet = db.fetchone('users', message.chat.id, 'wallet')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*BUTTONS)

        await message.answer(
            f"<b>Ваш баланс:</b> {get_balance(wallet)}\n\n"
            f"<b>Текущий хешрейт:</b> {get_hashrate(wallet)}\n\n"
            f"📊 <b>ETH:</b> {get_price('ETH', 'USD'):.{0}f}$ | {get_price('ETH', 'RUB'):.{0}f}₽",
            reply_markup=keyboard)


@dp.message_handler(lambda message: check_state(message.chat.id, "wait_wallet"))
async def send_stats(message: types.Message):
    """Save wallet to DB and send stats from ezil.me"""

    if wallet_correct(message.text):
        db.update("users", message.chat.id, {
            "wallet": message.text,
            "state": "connected"
        })

        wallet = db.fetchone('users', message.chat.id, 'wallet')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*BUTTONS)

        await message.answer("Отлично! В будущем Вы можете сменить кошелёк 😉")
        await message.answer(
            f"<b>Ваш баланс:</b> {get_balance(wallet)}\n\n"
            f"<b>Текущий хешрейт:</b> {get_hashrate(wallet)}\n\n"
            f"📊 <b>ETH:</b> {get_price('ETH', 'USD'):.{0}f}$ | {get_price('ETH', 'RUB'):.{0}f}₽",
            reply_markup=keyboard)

    else:
        await message.answer(
            'К сожалению, формат кошелька неверный😔\n'
            'Кошелек должен быть в формате <b>"ETH.ZIL"</b> или просто <b>"ETH"</b>\n\n'
            'Попробуйте снова!\n')


@dp.message_handler(commands=['delete'])
async def delete_user(message: types.Message):
    """Delete user info from DB"""

    db.delete("users", message.chat.id)
    await message.answer("✅ Ваши данные успешно удалены!")


@dp.message_handler(lambda message: check_state(message.chat.id, "connected"))
async def delete_all(message: types.Message):
    """Delete all user messages if they were not handled before"""

    await message.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
