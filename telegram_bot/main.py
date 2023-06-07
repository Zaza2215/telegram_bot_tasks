from aiogram import executor

from handlers import client, admin, other
from create_bot import dp


async def on_startup(_):
    print("Bot is online")


if __name__ == "__main__":
    client.register_handlers_client(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
