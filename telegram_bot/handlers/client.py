from datetime import date, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import dp, bot
from requests_aiohttp import send_request, send_request_json


class FSMCreateTask(StatesGroup):
    name = State()
    description = State()
    date = State()


class FSMUpdateTask(StatesGroup):
    pk = State()
    name = State()
    description = State()
    date = State()


class FSMDeleteTask(StatesGroup):
    pk = State()


HELP = """
This bot helps to manage your tasks.
/start - start bot
/help - list of commands
/tasks - get list of tasks
/today - get list of tasks for today
/create - create task
/edit - edit task
/delete - delete task
/done - mark task
"""


async def start_command(message: types.Message):
    data = {
        "username": message["from"]["username"],
        "password": message["from"]["id"],
    }

    response = await send_request(url="http://localhost:8000/api/v1/createuser/", data=data, method="POST")
    if response.status == 200:
        await message.answer("Start manage your tasks!")
    else:
        await message.answer("An error has occurred!")
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
        await message.reply("Enter date:\nformat: 2023-06-13 or today or tomorrow")


# The last step of creating task
async def load_taskdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "today":
            data["date"] = date.today().strftime("%Y-%m-%d")
        elif message.text == "tomorrow":
            tomorrow = date.today() + timedelta(days=1)
            data["date"] = tomorrow.strftime("%Y-%m-%d")
        else:
            data["date"] = message.text

        # Add to Database
        data_request = dict(data.items())
        data_request["username"] = message["from"]["username"]
        data_request["password"] = message["from"]["id"]

        response = await send_request(url="http://localhost:8000/api/v1/tasks/", data=data_request, method="POST")
        if response.status == 200:
            await message.reply("Task was created successfully")
            await state.finish()
        else:
            await message.answer("An error has occurred!\nEnter again your date:")



async def build_task_list_to_str(tasks):
    task_str = ""

    for num, task in enumerate(tasks, 1):
        if task["done"]:
            task_str += f"☑️ {num}. "
        else:
            task_str += f"⭕️ {num}. "
        task_str += task["name"].ljust(48, ".") + task["date"] + "\n"

    return task_str


async def get_tasks(message: types.Message):
    data = {
        "username": message["from"]["username"],
        "password": message["from"]["id"],
    }

    tasks = await send_request_json(url="http://localhost:8000/api/v1/tasks/", data=data, method="GET")
    if tasks:
        await message.answer(await build_task_list_to_str(tasks))
    else:
        await message.answer("You don't have tasks")
    await message.delete()


async def delete_tasks(message: types.Message):
    await FSMDeleteTask.pk.set()
    data = {
        "username": message["from"]["username"],
        "password": message["from"]["id"],
    }
    tasks = await send_request_json(url="http://localhost:8000/api/v1/tasks/", data=data, method="GET")
    await message.answer(await build_task_list_to_str(tasks))
    await message.reply("Enter the number of tasks to delete: \nEnter 'cancel' for cancel")


async def load_taskid_delete(message: types.Message, state: FSMContext):
    if message.text != "cancel":
        data = {
            "username": message["from"]["username"],
            "password": message["from"]["id"],
        }
        tasks = await send_request_json(url="http://localhost:8000/api/v1/tasks/", data=data, method="GET")
        try:
            data["id"] = tasks[int(message.text) - 1]["id"]
        except:
            await message.answer("An error has occurred!\nCheck is it a number and does it exist?")
        else:
            response = await send_request(url="http://localhost:8000/api/v1/tasks/", data=data, method="DELETE")
            if response.status == 200:
                await message.reply("Task was deleted successfully")
            else:
                await message.answer("An error has occurred!")
            await state.finish()
    else:
        await state.finish()


async def update_task(message: types.Message):
    await FSMUpdateTask.pk.set()
    data = {
        "username": message["from"]["username"],
        "password": message["from"]["id"],
    }
    tasks = await send_request_json(url="http://localhost:8000/api/v1/tasks/", data=data, method="GET")
    await message.answer(await build_task_list_to_str(tasks))
    await message.reply("Enter the number of tasks to update: \nEnter 'cancel' for cancel")


async def load_taskid_update(message: types.Message, state: FSMContext):
    if message.text == "cancel":
        await state.finish()
        await message.answer("Canceled")
        return

    async with state.proxy() as data:
        data["username"] = message["from"]["username"]
        data["password"] = message["from"]["id"]

        tasks = await send_request_json(url="http://localhost:8000/api/v1/tasks/", data=dict(data), method="GET")
        try:
            data["id"] = tasks[int(message.text) - 1]["id"]
        except:
            await message.answer("An error has occurred!\nCheck is it a number and does it exist?\nEnter again:")
        else:
            await FSMUpdateTask.next()
            await message.reply("Enter new name(length less than 48) or '.' for skip\n'cancel' for cancel")

async def load_task_name_update(message: types.Message, state: FSMContext):
    if message.text == "cancel":
        await state.finish()
        await message.answer("Canceled")
        return

    async with state.proxy() as data:
        if message.text != ".":
            if len(message.text) > 48:
                data["name"] = message.text[:45] + "..."
            else:
                data["name"] = message.text

        await message.reply("Enter new description or '.' for skip\n'сancel' for cancel")
        await FSMUpdateTask.next()


async def load_task_description_update(message: types.Message, state: FSMContext):
    if message.text == "cancel":
        await state.finish()
        await message.answer("Canceled")
        return

    async with state.proxy() as data:
        if message.text != ".":
            data["description"] = message.text
        await FSMUpdateTask.next()
        await message.reply("Enter new date or '.' for skip\nfoman: 2023-06-13 or today/tomorrow\n'сancel' for cancel")

async def load_task_date_update(message: types.Message, state: FSMContext):
    if message.text == "cancel":
        await state.finish()
        await message.answer("Canceled")
        return

    async with state.proxy() as data:
        if message.text != ".":
            if message.text == "today":
                data["date"] = date.today().strftime("%Y-%m-%d")
            elif message.text == "tomorrow":
                tomorrow = date.today() + timedelta(days=1)
                data["date"] = tomorrow.strftime("%Y-%m-%d")
            else:
                data["date"] = message.text

        response = await send_request(url="http://localhost:8000/api/v1/tasks/", data=dict(data), method="PUT")
        if response.status == 200:
            await message.reply("Task was updated successfully")
            await state.finish()
        else:
            await message.reply("An error has occurred!\nEnter again your date:")


def register_handlers_client(disp: Dispatcher = dp):
    disp.register_message_handler(start_command, commands=["start"])
    disp.register_message_handler(help_command, commands=["help"])
    disp.register_message_handler(create_task, commands=["create"])
    disp.register_message_handler(get_tasks, commands=["tasks"])
    disp.register_message_handler(load_taskname, state=FSMCreateTask.name)
    disp.register_message_handler(load_taskdescription, state=FSMCreateTask.description)
    disp.register_message_handler(load_taskdate, state=FSMCreateTask.date)
    disp.register_message_handler(delete_tasks, commands=["delete"])
    disp.register_message_handler(load_taskid_delete, state=FSMDeleteTask.pk)
    disp.register_message_handler(update_task, commands=["update"])
    disp.register_message_handler(load_taskid_update, state=FSMUpdateTask.pk)
    disp.register_message_handler(load_task_name_update, state=FSMUpdateTask.name)
    disp.register_message_handler(load_task_description_update, state=FSMUpdateTask.description)
    disp.register_message_handler(load_task_date_update, state=FSMUpdateTask.date)

