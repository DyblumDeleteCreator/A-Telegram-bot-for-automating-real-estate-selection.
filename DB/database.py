import aiosqlite

DB_NAME = 'real_estate.db'

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        #Квартиры
        await db.execute("""
            CREATE TABLE IF NOT EXISTS apartments (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         rooms INTEGER,
                         area REAL,
                         cost INTEGER,
                         adress TEXT,
                         link TEXT
                         )
                         """)

        # Зем участки
        await db.execute("""
            CREATE TABLE IF NOT EXISTS lands (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         square REAL,
                         cost INTEGER,
                         adress TEXT,
                         link TEXT
                         )
                         """)

        #Дома
        await db.execute("""
                    CREATE TABLE IF NOT EXISTS houses (
                                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 rooms INTEGER,
                                 floors INTEGER,
                                 area REAL,
                                 square REAL,
                                 cost INTEGER,
                                 adress TEXT,
                                 link TEXT
                                 )
                                 """)

        await db.commit()

#ADD
async def add_apartment(rooms, area, cost, adress, link):
    async with aiosqlite.connect(DB_NAME) as db:
        #Квартиры
        await db.execute("INSERT INTO apartments (rooms, area, cost, adress, link) VALUES(?, ?, ?, ?, ?)", (rooms, area, cost, adress, link))
        await db.commit()

async def add_land(square, cost, adress, link):
    async with aiosqlite.connect(DB_NAME) as db:
        #Зем участки
        await db.execute("INSERT INTO lands (square, cost, adress, link) VALUES(?, ?, ?, ?)", (square, cost, adress, link))
        await db.commit()

async def add_house(rooms, floors, area, square, cost, adress, link):
    async with aiosqlite.connect(DB_NAME) as db:
        #Дома
        await db.execute("INSERT INTO houses (rooms, floors, area, square, cost, adress, link) VALUES(?, ?, ?, ?, ?, ?, ?)", (rooms, floors, area, square, cost, adress, link))
        await db.commit()

#GET
async def get_apartments():
    async with aiosqlite.connect(DB_NAME) as db:
        #Квартиры
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM apartments")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_lands():
    async with aiosqlite.connect(DB_NAME) as db:
        #Зем участки
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM lands")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def get_houses():
    async with aiosqlite.connect(DB_NAME) as db:
        #Дома
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM houses")
        rows = await cursor.fetchall()
        return [dict(row) for row in rows] 

#SAVE
async def save_object(data: dict):
    if data.get('tip') == 'Квартира':
        await add_apartment(rooms=data['rooms'],
                            area=data['area'],
                            cost=data['cost'],
                            adress=data['adress'],
                            link=data['link']
                            )
    elif data.get('tip') == 'Дом':
        await add_house(rooms=data['rooms_house'],
                        floors=data['floors'],
                        area=data['area_house'],
                        square=data['square_house'],
                        cost=data['cost'],
                        adress=data['adress'],
                        link=data['link']
                        )
    elif data.get('tip') == 'Земельный участок':
        await add_land(square=data['square'],
                       cost=data['cost'],
                       adress=data['adress'],
                       link=data['link']
                       )

#DELETE
async def delete_object(table: str, obj_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(f"DELETE FROM {table} WHERE id = ?", (obj_id,))
        await db.commit()

#PODBOR
async def podbor_apartments(cost, rooms, area):
    async with aiosqlite.connect(DB_NAME) as db:
        #Квартиры
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM apartments WHERE cost <= ? AND rooms >= ? AND area >= ?", (cost, rooms, area))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def podbor_lands(cost, square):
    async with aiosqlite.connect(DB_NAME) as db:
        #Зем участки
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM lands WHERE cost <= ? AND square >= ?", (cost, square))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def podbor_houses(cost, rooms, floors, area, square):
    async with aiosqlite.connect(DB_NAME) as db:
        #Дома
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM houses WHERE cost <= ? AND rooms >= ? AND floors >= ? AND area >= ? AND square >= ?", (cost, rooms, floors, area, square))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows] 