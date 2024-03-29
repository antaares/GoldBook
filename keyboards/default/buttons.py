from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove




start_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ariza yuborish")
        ],
    ],
    resize_keyboard=True
)


contact_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
        ]
        ],
        resize_keyboard=True
)



remove_button = ReplyKeyboardRemove()



books_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ingliz tili")
        ],
        [
            KeyboardButton(text="Rus tili")
        ],
        [
            KeyboardButton(text="Turk tili")
        ],
                
        ],
        resize_keyboard=True
)



choice_goal_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Sayohat uchun"),
            KeyboardButton(text="Ish uchun")
        ],
        [
            KeyboardButton(text="O‘qish uchun"),
            KeyboardButton(text="Boshqa sabab")
        ]
    ],
    resize_keyboard=True
    
)






# for admins


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


ADMIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📈Statistika📉"),
            KeyboardButton(text="📤Xabar yuborish📬")
        ]
    ],
    resize_keyboard=True
)


BACK = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Bekor qilish")
        ]
    ],
    resize_keyboard=True
)



CHOICE = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Forward Message"),
            KeyboardButton(text="Copy Message")
        ],
        [
            KeyboardButton(text="Bekor qilish")
        ]
    ],
    resize_keyboard=True
)


CONFIRM = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yuborish"),
            KeyboardButton(text="Bekor qilish")
        ]
    ],
    resize_keyboard=True
)


YES_NO = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ha"),
            KeyboardButton(text="Yo'q")
        ]
    ],
    resize_keyboard=True
)
