import asyncio
import datetime

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Ticket jadvalini yaratamiz...")
    await db.drop_ticket()
    await db.create_table_ticket()
    print("Yaratildi")

    print("Ticketlarni qo'shamiz")

    await db.add_ticket(id=3245602, full_name="Raxmatillo Shermatov", group_number="20.08",
                        faculty="Matematika-informatika",
                        file="telegra.ph/photo/user.jpg",
                        created_at=datetime.datetime.now(),
                        telegram_id=94824293)
    # await db.add_user("olim", "olim223", 12341123)
    # await db.add_user("1", "1", 131231)
    # await db.add_user("1", "1", 23324234)
    # await db.add_user("John", "JohnDoe", 4388229)
    print("Qo'shildi")

    users = await db.get_all_ticked_id()
    print(f"Barcha foydalanuvchilar: {users}")
    #
    # user = await db.select_user(id=5)
    # print(f"Foydalanuvchi: {user}")


asyncio.run(test())
