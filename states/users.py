from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """States of user"""
    start = State()
    full_name = State()
    interesting = State()
    reason = State()
    contact = State()
    error = State()




class AdminState(StatesGroup):
    """States of admins"""
    getMessage = State()
    Choice = State()
    Confirm = State()