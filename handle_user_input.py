import json
import shlex

from helper_functions import string_arg, get_all_tasks, Status, timestamp, commit_changes, digit_arg, task_exists, \
    args_count_exact, mark_tasks, value_in_enum, get_all_todo_tasks, get_all_in_progress_tasks, get_all_done_tasks

while True:
    user_input = input("Enter your command:")
    command_args = shlex.split(user_input)
    command = command_args[0]
    if command == "exit":
        break

    if command == "add":
        if len(command_args) < 2:
            print("ERROR: Add command requires description")
            continue
        if not string_arg(command_args[1]):
            continue

        tasks = get_all_tasks()
        last_task_id = max(int(key) for key in tasks.keys()) if tasks else 0
        task_id = last_task_id + 1

        description = " ".join(command_args[1:])
        tasks[task_id] = {'description': description,
                                 'status': Status.TODO.value,
                                 'createdAt': timestamp(),
                                 'updatedAt':timestamp()}

        commit_changes(tasks)
        print(f"Task added successfully (ID: {task_id})")

    elif command == "update":
        if len(command_args) < 3:
            print("ERROR: Update command requires task ID and description")
            continue

        if not digit_arg(command_args[1]):
            continue

        task_id = command_args[1]
        new_description = " ".join(command_args[2:])
        tasks = get_all_tasks()

        if not task_exists(task_id):
            continue
        tasks[task_id]['description'] = new_description
        tasks[task_id]['updatedAt'] = timestamp()

        commit_changes(tasks)
        print(f"Task updated successfully (ID: {task_id})")


    elif command == "delete":
        if not args_count_exact(command_args,2):
            continue
        if not digit_arg(command_args[1]):
            continue

        task_id = command_args[1]
        tasks = get_all_tasks()
        if not task_exists(task_id):
            continue

        del tasks[task_id]
        commit_changes(tasks)
        print(f"Task deleted successfully (ID: {task_id})")

    elif command == "mark-in-progress":
        if not args_count_exact(command_args, 2):
            continue

        if not digit_arg(command_args[1]):
            continue

        if mark_tasks(Status.IN_PROGRESS, command_args[1]):
            print(f"Task marked in-progress successfully (ID: {command_args[1]})")

    elif command == "mark-done":
        if not args_count_exact(command_args, 2):
            continue

        if not digit_arg(command_args[1]):
            continue

        if mark_tasks(Status.DONE, command_args[1]):
            print(f"Task marked done successfully (ID: {command_args[1]})")

    elif command == "list":
        if len(command_args) == 1:
            print(json.dumps(get_all_tasks(), indent=4))
            continue
        elif len(command_args) == 2 and not value_in_enum(Status, command_args[1]):
            print("ERROR: You must enter a valid task status")
            continue

        if command_args[1] == Status.TODO.value:
            print(json.dumps(get_all_todo_tasks(), indent=4))

        elif command_args[1] == Status.IN_PROGRESS.value:
            print(json.dumps(get_all_in_progress_tasks(), indent=4))

        elif command_args[1] == Status.DONE.value:
            print(json.dumps(get_all_done_tasks(), indent=4))

    else:
        print('Please use one of these commands: add, update, delete,'
              ' mark-in-progress, mark-done, list')