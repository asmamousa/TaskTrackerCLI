
# TaskTrackerCLI

A command-line task tracker built as a solution for the assignment:  
https://roadmap.sh/projects/task-tracker


## 🚀 How to Use

###  From Terminal or cmd
Run the script:

```bash
python handle_user_input.py
````

or

```bash
python3 handle_user_input.py
```

---

## 📝 Supported Commands

### **Add a new task**

```bash
add <task title>
add "first task"
```

### **Update an existing task**

```bash
update <task id> <new title>
update 1 "updated first task title"
```

### **Delete a task**

```bash
delete <task id>
```

### **Mark task as in progress or done**

```bash
mark-in-progress <task id>
mark-done <task id>
```

### **List tasks**

All tasks:

```bash
list
```

Filter by status:

```bash
list done
list todo
list in-progress
```

---

## 📌 Examples

```bash
# Adding a new task
task-cli add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
task-cli update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task status
task-cli mark-in-progress 1
task-cli mark-done 1

# Listing tasks
task-cli list
task-cli list done
task-cli list todo
task-cli list in-progress
```

---