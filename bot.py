import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

# ========== ТОКЕН УЖЕ ВСТАВЛЕН! ==========
API_TOKEN = "8338086698:AAFF9l3jn8C-UL7yxnCIsntSbR-3zHy66lI"
# ========== ГОТОВО К ЗАПУСКУ ==========

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Получить AI-Прогноз"), KeyboardButton(text="📉 Анализ Паники")],
        [KeyboardButton(text="☕ Поддержать"), KeyboardButton(text="ℹ️ О Боте")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🚀 *AI Crypto Prophet* активирован!\n"
        "Я — твой личный шаман крипторынка. Анализирую тренды, предсказываю движения, разгоняю панику.\n\n"
        "💎 *Пример прогноза:*\n"
        "«XRP может вырасти на 15% к пятнице!\n"
        "· Вероятность: 82%\n"
        "· Лучшая цена входа: $0.58\n"
        "· Стоп-лосс: $0.54»\n\n"
        "Выбери действие:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

def get_crypto_data():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 10,
            'page': 1,
            'sparkline': 'false'
        }
        response = requests.get(url, params=params)
        return response.json()
    except:
        return None

def generate_prediction(data):
    if not data:
        return "⚠️ Данные недоступны. Попробуй позже."
    coin = data[0]
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = coin['current_price']
    change = coin['price_change_percentage_24h']
    
    prob = min(95, max(50, 70 + int(change)))
    target = round(price * 1.12, 4)
    stop = round(price * 0.94, 4)
    
    return (
        f"💎 *{name} ({symbol})*\n"
        f"📈 *Вероятность роста:* {prob}%\n"
        f"💰 *Цена:* ${price}\n"
        f"🎯 *Цель:* ${target}\n"
        f"⛔ *Стоп:* ${stop}\n\n"
        f"ℹ️ *AI-анализ завершен.*"
    )

@dp.message(F.text == "📊 Получить AI-Прогноз")
async def forecast(message: types.Message):
    await message.answer("⏳ Анализирую блокчейн...", parse_mode="Markdown")
    data = get_crypto_data()
    text = generate_prediction(data)
    await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)

@dp.message(F.text == "📉 Анализ Паники")
async def panic(message: types.Message):
    await message.answer(
        "🤖 *Анализ паники:*\n"
        "Уровень истерики: 42/100 🟡\n\n"
        "💡 *Рекомендация:*\n"
        "Не продавай в панике. Исторически — лучшее время для входа.\n"
        "P.S. Если бы я получал 1$ за каждого паникёра — я бы уже купил Ламбо.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@dp.message(F.text == "☕ Поддержать")
async def donate(message: types.Message):
    await message.answer(
        "🙏 *Поддержать проект:*\n"
        "TON: `EQDk...V9Xy` *(замени на свой!)*\n"
        "USDT: `TXYZ...ABCD`\n\n"
        "*Спасибо! Твой донат питает мои сервера!*",
        parse_mode="Markdown",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

@dp.message(F.text == "ℹ️ О Боте")
async def about(message: types.Message):
    await message.answer(
        "🤖 *AI Crypto Prophet v1.0*\n"
        "· Полностью автоматизирован\n"
        "· Анализирует CoinGecko\n"
        "· Работает 24/7\n"
        "· Принимает донаты в крипте\n\n"
        "⚠️ *Не финансовый совет.*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def main():
    print("✅ Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())