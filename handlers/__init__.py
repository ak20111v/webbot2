from .user import *
from .admin import *
from .coffee import *
from aiogram.types import ContentType

# DON'T TOUCH THIS IMPORT
from loader import dp
from aiogram import Dispatcher


def setup(dp: Dispatcher):
    """setup handlers for users and moders in one place and add throttling in 5 seconds

    Args:
        dp (Dispatcher): Dispatcher object
    """

    """user handlers"""
    dp.register_message_handler(cmd_start, commands=["start"], state=None)

    dp.register_message_handler(
        get_payment_buttons, lambda message: message.text in ("💵 Продлить VPN", "💵 Купить VPN"), state=None
    )
    dp.register_callback_query_handler(
        check_payment, lambda message: message.data[:13] == "check_payment", state=None
    )

    dp.register_message_handler(cmd_my_configs, text="🔑Мои ключи", state=None)

    dp.register_message_handler(cmd_menu, text="🔙 Назад", state=None)

    dp.register_callback_query_handler(
        device_selected,
        lambda call: call.data.endswith("config_create_request"),
        state=NewConfig.device,
    )

    dp.register_callback_query_handler(
        cancel_config_creation,
        lambda call: call.data == "cancel_config_creation",
        state=NewConfig.device,
    )

    dp.register_message_handler(create_new_config, text="🆕 Создать конфиг", state=None)

    dp.register_message_handler(
        cmd_show_config, lambda message: message.text.startswith("🔐"), state=None
    )

    dp.register_message_handler(
        cmd_support,
        text="📝 Помощь",
    )

    dp.register_message_handler(
        cmd_show_end_time,
        text="📅 Дата отключения",
    )

    dp.register_message_handler(
        cmd_show_subscription,
        text="🕑 Моя подписка",
    )

    dp.register_message_handler(
        sponsors,
        text="😎 Спонсоры",
    )

    dp.register_message_handler(
        cmd_reboot_wg_service,
        text="☢️Перезагрузить VPN",
    )

    """moder handlers"""
    dp.register_message_handler(cmd_info, commands=["info"], state=None)

    dp.register_message_handler(statistic_endtime, commands=["stats"], state=None)

    dp.register_message_handler(give_subscription_time, commands=["give"], state=None)

    dp.register_message_handler(
        restart_wg_service_admin, commands=["wgrestart"], state=None
    )


    dp.register_message_handler(
        get_coffee_list,
        text="😍 Пожертвовать",
    )

    dp.register_message_handler(
        buy_bread,
        text="😍 Булочку 35р",
    )

    dp.register_message_handler(
        buy_coffee,
        text="☕️ Айс кофе 250₽",
    )


    dp.register_message_handler(
        buy_cake,
        text="🍰 Тортик 350р",
    )

    dp.register_message_handler(
        prices,
        text="💵 Тарифы 💵"
    )

    dp.register_message_handler(
        cmd_pay,
        text="✅1 месяц 100р"
    )
    dp.register_message_handler(
        cmd_pay,
        text="✅3 месяц 300р"
    )
    dp.register_message_handler(
        cmd_pay,
        text="✅6 месяц 600р"
    )
    dp.register_message_handler(
        cmd_pay,
        text="✅12 месяц 1200р"
    )
    dp.register_message_handler(
        cmd_set,
        text="🤳Как настроить VPN"
    )
    #"""moder handlers"""   этот код был в стаором версии 
    #dp.register_message_handler(cmd_info, commands=["info"], state=None)

    #dp.register_message_handler(statistic_endtime, commands=["stats"], state=None)

    #dp.register_message_handler(give_subscription_time, commands=["give"], state=None)

    #dp.register_message_handler(
        #restart_wg_service_admin, commands=["wgrestart"], state=None
    #)
