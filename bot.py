import asyncio
import re
import aiohttp

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message


TOKEN = "8774119980:AAHlaUIms9JmLVWo3Rerc5ZK7nEc5ilRjGs"


bot = Bot(token=TOKEN)
dp = Dispatcher()


# Получаем актуальный курс валюты
async def get_rate(base: str) -> dict:
    url = f"https://open.er-api.com/v6/latest/{base}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            if data.get("result") != "success":
                raise Exception("Ошибка API")

            return data["rates"]


# Команда /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "💱 Бот-конвертер валют\n\n"
        "Напишите сумму и валюту.\n\n"
        "Например:\n"
        "100 USD\n"
        "50 EUR RUB\n"
        "100 USD → EUR\n"
        "100 USD в EUR"
    )


# Обрабатываем конвертацию
@dp.message(F.text.regexp(
    r"^\s*(\d+(?:[.,]\d+)?)\s*([A-Za-z]{3})\s*(?:→|->|в)?\s*([A-Za-z]{3})?\s*$"
))
async def convert(message: Message):

    # Получаем данные из сообщения
    match = re.match(
        r"^\s*(\d+(?:[.,]\d+)?)\s*([A-Za-z]{3})\s*(?:→|->|в)?\s*([A-Za-z]{3})?\s*$",
        message.text,
    )

    if not match:
        return

    # Сумма
    amount = float(
        match.group(1).replace(",", ".")
    )

    # Исходная валюта
    base = match.group(2).upper()

    # Валюта, в которую переводим
    # Если пользователь её не указал — RUB
    target = (match.group(3) or "RUB").upper()

    try:
        # Получаем свежие курсы
        rates = await get_rate(base)

    except Exception:
        await message.answer(
            "❌ Не удалось получить курс валют.\n"
            "Попробуйте ещё раз позже."
        )
        return

    # Проверяем существование валюты
    if target not in rates:
        await message.answer(
            f"❌ Валюта {target} не найдена."
        )
        return

    # Получаем курс
    rate = rates[target]

    # Считаем результат
    result = amount * rate

    # Отправляем ответ
    await message.answer(
        f"💱 Конвертация\n\n"
        f"{amount:g} {base} = {result:,.2f} {target}\n\n"
        f"📊 Курс:\n"
        f"1 {base} = {rate:g} {target}"
    )


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())