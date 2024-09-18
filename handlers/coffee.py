from loguru import logger
from os import remove
from io import BytesIO
from utils.payment import YookassaPayment
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode, hlink

from middlewares import rate_limit
import keyboards as kb



async def get_coffee_list(message: types.Message):
    await message.answer(
        f"{message.from_user.full_name or message.from_user.username}, "
        "\nСпасибо, что ценишь мой труд \nТы можешь дать мне возможность купить сегодня что-то из кнопок ниже⬇️",
        reply_markup=await kb.get_coffee_list(),
    )


async def buy_bread(message: types.Message):
    payment = YookassaPayment(amount=35.0)
    payment.create(message.from_user.id)

    await message.answer(
        "Спасибо, что ценишь мой труд👨‍💻",
        parse_mode=types.ParseMode.HTML,
        reply_markup=await kb.create_new_payment_kb(payment.payment_url, payment.payment_id, True)
    )

    return

async def buy_coffee(message: types.Message):
    payment = YookassaPayment(amount=250.0)
    payment.create(message.from_user.id)

    await message.answer(
        "Спасибо, что ценишь мой труд👨‍💻",
        parse_mode=types.ParseMode.HTML,
        reply_markup=await kb.create_new_payment_kb(payment.payment_url, payment.payment_id, True)
    )

    return

async def buy_cake(message: types.Message):
    payment = YookassaPayment(amount=350.0)
    payment.create(message.from_user.id)

    await message.answer(
        "Спасибо, что ценишь мой труд   ",
        parse_mode=types.ParseMode.HTML,
        reply_markup=await kb.create_new_payment_kb(payment.payment_url, payment.payment_id, True)
    )

    return

async def buy_pirog(message: types.Message):
    payment = YookassaPayment(amount=100.0)
    payment.create(message.from_user.id)

    await message.answer(
        "Спасибо, что ценишь мой труд",
        parse_mode=types.ParseMode.HTML,
        reply_markup=await kb.create_new_payment_kb(payment.payment_url, payment.payment_id, True)
    )

    return

async def sponsors(message: types.Message):
    payment = YookassaPayment(amount=100.0)
    payment.create(message.from_user.id)
    
    await message.answer(
        "😎Люди поддержавшие проект \n\n@web_am - 200р\n@durov - 150р \n\n✅Для поддержки проекта\nТ-банк/Сбер +7(928)555-10-26 \nперевод с текстом 'Поддержка'\n",

                parse_mode=types.ParseMode.HTML,
    
)
    return
