from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.is_private import IsPrivate


from loader import dp, db 


from data.config import GROUP_ID



# import buttons
from keyboards.default.buttons import contact_button, books_button, remove_button, start_button


# import states
from states.users import UserState
from aiogram.dispatcher.storage import FSMContext

from aiogram.dispatcher.filters import Text

QUESTIONS = {
    'start': 'Assalomu alaykum hurmatli mijoz.\nKitob olish uchun <b>Ariza yuborish</b> tugmasini bosing!',  # 1
    'full_name':'To‘liq ismingizni kiriting:',   #2
    'interesting':"Sizga qaysi til koʻproq qiziq?",   #3
    'whyyouneed':"Nega aynan {} sizga kerak?",   #4
    'wehelptoyou':"Sizdagi muammoga Goldbook yordam bera oladi😊 Siz bilan tez orada bogʻlanamiz!",  #6
    'contact':"Pastdagi tugmani bosish orqali telefon raqamingizni yuboring!", #5
    "ifyouwant": "Istasangiz biz bilan bogʻlaning!\n99-582-40-00 Goldbook Shaxzoda👩🏻‍💼\n99-592-66-00 Goldbook Ozoda👩🏽‍💻"   #7
}






# 1
@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(QUESTIONS['start'], reply_markup=start_button)

    db.add_user(message.from_user.id, message.from_user.full_name)

# 2
@dp.message_handler(IsPrivate(), Text(equals="Ariza yuborish", ignore_case=True), state="*")
async def get_fullname(message: types.Message, state: FSMContext):
    await message.answer(QUESTIONS['full_name'], reply_markup=remove_button)
    await UserState.full_name.set()

# 3
@dp.message_handler(IsPrivate(), state=UserState.full_name)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(QUESTIONS['interesting'], reply_markup=books_button)
    await UserState.interesting.set()

# 4
@dp.message_handler(IsPrivate(), state=UserState.interesting)
async def get_interestingt(message: types.Message, state: FSMContext):
    await state.update_data(interesting=message.text)   
    await message.answer(QUESTIONS['whyyouneed'].format(message.text), reply_markup=remove_button)
    await UserState.reason.set()


# 5
@dp.message_handler(IsPrivate(), state=UserState.reason)
async def get_reason(message: types.Message, state: FSMContext):
    await state.update_data(reason=message.text)       
    await message.answer(QUESTIONS['contact'], reply_markup=contact_button)
    await UserState.contact.set()


# 6
@dp.message_handler(IsPrivate(), state=UserState.contact)
async def get_contact(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(contact=message.contact.phone_number)
    else:
        await state.update_data(contact=message.text) 
    await message.answer(QUESTIONS['wehelptoyou'], reply_markup=remove_button)
    await message.answer(QUESTIONS['ifyouwant'], reply_markup=start_button)
    

    """Send message to admin"""
    data = await state.get_data()
    await dp.bot.send_message(chat_id= GROUP_ID, text=f"""
    <b>Yangi mijoz</b>
    <b>Ismi:</b> {data.get('full_name')}
    <b>Telegram ID:</b> <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.id}</a>
    <b>Telefon raqami:</b> {data.get('contact')}
    <b>Qiziqadigan tili:</b> {data.get('interesting')}
    <b>Kitobga qiziqish sababi:</b> {data.get('reason')}
    """, parse_mode='HTML')
    await state.finish()
    await state.reset_state()
    await UserState.start.set()



# cancel handler
@dp.message_handler(IsPrivate(), state="*", commands="cancel")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Siz malumotlarni o'chirib tashladingiz!", reply_markup=start_button)
    await state.finish()


@dp.message_handler(IsPrivate(), commands="error", state="*")
async def error(message: types.Message):
    await message.answer_document(document=open("logfile_err.log", "rb"))


@dp.message_handler(commands="info", state="*")
async def info(message: types.Message):
    await message.answer(message.chat.id, reply_markup=remove_button)