import asyncio
import aiomysql

from usages.database_usecase._initialize.notepad import generate_member_object


async def fetch_data(connection):
    async with connection.cursor() as cur:
        await cur.execute("SELECT * FROM member;")
        result = await cur.fetchall()

        return result


async def insert_data(connection, members):
    async with connection.cursor() as cur:
        _sql = """
        INSERT INTO demo.`member` (
            nanoid,
            name,
            age,
            address1,
            address2
        )
         VALUES (
            %(nanoid)s,
            %(name)s,
            %(age)s,
            %(address1)s,
            %(address2)s
             );
        """

        await cur.executemany(
            _sql,
            [{
                'nanoid': member.nanoid,
                'name': member.name,
                'age': member.age,
                'address1': member.address1,
                'address2': member.address2
            } for member in members])

    await connection.commit()

async def main():
    conn = await aiomysql.connect(
        host='127.0.0.1',
        port=19501,
        user='root',
        password='1234',
        db='demo'
    )

    members = generate_member_object()

    import time
    start_time = time.time()

    chunk_size = 10_000
    for i in range(0, len(members), chunk_size):
        member_dict = members[i:i + chunk_size]
        await insert_data(conn, member_dict)

    conn.close()

    end_time = time.time()
    print(end_time - start_time)

asyncio.run(main())
