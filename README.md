# Task Management Application (To-Do App) — Python

A simple, menu-driven To-Do application built in Python to streamline daily
task management for students and professionals. It supports the full task
workflow — creation, updates, deletion, and retrieval — through an intuitive
command-line interface, with no technical complexity.

## Features

- **Create** new tasks with a title and optional description
- **View** all tasks with their status, notes, and creation time
- **Update** a task's title or description
- **Mark** tasks as done / not done
- **Delete** tasks you no longer need
- **Automatic saving** — tasks persist in `tasks.json` between runs

## How to Run

No external libraries needed (uses only Python's standard library):

```bash
python todo.py
```

You'll see a menu. Type the number of the action you want and follow the prompts.

## How It Works

| Part | What it does |
|------|--------------|
| `load_tasks()` / `save_tasks()` | Read and write tasks to `tasks.json` so data isn't lost. |
| `get_next_id()` | Assigns each task a unique, increasing ID. |
| `add_task()` | Creates a new task (CREATE). |
| `view_tasks()` | Lists all tasks (READ). |
| `update_task()` / `toggle_done()` | Edits a task or flips its done status (UPDATE). |
| `delete_task()` | Removes a task (DELETE). |
| `read_int()` | Safely reads numbers so bad input won't crash the app. |
| `main()` | Shows the menu and routes each choice to the right function. |

## Data Format

Each task is stored as a simple record:

```json
{
    "id": 1,
    "title": "Finish assignment",
    "description": "Chapter 4 exercises",
    "done": false,
    "created_at": "2026-06-16 17:00"
}
```

This is a learning/demo project that focuses on clear, well-commented code.
