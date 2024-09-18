"""Finite state machine classes module
    """

from aiogram.dispatcher.filters.state import State, StatesGroup


class NewConfig(StatesGroup):
    device = State()
