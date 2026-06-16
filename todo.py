"""
=============================================================================
Task Management Application (To-Do App)
=============================================================================
A simple, menu-driven To-Do application in Python that helps students and
professionals manage daily tasks. It supports the full workflow:

    - Create  a new task
    - Read    (view all tasks / view one task)
    - Update  an existing task
    - Delete  a task
    - Mark    a task as done / not done

Tasks are saved to a JSON file ('tasks.json') so your data is not lost when
you close the program.

How to run:
    python todo.py

No external libraries are required - everything used here is part of
Python's standard library.
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import json                    # To save/load tasks in a structured file
import os                      # To check if the data file exists
from datetime import datetime  # To timestamp when a task is created


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

# The file where all tasks are stored on disk.
# Using JSON keeps the data human-readable and easy to load back later.
DATA_FILE = "tasks.json"


# ─────────────────────────────────────────────────────────────────────────────
# DATA HELPERS (load & save)
# ─────────────────────────────────────────────────────────────────────────────

def load_tasks():
    """
    Load the list of tasks from the JSON file.

    How it works:
        - If the file exists, read it and return the list of tasks.
        - If it does not exist yet (first run), return an empty list.

    Returns:
        list: A list of task dictionaries.
    """
    if os.path.exists(DATA_FILE):
        # Open the file and parse its JSON content into a Python list
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    # No file yet -> start with no tasks
    return []


def save_tasks(tasks):
    """
    Save the list of tasks back to the JSON file.

    Args:
        tasks (list): The list of task dictionaries to store.

    How it works:
        - Write the list to disk as nicely formatted JSON (indent=4).
        - This overwrites the file each time so it always reflects the
          current state of all tasks.
    """
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    """
    Work out the ID number for the next new task.

    How it works:
        - If there are no tasks, the first ID is 1.
        - Otherwise, find the highest existing ID and add 1.
        - This guarantees every task has a unique, increasing ID.

    Args:
        tasks (list): The current list of tasks.

    Returns:
        int: The ID to assign to the next task.
    """
    if not tasks:
        return 1
    # max() finds the biggest id among all tasks; +1 makes it unique
    return max(task["id"] for task in tasks) + 1


# ─────────────────────────────────────────────────────────────────────────────
# CORE FEATURES (Create, Read, Update, Delete)
# ─────────────────────────────────────────────────────────────────────────────

def add_task(tasks):
    """
    CREATE: Add a new task to the list.

    How it works:
        1. Ask the user for a title (required) and an optional description.
        2. Build a task dictionary with a unique ID, status, and timestamp.
        3. Append it to the list and save to disk.
    """
    print("\n--- Add a New Task ---")
    title = input("Task title: ").strip()

    # A task must have a title; if empty, cancel the operation
    if not title:
        print("Title cannot be empty. Task not added.")
        return

    description = input("Description (optional): ").strip()

    # Build the task as a dictionary (key-value pairs)
    task = {
        "id": get_next_id(tasks),                       # unique number
        "title": title,                                 # what to do
        "description": description,                     # extra details
        "done": False,                                  # not completed yet
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")  # timestamp
    }

    tasks.append(task)   # add the new task to our list
    save_tasks(tasks)    # write the updated list to the file
    print(f"Task added successfully with ID {task['id']}.")


def view_tasks(tasks):
    """
    READ: Display all tasks in a clean, readable table-like format.

    How it works:
        - If there are no tasks, tell the user.
        - Otherwise, loop through and print each task with its status.
    """
    print("\n--- Your Tasks ---")

    if not tasks:
        print("No tasks yet. Add one to get started!")
        return

    # Loop over every task and print its details
    for task in tasks:
        # Show a checkmark for done tasks, empty box for pending ones
        status = "[X]" if task["done"] else "[ ]"
        print(f"{status} ID {task['id']}: {task['title']}")
        if task["description"]:
            print(f"      Notes: {task['description']}")
        print(f"      Created: {task['created_at']}")
    print("------------------")


def find_task(tasks, task_id):
    """
    Helper: Find a single task by its ID.

    Args:
        tasks (list): The list of tasks to search.
        task_id (int): The ID we are looking for.

    Returns:
        dict or None: The matching task, or None if not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task(tasks):
    """
    UPDATE: Change the title or description of an existing task.

    How it works:
        1. Ask which task ID to update.
        2. Find that task.
        3. Let the user type new values (pressing Enter keeps the old value).
        4. Save the changes.
    """
    print("\n--- Update a Task ---")
    task_id = read_int("Enter the ID of the task to update: ")
    task = find_task(tasks, task_id)

    # If no task has that ID, stop here
    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    print("Press Enter to keep the current value.")

    # Ask for a new title; keep the old one if the user types nothing
    new_title = input(f"New title [{task['title']}]: ").strip()
    if new_title:
        task["title"] = new_title

    # Same idea for the description
    new_desc = input(f"New description [{task['description']}]: ").strip()
    if new_desc:
        task["description"] = new_desc

    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")


def toggle_done(tasks):
    """
    UPDATE (status): Mark a task as done, or undo it if already done.

    How it works:
        - Find the task by ID.
        - Flip its 'done' value (True <-> False).
        - Save the change.
    """
    print("\n--- Mark Task Done / Not Done ---")
    task_id = read_int("Enter the ID of the task: ")
    task = find_task(tasks, task_id)

    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    # 'not' flips a boolean: True becomes False and vice versa
    task["done"] = not task["done"]
    save_tasks(tasks)

    state = "done" if task["done"] else "not done"
    print(f"Task {task_id} marked as {state}.")


def delete_task(tasks):
    """
    DELETE: Remove a task from the list permanently.

    How it works:
        1. Ask which task ID to delete.
        2. Confirm it exists.
        3. Rebuild the list without that task, then save.
    """
    print("\n--- Delete a Task ---")
    task_id = read_int("Enter the ID of the task to delete: ")
    task = find_task(tasks, task_id)

    if task is None:
        print(f"No task found with ID {task_id}.")
        return

    # Keep every task EXCEPT the one with the matching id
    tasks[:] = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")


# ─────────────────────────────────────────────────────────────────────────────
# INPUT HELPER
# ─────────────────────────────────────────────────────────────────────────────

def read_int(prompt):
    """
    Safely read a whole number from the user.

    Why we need this:
        - input() always returns text. If we try to use text where a number
          is expected, the program could crash.
        - This loops until the user types a valid integer.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        int: The number the user entered.
    """
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("Please enter a valid number.")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """
    The main program loop.

    How it works:
        - Load existing tasks from disk once at the start.
        - Show a menu over and over until the user chooses to exit.
        - Each menu choice calls the matching function above.
    """
    tasks = load_tasks()  # bring back any tasks saved from previous runs

    print("=" * 40)
    print("        TASK MANAGER (To-Do App)")
    print("=" * 40)

    while True:
        # Display the menu of options
        print("\nWhat would you like to do?")
        print("  1. Add a task")
        print("  2. View all tasks")
        print("  3. Update a task")
        print("  4. Mark task done / not done")
        print("  5. Delete a task")
        print("  6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        # Run the action that matches the user's choice
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            toggle_done(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            print("Goodbye! Your tasks are saved.")
            break  # exit the while loop -> program ends
        else:
            print("Invalid choice. Please pick a number from 1 to 6.")


# This runs main() only when the file is executed directly (best practice).
if __name__ == "__main__":
    main()
