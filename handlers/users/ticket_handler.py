from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.menu_keyboards import menu
from keyboards.inline.dashboard_keyboards import faculty_keyboards, \
    faculty_cd, confirmation_keyboards, confirm_cd


from loader import dp, db
from states.TicketState import Ticket

from utils.misc.others import check
from utils.misc.photography import photo_link



@dp.message_handler(text="Info")
async def info_about_bot(message: types.Message):
    await message.answer("Arizlarni qabul qiluvchi telegram bot")

@dp.message_handler(text="Ariza")
async def contidion(message: types.Message):
    await message.answer(
        "Ariza yuborish uchun to'liq ism familyangizni kiriting\nNamuna: <i>Anvarov Anvar Anvarjon o'g'li</i>",
        parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
    await Ticket.full_name.set()

@dp.message_handler(state=Ticket.full_name)
async def get__full_name(message: types.Message, state: FSMContext):
    await state.update_data(full_name = message.text)
    await state.update_data(user_id=message.from_user.id)
    await message.answer(
        "Gurux raqamingizni kiriting\nNamuna: <i>20.08</i>",
        parse_mode='html')
    await Ticket.group_number.set()

@dp.message_handler(state=Ticket.group_number)
async def get__group_number(message: types.Message, state: FSMContext):
    await state.update_data(group_number = message.text)
    markup = await faculty_keyboards()
    await message.answer(
        "Quyidagi menu orqali fakultetingizni tanlang", parse_mode='html',
        reply_markup=markup)
    await Ticket.faculty.set()

@dp.message_handler(state=Ticket.faculty)
async def unknown_get__faculty(message: types.Message):
    await message.answer("Iltimos fakultetingizni tanlang")

@dp.callback_query_handler(faculty_cd.filter(), state=Ticket.faculty)
async def get__faculty(call: types.CallbackQuery, state: FSMContext,
                       callback_data: dict):
    await call.answer(cache_time=1)
    faculty = callback_data.get("faculty_name")
    fac = await db.get_faculty(faculty_name=faculty)

    await state.update_data(faculty_name=faculty)
    await state.update_data(faculty_id=fac['id'])

    await call.message.edit_reply_markup()
    await call.message.answer("Kvitansiya rasmini yuboring...",
                              parse_mode='html')
    await Ticket.file.set()


@dp.message_handler(state=Ticket.file, content_types='photo')
async def get__file(message: types.Message, state: FSMContext):
    xabar = await message.answer("Iltimos kuting ...")
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data(file=link)
    async with state.proxy() as data:
        full_name = data.get("full_name")
        group_number = data.get("group_number")
        faculty = data.get("faculty_name")
        file = data.get("file")

    string = "Ma'lumotlar qabul qilindi\n\n"
    string += f"<b>To'liq ismi: </b>{full_name}\n"
    string += f"<b>Gurux raqami: </b>{group_number}\n"
    string += f"<b>Fakulteti: </b>, {faculty}\n"
    string += f"<b><a href='{file}'>Kvitansiya rasmi</a></b>"
    await xabar.delete()
    await message.answer(string, parse_mode='html',
                          reply_markup=confirmation_keyboards)
    await Ticket.confirm.set()




@dp.message_handler(state=Ticket.file)
async def get__file(message: types.Message, state: FSMContext):
    await message.answer("Noto'g'ri amal")


@dp.callback_query_handler(confirm_cd.filter(), state=Ticket.confirm)
async def confirm(call: types.CallbackQuery, callback_data: dict,
                  state: FSMContext):
    await call.answer(cache_time=1)
    confirm = callback_data.get("confirm")
    await call.message.edit_reply_markup()

    async with state.proxy() as data:
        full_name = data.get("full_name")
        group_number = data.get("group_number")
        faculty = data.get("faculty_id")
        file = data.get("file")
        user_id = data.get("user_id")

    all_id = await db.get_all_ticket()

    if confirm == "confirm":
        ticket_id = check(all_id)
        try:
            await db.add_ticket(
                id=ticket_id,
                full_name=full_name,
                group_number=group_number,
                faculty=faculty,
                file=file,
                telegram_id=user_id,
                created_at=datetime.now()
            )
            await call.message.answer("✅ Xabaringiz muvaffaqiyatli "
                                      "jo'natildi",
                                      reply_markup=menu)
        except Exception as err:
            print(err)
            print("Ticketni bazaga saqashda xatolik yuz berdi!")
            await call.message.answer("Ma'lumotlaringizda xatlik mavjud "
                                      "iltimos qaytadan urinib ko'ring!",
                                      reply_markup=menu)
        finally:
            await state.finish()
    else:
        await call.message.answer("Bekor qilindi, qayta ariza berish uchun "
                                  "Ariza tugmasini bosing", reply_markup=menu)
    await state.finish()