import asyncio
from filters.is_admin import IsAdmin
from filters.is_private import IsPrivate


from loader import dp, db, bot
from aiogram import Bot, types
from aiogram.dispatcher.filters import Text



from keyboards.default.buttons import ADMIN_MENU, BACK, CHOICE, CONFIRM, YES_NO
from aiogram.dispatcher import FSMContext

from states.users import AdminState
from utils.db_api.database import Database

@dp.message_handler(IsAdmin(), IsPrivate(), commands=['dastur'])
async def send_welcome(message: types.Message):
    text = "Assalomu alaykum, siz admin paneldasiz..."
    await message.answer(text=text, reply_markup=ADMIN_MENU)



@dp.message_handler(IsAdmin(), IsPrivate(), Text(equals="📈Statistika📉"), state="*")
async def SendStat(message: types.Message):
    users = 1200
    text = f"Foydalanuvchilar: {users} ta"
    await message.answer(text=text)




@dp.message_handler(IsAdmin(), IsPrivate(), Text(equals="📤Xabar yuborish📬"), state="*")
async def startForm(message: types.Message, state: FSMContext):
    text = "Ho‘sh, demak boshladik, menga barcha foydalanuvchilarga yubormoqchi bo‘lgan xabaringizni yuboring:"
    await message.answer(text=text, reply_markup=BACK)
    await AdminState.getMessage.set()





@dp.message_handler(IsPrivate(), content_types=types.ContentType.ANY, state=AdminState.getMessage)
async def get_message(message: types.Message, state: FSMContext):
    text = message.text

    if text == "Bekor qilish":
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=ADMIN_MENU)
        return
    
    MessageID = message.message_id
    ChatID = message.chat.id
    await state.update_data(MessageID=MessageID)
    await state.update_data(ChatID=ChatID)

    await message.answer(text="Qaysi usulda yuboramiz?", reply_markup=CHOICE)
    await AdminState.Choice.set()


    






@dp.message_handler(IsPrivate(), state=AdminState.Choice)
async def choiceMethod(message: types.Message, state: FSMContext):
    text = message.text

    if text == "Bekor qilish":
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=ADMIN_MENU)
        return
    
    Method = message.text
    await state.update_data(Method=Method)

    data = await state.get_data()
    MessageID = data['MessageID']
    # await message.answer(
    #     text="Shu xabarni yuboramizmi?",
    #     reply_to_message_id=MessageID, 
    #     reply_markup=CONFIRM
    #         )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Shu xabarni yuboramizmi?",
        reply_to_message_id=MessageID,
        reply_markup=CONFIRM
    )
    await AdminState.Confirm.set()




@dp.message_handler(IsPrivate(), state=AdminState.Confirm)
async def Sending(message: types.Message, state: FSMContext):
    text = message.text
    if text == "Yuborish":
        data = await state.get_data()
        Method = data['Method']
        ChatID = data['ChatID']
        if Method == "Forward Message":
            count = await SEND_FORWARD(db, bot, state)
            send_text = f"Tayyor, sizning xabaringiz {count} ta foydalanuvchiga yetkazildi..."
            await dp.bot.send_message(chat_id=ChatID, text=send_text, reply_markup=ADMIN_MENU)
        else:
            count = await SEND_COPY(db, bot, state)
            send_text = f"Tayyor, sizning xabaringiz {count} ta foydalanuvchiga yetkazildi..."
            await dp.bot.send_message(chat_id=ChatID, text=send_text, reply_markup=ADMIN_MENU)
    else:
        await message.answer(text="Assalomu alaykum, siz admin paneldasiz...", reply_markup=ADMIN_MENU)
    await state.finish()







async def SEND_COPY(db: Database, bot: Bot, state: FSMContext):
    users = db.all()
    data = await state.get_data()
    ChatID = data['ChatID']
    MessageID = data['MessageID']
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user, from_chat_id=ChatID, message_id=MessageID)
            count += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(e)
    return count


async def SEND_FORWARD(db: Database, bot: Bot, state: FSMContext):
    users = db.all()
    data = await state.get_data()
    ChatID = data['ChatID']
    MessageID = data['MessageID']
    count = 0
    for user in users:
        try:
            await bot.forward_message(chat_id=user, from_chat_id=ChatID, message_id=MessageID)
            count += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(e)
    return count
