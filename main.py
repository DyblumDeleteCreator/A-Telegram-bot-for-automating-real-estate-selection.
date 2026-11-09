#Welocme to Основа все выводится через этот блок и отвечает за подключение к серверу(здесь идет подключение к сервакам телеги)
from os import  getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from Handlers.routes import router
from DB.database import init_db

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()

dp.include_router(router)



async def main():
    
    await init_db()
    
    bot = Bot(token=TOKEN)

    print('Bot starting')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

