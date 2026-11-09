# TASK TRACKER PROJ
# JASON BURMEISTER

import argparse
import json
import os
import time
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

TASKS_FILE = 'tasks.json'
STATUSES = {'pending': 'Pending', 'in-progress': 'In-Progress', 'completed': 'Completed'}
STATUS_COLORS = {'Pending': 'green', 'In-Progress': 'purple', 'Completed': 'cyan'}

console = Console()

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as file:
            json.dump([], file)
        return []
    with open(TASKS_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    return max([task['id'] for task in tasks], default=0) + 1


def add_task(description):
    tasks = load_tasks()
    task_id = get_next_id(tasks)
    timestamp = now()
    tasks.append({
        'id': task_id,
        'description': description,
        'status': 'Pending',
        'created_at': timestamp,
        'updated_at': timestamp,
    })
    save_tasks(tasks)
    console.print(f"[green]Task added successfully! (ID: {task_id})[/green]")


def list_tasks(status=None):
    """List tasks filtered by status, or all tasks if no status is given."""
    tasks = load_tasks()
    if status:
        wanted = STATUSES.get(status.lower())
        tasks = [t for t in tasks if t['status'] == wanted]
    if not tasks:
        console.print("[red]No tasks found.[/red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    for col in ("#", "Description", "Status", "Created at", "Updated at"):
        table.add_column(col)
    for task in tasks:
        color = STATUS_COLORS.get(task['status'], 'white')
        table.add_row(
            str(task['id']),
            task['description'],
            f"[{color}]{task['status']}[/{color}]",
            task['created_at'],
            task['updated_at'],
        )
    console.print(table)


def update_task_status(task_id, new_status):
    """Update the status of a task."""
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            task['updated_at'] = now()
            save_tasks(tasks)
            console.print(f"[green]Task ID {task_id} marked as {new_status}.[/green]")
            return
    console.print(f"[red]Task ID {task_id} not found.[/red]")


def delete_task(task_id):
    """Delete a task by its id."""
    tasks = load_tasks()
    remaining = [t for t in tasks if t['id'] != task_id]
    if len(remaining) == len(tasks):
        console.print(f"[red]Task ID {task_id} not found.[/red]")
        return
    save_tasks(remaining)
    console.print(f"[yellow]Task ID {task_id} deleted successfully.[/yellow]")


def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['description'] = new_description
            task['updated_at'] = now()
            save_tasks(tasks)
            console.print(f"[green]Task ID {task_id} description updated.[/green]")
            return
    console.print(f"[red]Task ID {task_id} not found.[/red]")


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p = subparsers.add_parser("add", help="Add a new task")
    p.add_argument("description", type=str, help="Description of the task")

    p = subparsers.add_parser("list", help="List all tasks")
    p.add_argument("status", type=str, nargs='?', default=None,
                   choices=list(STATUSES), help="Status of the tasks to list (optional)")

    p = subparsers.add_parser("update", help="Update an existing task")
    p.add_argument("id", type=int, help="ID of the task to update")
    p.add_argument("description", type=str, help="New description of the task")

    p = subparsers.add_parser("mark", help="Mark a task's status")
    p.add_argument("id", type=int, help="ID of the task to mark")
    p.add_argument("status", type=str, choices=list(STATUSES), help="New status of the task")

    p = subparsers.add_parser("delete", help="Delete a task")
    p.add_argument("id", type=int, help="ID of the task to delete")

    args = parser.parse_args()

    
    console.print("Welcome to jason burmeister task tracker", style="green")

    if args.command == "add":
        add_task(args.description)
    elif args.command == "list":
        list_tasks(args.status)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "mark":
        update_task_status(args.id, STATUSES[args.status])
    elif args.command == "delete":
        if Prompt.ask(f"Are you sure you want to delete task {args.id}?", choices=["y", "n"]) == "y":
            delete_task(args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()