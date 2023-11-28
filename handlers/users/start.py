from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from filters.is_private import IsPrivate


from loader import dp, db 


from data.config import ADMINS, GROUP_ID



# import buttons
from keyboards.default.buttons import contact_button, no_contact_button, books_button, remove_button


# import states
from states.users import UserState
from aiogram.dispatcher.storage import FSMContext




QUESTIONS = {
    'start': 'Assalomu alaykum hurmatli mijoz, iltimos ismingizni yozing',
    'contact':"Pastdagi tugmani bosish orqali telefon raqamingizni yuboring!",
    'secon-phone':"Qo'shimcha telefon raqamingizni yuboring! \n\n<b>Agar qo'shimcha raqam yo'q bo'lsa yo'q tugmasini bosing</b>",
    'choose-books':"Siz aynan qaysi kitobimizni sotib olmoqchisiz?",
    'last-words':'Tez orada siz bilan mutaxasisimiz bog‘lanadi!'     
}





@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(QUESTIONS['start'], reply_markup=remove_button)

    db.add_user(message.from_user.id, message.from_user.full_name)
    await UserState.start.set()



@dp.message_handler(IsPrivate(), state=UserState.start)
async def get_fullname(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer(QUESTIONS['contact'], reply_markup=contact_button)
    await UserState.contact.set()


@dp.message_handler(IsPrivate(), state=UserState.contact, content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    if message.contact:
        await state.update_data(contact=message.contact.phone_number)
    else:
        await state.update_data(contact=message.text)   
    await message.answer(QUESTIONS['secon-phone'], reply_markup=no_contact_button)
    await UserState.second_phone.set()

@dp.message_handler(IsPrivate(), state=UserState.second_phone)
async def get_second_phone(message: types.Message, state: FSMContext):
    await state.update_data(second_phone=None)
    if message.text != "Yo'q":
        await state.update_data(second_phone=message.text)        
    await message.answer(QUESTIONS['choose-books'], reply_markup=books_button)
    await UserState.choose_books.set()

@dp.message_handler(IsPrivate(), state=UserState.choose_books)
async def get_books(message: types.Message, state: FSMContext):
    await state.update_data(books=message.text)
    await message.answer(QUESTIONS['last-words'], reply_markup=remove_button)
    

    """Send message to admin"""
    data = await state.get_data()
    await dp.bot.send_message(chat_id= GROUP_ID, text=f"""
    <b>Yangi mijoz</b>
    <b>Ismi:</b> {data.get('full_name')}
    <b>Telegram ID:</b> <a href=\"tg://user?id={message.from_user.id}\">{message.from_user.id}</a>
    <b>Telefon raqami:</b> {data.get('contact')}
    <b>Qo'shimcha raqami:</b> {data.get('second_phone')}
    <b>Kitobi:</b> {data.get('books')}
    """, parse_mode='HTML')



# cancel handler
@dp.message_handler(IsPrivate(), state="*", commands="cancel")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Siz malumotlarni o'chirib tashladingiz!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(IsPrivate(), commands="error")
async def error(message: types.Message):
    await message.answer_document(document=open("logfile_err.log", "rb"))


@dp.message_handler(commands="info")
async def info(message: types.Message):
    await message.answer(message.chat.id)