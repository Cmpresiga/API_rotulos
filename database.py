import asyncpg


async def get_connection():
    conn = await asyncpg.connect(
        database="rotulos",
        user="publico",
        password="Abcd1234",
        host="localhost",
        port=5432
    )
    return conn
