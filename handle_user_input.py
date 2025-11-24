import json
import shlex
from enum import Enum
from datetime import datetime

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)

class Status(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

def value_in_enum(enum, value):
    return value in (item.value for item in enum)

def get_all_tasks():
    try:
        with open("tasks.json", "r") as file:
            all_tasks = json.load(file)
    except FileNotFoundError:
        all_tasks = {}
    return all_tasks

def get_certain_status_tasks(status, data):
    all_tasks = get_all_tasks()

    for key in all_tasks.keys():
        if all_tasks[key]['status'] == status:
            data[key] = all_tasks[key]
    return data


def get_all_todo_tasks():
    todo_tasks = {}
    return get_certain_status_tasks(Status.TODO.value, todo_tasks)

def get_all_in_progress_tasks():
    in_progress_tasks = {}
    return get_certain_status_tasks(Status.IN_PROGRESS.value, in_progress_tasks)

def get_all_done_tasks():
    done_tasks = {}
    return get_certain_status_tasks(Status.DONE.value, done_tasks)

def commit_changes(committed_tasks):
    with open("tasks.json", "w") as task_file:
        json.dump(committed_tasks, task_file, cls=EnumEncoder, indent=4)

while True:
    full_input = input("Enter your command:")
    command_parts = shlex.split(full_input)
    command = command_parts[0]
    if command == "exit":
        break

    if command == "add":
        if len(command_parts) < 2:
            print("ERROR: You must provide an argument")
            continue

        elif len(command_parts) > 2:
            print("ERROR: add command takes only one argument")
            continue

        if command_parts[1].isdigit():
            print("ERROR: Argument must be a text")
            continue

        tasks = get_all_tasks()
        last_task_id = max(int(key) for key in tasks.keys()) if tasks else 0

        tasks[last_task_id+1] = {'description': command_parts[1],
                                 'status': Status.TODO.value,
                                 'createdAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 'updatedAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

        commit_changes(tasks)
        print(f"Task added successfully (ID: {last_task_id + 1})")

    elif command == "update":
        if len(command_parts) < 3:
            print("ERROR: Your command is missing one or more arguments")
            continue
        elif len(command_parts) > 3:
            print("ERROR: update command takes three arguments only")
            continue

        if not command_parts[1].isdigit():
            print("ERROR: First argument must be a number")
            continue
        if command_parts[2].isdigit():
            print("ERROR: Second argument must be a text")
            continue

        tasks = get_all_tasks()
        if command_parts[1] not in tasks.keys():
            print("ERROR: Task id does not exit")
            continue
        tasks[command_parts[1]]['description'] = command_parts[2]
        tasks[command_parts[1]]['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        commit_changes(tasks)


    elif command == "delete":
        if len(command_parts) < 2:
            print("ERROR: You must provide an argument")
            continue
        elif len(command_parts) > 2:
            print("ERROR: delete command takes only one argument")
            continue

        if not command_parts[1].isdigit():
            print("ERROR: the argument must be a number")
            continue

        tasks = get_all_tasks()
        if command_parts[1] not in tasks.keys():
            print("ERROR: Task id does not exit")
            continue

        del tasks[command_parts[1]]
        commit_changes(tasks)


    elif command == "mark-in-progress":
        if len(command_parts) < 2:
            print("ERROR: You must provide an argument")
            continue
        elif len(command_parts) > 2:
            print("ERROR: mark-in-progress command takes only one argument")
            continue

        if not command_parts[1].isdigit():
            print("ERROR: the argument must be a number")
            continue

        tasks = get_all_tasks()
        if command_parts[1] not in tasks.keys():
            print("ERROR: Task id does not exit")
            continue

        tasks[command_parts[1]]['status'] = Status.IN_PROGRESS.value
        tasks[command_parts[1]]['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        commit_changes(tasks)

    elif command == "mark-done":
        if len(command_parts) < 2:
            print("ERROR: You must provide an argument")
            continue
        elif len(command_parts) > 2:
            print("ERROR: mark-done command takes only one argument")
            continue

        if not command_parts[1].isdigit():
            print("ERROR: the argument must be a number")
            continue

        tasks = get_all_tasks()
        if command_parts[1] not in tasks.keys():
            print("ERROR: Task id does not exit")
            continue

        tasks[command_parts[1]]['status'] = Status.DONE.value
        tasks[command_parts[1]]['updatedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        commit_changes(tasks)

    elif command == "list":
        if len(command_parts) == 1:
            print(get_all_tasks())
            continue
        elif len(command_parts) == 2 and not value_in_enum(Status, command_parts[1]):
            print("ERROR: You must enter a valid task status")
            continue

        if command_parts[1] == Status.TODO.value:
            print(json.dumps(get_all_todo_tasks()))

        elif command_parts[1] == Status.IN_PROGRESS.value:
            print(json.dumps(get_all_in_progress_tasks()))

        elif command_parts[1] == Status.DONE.value:
            print(json.dumps(get_all_done_tasks()))

    else:
        print('Please use one of these commands: add, update, delete,'
              ' mark-in-progress, mark-done', 'list')