from aiogram.dispatcher.filters.state import State, StatesGroup


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


class FSMDoneTask(StatesGroup):
    pk = State()


class FSMByIdTask(StatesGroup):
    pk = State()
