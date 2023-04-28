# import logging
# import asyncio
#
# from aiogram import types
# from aiogram.dispatcher import FSMContext
#
# from data.config import ADMINS
# from filters import AdminFilter
# # from keyboards.default.general_keyboards import cancel
# # from keyboards.inline.channels_keyboard import channels_list, channel_cd
# # from keyboards.inline.dashboard import dashboard_keyboards, channels
# # from states.AdminState import AddChannel, SendAds
# # from aiogram.utils import exceptions
# #
# # from .start import show_channels_start
#
#
# from loader import dp, bot, db
#
#
# @dp.message_handler(AdminFilter(), commands="admin", state=None)
# async def show_dashboard(message: types.Message):
#     await message.answer("Admin panel", reply_markup=dashboard_keyboards)
#
#
# @dp.message_handler(AdminFilter(), state="*", text="❌ Bekor qilish")
# async def stop_state(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Amaliyot bekor qilindi", reply_markup=types.ReplyKeyboardRemove())
#
#
#
# @dp.callback_query_handler(AdminFilter(), text="channels")
# async def show_channels(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     await call.message.edit_reply_markup()
#     CHANNELS = await db.get_all_channels()
#     channels_str = "<b>Botga ulangan kanallar ro'yxati</b>\n\n"
#     for channel in CHANNELS:
#         channel = channel[1]
#
#         channel = await bot.get_chat(channel)
#         invite_link = await channel.export_invite_link()
#         channels_str += f"<a href='{invite_link}'>{channel.title}</a>\n"
#
#     await call.message.edit_text(channels_str, reply_markup=channels, disable_web_page_preview=True, parse_mode="HTML")
#
#
#
# @dp.callback_query_handler(AdminFilter(), text="add_channel")
# async def add_channel(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     await call.message.edit_reply_markup()
#     await call.message.answer("Kanalga tegishli <b>id</b> yoki <b>@username</b> kiriting", reply_markup=cancel)
#     await AddChannel.first.set()
#
# @dp.message_handler(AdminFilter(), state=AddChannel.first)
# async def get_channel_id(message: types.Message, state: FSMContext):
#     try:
#         channel = await bot.get_chat_administrators(message.text)
#         await db.add_channel(channel_id=message.text)
#         await message.answer("Kanal muvaffaqiyatli qo'shildi ✅", reply_markup=types.ReplyKeyboardRemove())
#         await state.finish()
#     except exceptions.ChatNotFound as err:
#         await message.answer("<i>Bot bu kanalda admin emas. Avval botni kanalga admin qilishizngiz zarur ⚠️</i>", parse_mode="HTML")
#
#
# @dp.callback_query_handler(AdminFilter(), text="del_channel")
# async def delete_channel(call: types.CallbackQuery):
#     channels = await db.get_all_channels()
#     if len(channels) == 0:
#         await call.answer("Botga hech qanday kanal ulanmagan ⚠️", show_alert=True, cache_time=1)
#         return
#     await call.answer(cache_time=1)
#     markup = await channels_list(CHANNELS=channels)
#     await call.message.edit_reply_markup()
#     await call.message.edit_text("Kanal nomini tanlash orqali ularni o'chirishingiz mumkin", reply_markup=markup)
#
#
# @dp.callback_query_handler(AdminFilter(), channel_cd.filter())
# async def del_channel(call: types.CallbackQuery, callback_data: dict):
#     get_id = callback_data.get("channel_id")
#     id = int(get_id)
#     try:
#         await db.delete_channel(id=id)
#         await call.answer("Kanal o'chirildi ✅", show_alert=True, cache_time=1)
#         channels = await db.get_all_channels()
#         markup = await channels_list(CHANNELS=channels)
#         await call.message.edit_reply_markup(reply_markup=markup)
#     except Exception as err:
#         print(err)
#         await call.answer("Nomalum xatolik  yuz berdi!", cache_time=1)
#
#
#
# # STATISTICA ------------------------------------------------------------
# @dp.callback_query_handler(AdminFilter(), text="statistica")
# async def show_statistics(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     count_users = await db.count_users()
#     count_books = await db.count_books()
#     text = f"<b>📊 Statistika</b>\n\n"
#     text += f"<b>👤 Foydalanuvchilar soni: {count_users} ta</b>\n"
#     text += f"<b>📚 Kitoblar soni: {count_books} ta</b>"
#     await call.message.edit_reply_markup()
#     await call.message.answer(text)
#
#
#
#
# # REKLAMA ---------------------------------------------------------------
# async def send_post(chat_id,message_id,user_id,reply_markup=None):
#     try:
#         if reply_markup:
#             await bot.copy_message(chat_id=user_id, from_chat_id=chat_id, message_id=message_id,reply_markup=reply_markup)
#         else:
#             await bot.copy_message(chat_id=user_id, from_chat_id=chat_id, message_id=message_id)
#     except exceptions.BotBlocked:
#         logging.error(f"Target [ID:{user_id}]: blocked by user")
#     except exceptions.ChatNotFound:
#         logging.error(f"Target [ID:{user_id}]: invalid user ID")
#     except exceptions.RetryAfter as e:
#         logging.error(
#             f"Target [ID:{user_id}]: Flood limit is exceeded. "
#             f"Sleep {e.timeout} seconds."
#         )
#         await asyncio.sleep(e.timeout)
#         return await bot.copy_message(chat_id=user_id, from_chat_id=chat_id, message_id=message_id)
#     except exceptions.UserDeactivated:
#         logging.error(f"Target [ID:{user_id}]: user is deactivated")
#     except exceptions.TelegramAPIError:
#         logging.exception(f"Target [ID:{user_id}]: failed")
#     else:
#         logging.info(f"Target [ID:{user_id}]: success")
#         return True
#     return False
#
#
# @dp.callback_query_handler(AdminFilter(), text="ads")
# async def ads_function(call: types.CallbackQuery):
#     await call.message.edit_reply_markup()
#     await call.message.answer("Reklama postini yuboring", reply_markup=cancel)
#     await SendAds.first.set()
#
# @dp.message_handler(AdminFilter(), state=SendAds.first, content_types=["photo", "video", "text"])
# async def send_ads(message: types.Message, state: FSMContext):
#     users = await db.select_all_users()
#     for user in users:
#         await send_post(chat_id=ADMINS[0], message_id=message.message_id, user_id=user[2])
#         await asyncio.sleep(0.05)
#     await bot.send_message(chat_id=message.from_user.id, text="Reklama muvaffaqiyatli yuborildi ✅", reply_markup=types.ReplyKeyboardRemove())
#     await state.finish()
#
#
#  # TOP USERS ---------------------------------------------------------------
# @dp.callback_query_handler(AdminFilter(), text="top_users")
# async def top_users(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     top_users = await db.get_top_users()
#     text, li = "<b>🏆 Top foydalanuvchilar 10 taligi</b>\n\n", 1
#     for user in top_users:
#         text += f"<b>{li}. {user[1]}</b> <i>{user[3]} ta kitob</i>\n"
#         li += 1
#     await call.message.edit_reply_markup()
#     await call.message.answer(text)
#
#
# @dp.callback_query_handler(AdminFilter(), text="menu")
# async def go_to_menu(call: types.CallbackQuery):
#     await call.answer(cache_time=1)
#     await call.message.edit_reply_markup()
#     await call.message.edit_text("Admin panel", reply_markup=dashboard_keyboards)
#
#
#
#
#
#
#
#
# @dp.callback_query_handler(AdminFilter(), text="close_window", state="*")
# async def go_to_menu(call: types.CallbackQuery, state: FSMContext):
#     await call.answer(cache_time=1)
#     await call.message.edit_reply_markup()
#     await show_channels_start(call.message)
#     await state.finish()