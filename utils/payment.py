import uuid

from time import time
from hashlib import md5
from data import configuration
from yookassa import Configuration, Payment


class YookassaPayment:
    def __init__(self, payment_id: str | None = None, amount: float | None = None):
        Configuration.account_id, Configuration.secret_key = configuration.get_yookassa_params

        self._amount = configuration.base_subscription_monthly_price_rubles if amount is None else amount
        self._payment: Payment = Payment # type: ignore
        self._payment_id: str | None = payment_id
        self._payment_hash: str | None = None

    def create(self, user_id) -> None:
        self._payment_hash = md5(f"{user_id}:{int(time())}:https://t.me/webam_bot".encode("utf-8")).hexdigest()[-8:]

        payment_data = self._payment.create({
            "amount": {
                "value": self._amount,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/webam_bot"
            },
            "capture": True,
            "description": f"Оплата подписки в https://t.me/webam_bot, индификатор заказа: {self._payment_hash}"
        }, uuid.uuid4())

        self._payment_id = payment_data.id

        return

    @property
    def payment_amount(self) -> float:
        return self._amount

    @property
    def payment_url(self) -> str:
        if not self._payment_id:
            raise Exception("payment_id is None")

        return self._payment.find_one(self.payment_id).confirmation.confirmation_url # type: ignore
    
    @property
    def payment_id(self) -> str:
        if not self._payment_id:
            raise Exception("payment_id is None")
        
        return self._payment_id

    @property
    def payment_paid(self) -> bool:
        if not self.payment_id:
            raise Exception("payment_id is None")

        return self._payment.find_one(self.payment_id).paid # type: ignore
