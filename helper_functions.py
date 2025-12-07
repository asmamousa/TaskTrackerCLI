import json
from enum import Enum
from datetime import datetime

file_name = "tasks.json"

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
    return value in {item.value for item in enum}

def get_all_tasks():

    try:
        with open(file_name, "r") as file:
            all_tasks = json.load(file)
    except FileNotFoundError:
        all_tasks = {}
    return all_tasks

def get_certain_status_tasks(status):
    return \
        {k: v for k, v in get_all_tasks().items() if v['status'] == status}

def get_all_todo_tasks():
    return get_certain_status_tasks(Status.TODO.value)

def get_all_in_progress_tasks():
    return get_certain_status_tasks(Status.IN_PROGRESS.value)

def get_all_done_tasks():
    return get_certain_status_tasks(Status.DONE.value)

def commit_changes(committed_tasks):
    with open(file_name, "w") as task_file:
        json.dump(committed_tasks, task_file, cls=EnumEncoder, indent=4)

def args_count_exact(args, args_count):
    if len(args) != args_count:
        print(f"ERROR: Command must have exactly {args_count - 1} argument(s)")
        return False
    return True

def string_arg(arg):
    if arg.isdigit():
        print("ERROR: Argument must be a text")
        return False
    return True

def digit_arg(arg):
    if not arg.isdigit():
        print("ERROR: Argument must be a number")
        return False
    return True

def task_exists(task_id):
    tasks = get_all_tasks()
    if task_id not in tasks.keys():
        print("ERROR: Task id does not exist")
        return False
    return True

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def mark_tasks(status, task_id):
    all_tasks = get_all_tasks()
    if not task_exists(task_id):
        return False
    all_tasks[task_id]['status'] = status.value
    all_tasks[task_id]['updatedAt'] = timestamp()

    commit_changes(all_tasks)
    return True