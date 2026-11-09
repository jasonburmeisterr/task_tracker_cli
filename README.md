# Task Tracker CLI
https://roadmap.sh/projects/task-tracker

A simple command-line task tracker written in Python. Tasks are saved to a local `tasks.json` file and displayed in a colored table using [Rich](https://github.com/Textualize/rich).

**Author:** Jason Burmeister

## Features

- Add, update, and delete tasks
- Mark tasks as `pending`, `in-progress`, or `completed`
- List all tasks, or filter by status
- Tracks when each task was created and last updated
- Color-coded status table in the terminal

## Requirements

- Python 3.8+
- [Rich](https://pypi.org/project/rich/)

## Installation

```bash
git clone <your-repo-url>
cd task-tracker-cli
pip install rich
```

On Windows, use `py -m pip install rich`.

## Usage

```bash
python main.py <command> [arguments]
```

On Windows, use `py` instead of `python`.

| Command | Description | Example |
|---|---|---|
| `add "<description>"` | Add a new task | `python main.py add "Buy groceries"` |
| `list [status]` | List all tasks, or only those with a status | `python main.py list in-progress` |
| `update <id> "<description>"` | Change a task's description | `python main.py update 1 "Buy oat milk"` |
| `mark <id> <status>` | Set a task's status | `python main.py mark 1 completed` |
| `delete <id>` | Delete a task (asks for confirmation) | `python main.py delete 1` |

Valid statuses are `pending`, `in-progress` and `completed`.

Run `python main.py -h` for help.

## Example

```text
$ python main.py add "Finish homework"
Task added successfully! (ID: 1)

$ python main.py mark 1 in-progress
Task ID 1 marked as In-Progress.

$ python main.py list
┏━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ # ┃ Description     ┃ Status      ┃ Created at          ┃ Updated at          ┃
┡━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ 1 │ Finish homework │ In-Progress │ 2026-11-09 00:30:00 │ 2026-11-09 00:31:00 │
└───┴─────────────────┴─────────────┴─────────────────────┴─────────────────────┘
```

## Data storage

Tasks are stored in `tasks.json` in the folder you run the script from. The file is created automatically the first time you run a command. Each task looks like this:

```json
{
    "id": 1,
    "description": "Finish homework",
    "status": "In-Progress",
    "created_at": "2026-11-09 00:30:00",
    "updated_at": "2026-11-09 00:31:00"
}
```
