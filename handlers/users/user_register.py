from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu_keyboards import menu, registration_keyboard
from keyboards.inline.dashboard_keyboards import faculty_keyboards, faculty_cd
from loader import dp, db
from states.TicketState import User


@dp.message_handler(text="🌐 Ro'yxatdan o'tish")
async def start_ticket(message: types.Message):
    users = await db.get_all_users()
    markup = await faculty_keyboards()
    await message.answer(
        text="🔍 Fakultetingizni tanlang",
        parse_mode='html', reply_markup=markup)
    await User.faculty.set()



@dp.callback_query_handler(faculty_cd.filter(), state=User.faculty)
async def get__faculty(call: types.CallbackQuery, state: FSMContext,
                       callback_data: dict):
    await call.answer(cache_time=1)
    faculty = callback_data.get("faculty_name")
    fac = await db.get_faculty(faculty_name=faculty)
    print(fac['id'])
    await state.update_data(faculty_id=fac['id'])

    await call.message.edit_reply_markup()
    await call.message.answer(
        "🖊 Guruh raqamingizni kiriting.\n\nNamuna: <i>20.07</i>",
        parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    await User.group_number.set()


@dp.message_handler(state=User.faculty, content_types='any')
async def unknown_get__faculty(message: types.Message):
    await message.answer("❗️ Iltimos, fakultetingizni tanlang")
    await User.faculty.set()



@dp.message_handler(state=User.group_number, content_types='text')
async def get__group_number(message: types.Message, state: FSMContext):
    if len(message.text) > 20:
        await message.answer("❗️ Maksimal 20 ta belgidan iborat gurux raqam uyuqoring")
        return
    await state.update_data(group_number = message.text)
    await message.answer(
        text="🖊 To'liq ism familyangizni kiriting.\n\nNamuna: "
             "<i>Anvarov Anvar Anvarjon o'g'li</i>",
        parse_mode = 'html', reply_markup = types.ReplyKeyboardRemove())
    await User.full_name.set()

@dp.message_handler(state=User.group_number, content_types='any')
async def unknown_get__group_number(message: types.Message, state: FSMContext):
    await message.answer("❗️ Iltimos, matn sifatida yuboring")



@dp.message_handler(state=User.full_name)
async def get__full_name(message: types.Message, state: FSMContext):
    if len(message.text) > 255:
        await message.answer("❗️ Kiritilgan belgilar soni 255 tadan oshmasin!")
        return
    await state.update_data(full_name = message.text)
    await state.update_data(user_id = message.from_user.id)
    await message.answer(
        text="📞 Siz bilan bog'lanishimiz uchun telefon raqamingizni kiriting. \n\nNamuna: <i>+99890 123 45 67</i>",
        parse_mode='html')
    await User.phone_number.set()

@dp.message_handler(state=User.full_name, content_types='any')
async def unknown_get__full_name(message: types.Message, state: FSMContext):
    await message.answer("❗️ Iltimos, matn sifatida yuboring")


@dp.message_handler(state=User.phone_number)
async def get__phone_number(message: types.Message, state: FSMContext):
    if len(message.text) > 15:
        await message.answer("❗️ Kiritilgan telefon raqami 15 ta belgidan oshmasin")
        return
    await state.update_data(phone_number = message.text)
    async with state.proxy() as data:
        full_name = data.get("full_name")
        group_number = data.get("group_number")
        faculty_id = data.get("faculty_id")
        phone_number = data.get("phone_number")
        telegram_id = data.get("user_id")
    try:
        await db.add_user(
            full_name=full_name,
            group_number=group_number,
            faculty=faculty_id,
            phone_number=phone_number,
            telegram_id=telegram_id,
            created_at=datetime.now()
        )
        await message.answer("✅ Muvaffaqiyatli ro'yxatdan o'tdingiz.")
        await message.answer("⬇️ Quyidagi menyulardan birini tanlang",
                             reply_markup=menu)
    except Exception as err:
        print(err)
        print("Foydalanuvchini ro'yxatda olishda xatolik")
        await message.answer("❗️ Ro'yxatdan o'tish xatolik.\n\nQayta urinib ko'ring!", reply_markup=registration_keyboard)
    finally:
        await state.finish()

@dp.message_handler(state=User.phone_number, content_types='any')
async def unknown_get__phone_number(message: types.Message, state: FSMContext):
    await message.answer("❗️ Iltimos, matn sifatida yuboring")





