import asyncio

import aiomysql

from usages.database_usecase._initialize.notepad import generate_member_object


async def insert_data(pool, members):
    async with pool.acquire() as connection:
        async with connection.cursor() as cur:
            _sql = """
            INSERT INTO demo.`member` (nanoid, name, age, address1, address2)
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
    members = generate_member_object()

    # connection pool
    pool = await aiomysql.create_pool(
        host='127.0.0.1',
        port=19501,
        user='root',
        password='1234',
        db='demo',
        minsize=10,
        maxsize=100
    )

    import time
    start_time = time.time()

    tasks = []
    chunk_size = 10_000
    for i in range(0, len(members), chunk_size):
        member_dict = members[i:i + chunk_size]

        task = asyncio.create_task(insert_data(pool, member_dict))
        tasks.append(task)

    if tasks:
        await asyncio.gather(*tasks)

    pool.close()
    await pool.wait_closed()

    end_time = time.time()
    print(end_time - start_time)


asyncio.run(main())
