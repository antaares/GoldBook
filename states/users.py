from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """States of user"""
    start = State()
    contact = State()
    second_phone = State()
    choose_books = State()
    last_words = State()
    error = State()




class AdminState(StatesGroup):
    """States of admins"""
    getMessage = State()
    Choice = State()
    Confirm = State()