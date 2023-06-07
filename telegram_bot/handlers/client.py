from aiogram import types, Dispatcher
from telegram_bot.create_bot import dp, bot


HELP = """
This bot helps to manage your tasks.
/start - start bot
/help - list of commands
/create - create task
/delete - delete task
"""

async def start_command(message: types.Message):
    await message.answer("Start manage your tasks!")
    await message.delete()

async def help_command(message: types.Message):
    await message.answer(HELP)
    await message.delete()

def register_handlers_client(disp: Dispatcher=dp):
    disp.register_message_handler(start_command, commands=["start"])
    disp.register_message_handler(help_command, commands=["help"])
