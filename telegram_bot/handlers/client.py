from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from telegram_bot.create_bot import dp, bot


class FSMCreateTask(StatesGroup):
    name = State()
    description = State()
    date = State()


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


# Creating task
async def create_task(message: types.Message):
    await FSMCreateTask.name.set()
    await message.reply("Enter your task:")


# First step of creating task
async def load_taskname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
        await FSMCreateTask.next()
        await message.reply("Enter your description:")

# Second step of creating task
async def load_taskdescription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["description"] = message.text
        await FSMCreateTask.next()
        await message.reply("Enter date:\nformat: 2023-06-13")

# The last step of creating task
async def load_taskdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["date"] = message.text
        await message.reply(str(data.items()))

    # Add to Database

    await state.finish()


def register_handlers_client(disp: Dispatcher=dp):
    disp.register_message_handler(start_command, commands=["start"])
    disp.register_message_handler(help_command, commands=["help"])
    disp.register_message_handler(create_task, commands=["create"])
    disp.register_message_handler(load_taskname, state=FSMCreateTask.name)
    disp.register_message_handler(load_taskdescription, state=FSMCreateTask.description)
    disp.register_message_handler(load_taskdate, state=FSMCreateTask.date)
