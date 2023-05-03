from typing import Union
from datetime import date
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_status(self):
        sql = """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            situation_en VARCHAR(50) NOT NULL,
            situation_uz VARCHAR(50) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_faculty(self):
        sql = """
        CREATE TABLE IF NOT EXISTS faculty (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_ticket_type(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ticket_type (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_user(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            group_number VARCHAR(20) NOT NULL,
            phone_number VARCHAR(15) NOT NULL,
            faculty INTEGER REFERENCES faculty(id),
            telegram_id BIGINT NOT NULL UNIQUE,
            created_at TIMESTAMP NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_ticket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS ticket (
            id BIGINT UNIQUE NOT NULL,
            status INTEGER REFERENCES status(id) DEFAULT 1,
            file VARCHAR(300) NULL,
            text TEXT NULL,
            paynet NUMERIC(12, 3) NULL,
            created_at TIMESTAMP NOT NULL,
            tickey_type INTEGER REFERENCES ticket_type(id),
            user_id INTEGER REFERENCES users(id)
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())


    """ STATUS TABLE """
    async def prepare_status(self):
        sql = """
        INSERT INTO status (situation_en, situation_uz)
        VALUES
            ('new', 'Yangi'),
            ('waiting', 'Kutilmoqda'),
            ('confirmed', 'Tasdiqlangan');
        """
        await self.execute(sql, fetch=True)


    """ FACUTY TABLE """
    async def prepare_faculty(self):
        sql = """
        INSERT INTO faculty (name) 
        VALUES
            ('Filologiya'), ('Matematika-informatika'), ('Tarix'),
            ('Chet tillari'), ('Harbiy talim'), ('Jismoniy madaniyat'), ('Iqtisodiyot'), 
            ('Pedagogika psixologiya'), ('Tabiiy fanlar'), ('Sanatshunoslik'), ('Fizika-texnika'), 
            ('Ingliz tili va adabiyoti'), ('Sirtqi bolim'), ('Agrar qoshma');
        """
        await self.execute(sql, fetch=True)


    """ USER TABLE"""
    async def add_user(
            self,
            full_name: str,
            group_number: str,
            faculty: int,
            phone_number: str,
            telegram_id: int,
            created_at: date):
        sql = """
        INSERT INTO users 
            (full_name, group_number, faculty, phone_number, telegram_id, created_at) 
        VALUES 
            ( $1, $2, $3, $4, $5, $6) returning *
        """
        return await self.execute(sql, full_name, group_number, faculty,
                                  phone_number, telegram_id, created_at,
                                  fetchrow=True)


    async def get_user(self, telegram_id):
        sql = f"""
        SELECT * FROM users WHERE telegram_id={telegram_id}
        """
        return await self.execute(sql, fetchrow=True)

    async def get_all_users(self):
        sql = "SELECT * FROM users;"
        return await self.execute(sql, fetch=True)

    async def get_user_full_data(self, telegram_id):
        sql = f"""
        SELECT * FROM users INNER JOIN faculty ON users.faculty = faculty.id WHERE telegram_id = {telegram_id};  
        """
        return await self.execute(sql, fetchrow=True)





    """ TICKET TYPE TABLE """
    async def get_all_tickets(self):
        return await self.execute("SELECT * FROM ticket_type;", fetch=True)



    """ TICKET TABLE """
    async def add_ticket(
            self,
            id: int,
            file: str,
            text: str,
            created_at: date,
            ticket_type: int,
            user_id: int
    ):
        sql = """
        INSERT INTO ticket 
            (id, file, text, created_at, ticket_type, user_id) 
        VALUES
            ($1, $2, $3, $4, $5, $6) returning *"""
        return await self.execute(
            sql,
            id,
            file,
            text,
            created_at,
            ticket_type,
            user_id,
            fetchrow=True
        )

    async def get_all_ticket(self):
        sql = "SELECT * FROM ticket"
        return await self.execute(sql, fetch=True)

    async def get_ticket_full_data(self, ticket_type: int):
        sql = f"""
        SELECT * FROM ticket INNER JOIN ticket_type ON ticket.ticket_type=ticket_type.id WHERE ticket_type={ticket_type};
        """
        return await self.execute(sql, fetchrow=True)

    async def get_ticket(self, **kwargs):
        sql = "SELECT * FROM ticket WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_ticket(self):
        sql = "SELECT COUNT(*) FROM ticket"
        return await self.execute(sql, fetchval=True)

    async def delete_ticket(self):
        await self.execute("DELETE FROM ticket WHERE TRUE", execute=True)

    async def drop_ticket(self):
        await self.execute("DROP TABLE ticket", execute=True)



    """ FACULTY TABLE """
    async def get__all_faculties(self):
        return await self.execute("SELECT * FROM faculty", fetch=True)

    async def get_faculty(self, faculty_name):
        sql = f"SELECT * FROM faculty WHERE name = '{faculty_name}'"
        return await self.execute(sql, fetchrow=True)


