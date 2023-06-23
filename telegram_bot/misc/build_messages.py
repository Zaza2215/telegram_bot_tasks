HELP_TEXT = """
This bot helps to manage your tasks.
/start - start bot
/help - list of commands
/tasks - get list of tasks
/task - get task in detail
/today - get list of tasks for today
/create - create task
/update - edit task
/delete - delete task
/done - mark task
"""

async def build_task_list_to_str(tasks):
    task_str = ""

    for num, task in enumerate(tasks, 1):
        if task["done"]:
            task_str += f"✅ {num}. "
        else:
            task_str += f"⭕️ {num}. "
        task_str += task["name"].ljust(48, ".") + task["date"] + "\n"

    return task_str