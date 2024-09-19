from loguru import logger
from os import remove
from io import BytesIO
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode, hlink

from middlewares import rate_limit
import keyboards as kb

import database
from loader import bot
from data import configuration
from loader import vpn_config
from database import selector

from utils.payment import YookassaPayment
from utils.fsm import NewConfig
from utils.qr_code import create_qr_code_from_peer_data
from aiogram.utils.exceptions import ChatNotFound

async def cmd_start(message: types.Message) -> types.Message:
    if not message.from_user.username:
        await message.answer(
            f"Привет, {message.from_user.full_name}!\nУ тебя не установлен username, установи его в настройках телеграма и напиши /start\n"
            f"Если не знаешь как это сделать - посмотри {hlink('справку', 'https://silverweb.by/kak-sozdat-nik-v-telegramm/')}",
            parse_mode=types.ParseMode.HTML,
        )
        return
    if database.selector.is_exist_user(message.from_user.id):
        status = database.selector.is_subscription_end(message.from_user.id)
        if status is True:
            await message.answer(
                f"Привет, {message.from_user.full_name or message.from_user.username}, твоя подписка закончилась, оплати её, чтобы продолжить пользоваться VPN",
                reply_markup=await kb.update_user_kb(message.from_user.id),
            )
            return
        elif status is False:
            await message.answer(
                f"Привет, {message.from_user.full_name or message.from_user.username},\n\n👋 Добро пожаловать! \n🤯 Устал от поисков VPN?. \n🚀 Оформи подписку VPN-WEBAM и пользуйся без ограничений\n\n\n🟢 Наши премущества:\n\n✅ Высокая скорость\n✅ Конфиденциальность и приватность\n✅ Доступ к любым сайтам и соц сетям\n\n🔴 Мы не поддерживаем использование VPN для посещения экстремистских ресурсов или запрещенных в РФ веб-сайтов, и не рекомендуем это. \n\n🟢 Наш сервис предназначен для тех, кто ищет безопасный и свободный доступ в интернет, соблюдая все законы и правила России.\n\n",
                reply_markup=await kb.payed_user_kb(),
            )
            return
        else:
            await message.answer(
                f"Привет, {message.from_user.full_name or message.from_user.username},\n\n👋 Добро пожаловать! \n🤯 Устал от поисков VPN?. \n🚀 Оформи подписку VPN-WEBAM и пользуйся без ограничений\n\n\n🟢 Наши премущества:\n\n✅ Высокая скорость\n✅ Конфиденциальность и приватность\n✅ Доступ к любым сайтам и соц сетям \n\n🔴 Мы не поддерживаем использование VPN для посещения экстремистских ресурсов или запрещенных в РФ веб-сайтов, и не рекомендуем это. \n\n🟢 Наш сервис предназначен для тех, кто ищет безопасный и свободный доступ в интернет, соблюдая все законы и правила России.\n\n",
                reply_markup=await kb.free_user_kb(message.from_user.id)
            )
            return

 #тут хотел что бы по команде  cmd_admin выдавался мой профиль клиентам эту команду создал я через бот фазер 
#async def cmd_admin(message: types.Message) -> types.Message:
    #if not message.from_user.username:
        #await message.answer(
           # f"Привет, {message.from_user.full_name}!\nУ тебя не установлен username, установи его в настройках телеграма и напиши /start\n"
           # f"Если не знаешь как это сделать - посмотри {hlink('справку', 'https://silverweb.by/kak-sozdat-nik-v-telegramm/')}",
           # parse_mode=types.ParseMode.HTML,
        #)
    await message.answer(
        f"Привет, {message.from_user.full_name or message.from_user.username},\n\n👋 Добро пожаловать! \n🤯 Устал от поисков VPN?. \n🚀 Оформи подписку VPN-WEBAM и пользуйся без ограничений\n\n\n🟢 Наши премущества:\n\n✅ Высокая скорость\n✅ Конфиденциальность и приватность\n✅ Доступ к любым сайтам и соц сетям\n\n🔴 Мы не поддерживаем использование VPN для посещения экстремистских ресурсов или запрещенных в РФ веб-сайтов, и не рекомендуем это. \n\n🟢 Наш сервис предназначен для тех, кто ищет безопасный и свободный доступ в интернет, соблюдая все законы и правила России.\n\n",
        reply_markup=await kb.free_user_kb(message.from_user.id)
    )

    database.insert_new_user(message)




    # notify admin about new user
    for admin in configuration.admins:
        # format: Новый пользователь: Имя (id: id), username, id like code format in markdown
        try:
            await bot.send_message(
                admin,
                f"Новый пользователь: {hcode(message.from_user.full_name)}\n"
                f"id: {hcode(message.from_user.id)}, username: {hcode(message.from_user.username)}",
                parse_mode=types.ParseMode.HTML,
            )
        except ChatNotFound:
            pass


async def cmd_pay(message: types.Message) -> None:
    match message.text:
        case "✅3 месяц 300р":
            payment_three_months = YookassaPayment(amount=300)
            payment_three_months.create(message.from_user.id)

            await message.answer("После оплаты нажмите на кнопку \n⬇обновить статус платежа⬇",
                parse_mode=types.ParseMode.HTML,
                reply_markup=await kb.create_new_payment_kb(
                    payment_three_months.payment_url, payment_three_months.payment_id, False, 1)
            )
           

        case "✅6 месяц 600р":
            payment_six_months = YookassaPayment(amount=600)
            payment_six_months.create(message.from_user.id)
            await message.answer("После оплаты нажмите на кнопку \n⬇обновить статус платежа⬇",

                parse_mode=types.ParseMode.HTML,
                reply_markup=await kb.create_new_payment_kb(payment_six_months.payment_url, payment_six_months.payment_id, False, 2)
            )
            
            
        case "✅12 месяц 1200р":
            payment_year = YookassaPayment(amount=1200)
            payment_year.create(message.from_user.id)
            await message.answer("После оплаты нажмите на кнопку \n⬇обновить статус платежа⬇",
                parse_mode=types.ParseMode.HTML,
                reply_markup=await kb.create_new_payment_kb(payment_year.payment_url, payment_year.payment_id, False, 3)
                )
          
            
        case "✅1 месяц 100р":
            payment_month = YookassaPayment()
            payment_month.create(message.from_user.id)
            await message.answer("После оплаты нажмите на кнопку \n⬇обновить статус платежа⬇",
                parse_mode=types.ParseMode.HTML,
                reply_markup=await kb.create_new_payment_kb(payment_month.payment_url, payment_month.payment_id, False, 0)
                )
           
            


async def get_payment_buttons(message: types.Message):
    await message.answer("💵 Выберите на сколько хотите оплатить VPN", reply_markup=await kb.get_pay_buttons())



async def check_payment(message: types.CallbackQuery) -> None:
    if message.data[:13] != "check_payment":
        return
    
    command, payment_id, free, time = message.data.split(":")
    free = True if int(free) == 1 else False
    payment = YookassaPayment(payment_id=payment_id)

    if payment.payment_paid is not True:
        await message.answer("Ожидается платёж.")
        return
    
    if free:
        await got_present(message, payment.payment_id)
        await message.message.delete()
        await bot.send_message(
            message.from_user.id,
            "Спасибо, что делаешь меня счастливей!",
            reply_markup=await kb.payed_user_kb()
        )
        return
    
    match int(time):
        case 0:
            date = 30
        case 1:
            date = 90
        case 2:
            date = 180
        case 3:
            date = 365
        case _:
            date = 30

    await message.message.delete()
    await got_payment(message, payment.payment_id, date)
    await successful_payment_handler(message.from_user.id, payment.payment_amount, message, date)


async def got_present(message: types.CallbackQuery, payment_id: str):
    for admin in configuration.admins:
        try:
            await bot.send_message(
                admin,
                f"Пользователь {message.from_user.full_name}\n"
                f"id: {hcode(message.from_user.id)}, username: {hcode(message.from_user.username)},\npayment: {payment_id} подарил деньги.",
                parse_mode=types.ParseMode.HTML,
                reply_markup=None
            )
        except ChatNotFound:
            pass


async def got_payment(message: types.CallbackQuery, payment_id: str, date: int):
    for admin in configuration.admins:
        try:
            await bot.send_message(
                admin,
                f"Пользователь {message.from_user.full_name}\n"
                f"id: {hcode(message.from_user.id)}, username: {hcode(message.from_user.username)},\npayment: {payment_id} оплатил подписку на VPN на {date} дней.",
                parse_mode=types.ParseMode.HTML,
                reply_markup=None
            )
        except ChatNotFound:
            pass

async def successful_payment_handler(user_id: int, amount, message: types.CallbackQuery, date: int):
    database.update_user_payment(user_id, date)
    database.insert_new_payment(user_id, amount)
    if database.selector.is_user_have_config(user_id):
        try:
            await vpn_config.reconnect_payed_user(user_id)
        except Exception as e:
            logger.error(e)

    await message.message.answer(
        f"{message.from_user.full_name or message.from_user.username}, Вы оплатили vpn {database.selector.get_subscription_end_date(user_id)}",
        reply_markup=await kb.payed_user_kb()
    )


async def cmd_my_configs(message: types.Message):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        return

    if database.selector.all_user_configs(message.from_user.id):
        await message.answer(
            "Отображаю твои конфиги на кнопках",
            reply_markup=await kb.configs_kb(message.from_user.id),
        )
    else:
        await message.answer(
            "У тебя нет конфигов",
            reply_markup=await kb.configs_kb(message.from_user.id),
        )


async def cmd_menu(message: types.Message):
    if database.selector.is_subscription_end(message.from_user.id):
        await message.answer(
            "Возвращаю тебя в основное меню",
            reply_markup=await kb.free_user_kb(message.from_user.id),
        )
    else:
        await message.answer(
            "Возвращаю тебя в основное меню", reply_markup=await kb.payed_user_kb()
        )


async def create_new_config(message: types.Message, state=FSMContext):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        await state.finish()
        return

    await message.answer(
        "Для какого устройства ты хочешь создать конфиг?",
        reply_markup=await kb.device_kb(message.from_user.id),
    )
    await NewConfig.device.set()


async def device_selected(call: types.CallbackQuery, state=FSMContext):
    if database.selector.is_subscription_end(call.from_user.id):
        await cmd_start(call.message)
        await state.finish()
        return

    """
    This handler will be called when user presses `pc` or `phone` button
    """
    await state.update_data(device=call.data)
    # edit message text and delete keyboard from message
    device = "💻 ПК" if call.data.startswith("pc") else "📱 Смартфон"
    await call.message.edit_text(
        f"Ты выбрал {device}, приступаю к созданию конфига", reply_markup=None
    )
    await state.finish()

    # add +1 to user config count
    database.update_user_config_count(call.from_user.id)

    device = "PC" if call.data.startswith("pc") else "PHONE"
    user_config = await vpn_config.update_server_config(
        username=call.from_user.username, device=device
    )

    database.insert_new_config(
        user_id=call.from_user.id,
        username=call.from_user.username,
        device=device,
        config=user_config,
    )

    io_config_file = BytesIO(user_config.encode("utf-8"))
    filename = f"{configuration.configs_prefix}_{call.from_user.username}_{device}.conf"

    # send config file
    await call.message.answer_document(
        types.InputFile(
            io_config_file,
            filename=filename,
        ),
        reply_markup=await kb.configs_kb(call.from_user.id),
    )

    if device == "PHONE":
        config_qr_code = create_qr_code_from_peer_data(user_config)
        await call.message.answer_photo(
            types.InputFile(
                config_qr_code,
                filename=f"{configuration.configs_prefix}_{call.from_user.username}.png",
            ),
        )


async def cancel_config_creation(call: types.CallbackQuery, state=FSMContext):
    if database.selector.is_subscription_end(call.from_user.id):
        await cmd_start(call.message)
        await state.finish()
        return

    await state.finish()
    await call.message.edit_text("Отмена создания конфига", reply_markup=None)


async def cmd_show_config(message: types.Message, state=FSMContext):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        await state.finish()
        return

    if message.text.lower().endswith("пк"):
        device = "PC"
    elif message.text.lower().endswith("смартфон"):
        device = "PHONE"

    config = database.selector.get_user_config(
        user_id=message.from_user.id,
        config_name=f"{message.from_user.username}_{device}",
    )
    filename = (
        f"{configuration.configs_prefix}_{message.from_user.username}_{device}.conf"
    )
    io_config_file = BytesIO(config.encode("utf-8"))

    if device == "PC":
        # send config file
        await message.answer_document(
            types.InputFile(
                io_config_file,
                filename=filename,
            ),
        )

    if device == "PHONE":
        # firstly create qr code image, then send it with config file
        # this method is used for restrict delay between sending file and photo
        image_filename = (
            f"{configuration.configs_prefix}_{message.from_user.username}.png"
        )
        config_qr_code = create_qr_code_from_peer_data(config)

        await message.answer_document(
            types.InputFile(
                io_config_file,
                filename=filename,
            ),
        )

        await message.answer_photo(
            types.InputFile(
                config_qr_code,
                filename=image_filename,
            ),
        )


async def cmd_support(message: types.Message):
    # send telegraph page with support info (link: https://telegra.ph/FAQ-po-botu-01-08)
    await message.answer(
        f"Подробное описание бота и его функционала доступно на {hlink('странице','https://telegra.ph/WEBAM-BOT-09-07')}",
        parse_mode=types.ParseMode.HTML,
    )

    admin_username = selector.get_username_by_id(configuration.admins[0])
    admin_telegram_link = f"t.me/{admin_username}"
    await message.answer(
        f"Если у тебя все еще остались вопросы, то ты можешь написать {hlink('мне',admin_telegram_link)} лично",
        parse_mode=types.ParseMode.HTML,
    )


async def cmd_show_end_time(message: types.Message):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        return

    # show user end time
    await message.answer(
        f"{message.from_user.full_name or message.from_user.username}, "
        f"твой доступ к VPN закончится {database.selector.get_subscription_end_date(message.from_user.id)}"
    )


async def cmd_show_subscription(message: types.Message):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        return

    await message.answer(
        f"{message.from_user.full_name or message.from_user.username}, "
        "здесь ты можешь распорядиться своей подпиской",
        reply_markup=await kb.subscription_management_kb(),
    )


async def cmd_reboot_wg_service(message: types.Message):
    if database.selector.is_subscription_end(message.from_user.id):
        await cmd_start(message)
        return

    await message.answer("Перезагрузка сервиса WireGuard...")
    vpn_config.restart_service()
    await message.answer("Сервис WireGuard перезагружен")


async def sponsors(message: types.Message):
    await message.answer("😎Люди поддержавшие проект \n\n@web_am - 200р\n@durov - 150р ")


async def prices(message: types.Message):
    await message.answer("✅1 месяц 100р\n✅3 месяц 300р\n✅6 месяц 600р\n✅12 месяц 1200р")

async def cmd_set(message: types.Message):
   await message.answer(
        f"✅Видеоинструкция как купить и настроить{hlink('VPN','https://rutube.ru/video/8d4e927ac11658f5aeab73e68b4a3b7b/?r=wd')}\n\n✅ Установите приложение Wireguard \n \n🔰Для iPhone➡️{hlink('WireGuard','https://apps.apple.com/ru/app/wireguard/id1441195209 ')}\n🔰Для Andoid➡️{hlink('WireGuard','https://play.google.com/store/apps/datasafety?id=com.wireguard.android&hl=ru&gl=US')}\n\n✅Есть два варианта активаций\n\n1️⃣ Через программу WireGuard отсканируйте qr-код который мы вам дадим после покупки и зайдете имя своему vpn\n\n2️⃣ Полеченый конфиг файл откройте Через программу WireGuard \n\n❗ Oдин и тот же QR код и конфиг файл можно использовать только на одном устройстве!",
        parse_mode=types.ParseMode.HTML,
    )
