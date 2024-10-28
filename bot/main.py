import os
import asyncio
from app.user import router_users
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv




# Starts the bot and creates a database
async def main():

    load_dotenv()
    token = os.getenv("TOKEN")

    # Initialize the bot with the actual token
    bot = Bot(token)
    dp = Dispatcher()
    dp.include_routers(router_users)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        os.remove("UsersInformation.sqlite3")
        print("Exit")