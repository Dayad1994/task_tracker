"""Main module of app."""
__all__ = [
    'TaskData', 'main', 'check_db', 'read_db', 'write_db', 'add',
    'update', 'delete', 'mark_done', 'mark_in_progress', 'list'
    ]

import datetime
import json
import os
import sys
from typing import TypedDict

DB_FILE = 'tasks.json'
# varibale for check count of args
TWO_ARGS = 2
# varibale for check length of description
MIN_LENGTH_OF_DESCRIPTION = 5


class CommandNotFoundError(Exception):
    """Exception raised when an unknown command is entered."""
    
    def __init__(self, command: str) -> None:
        self.command = command
        super().__init__(f"Command '{command}' not exists.")


class Task(TypedDict):  
    id: int
    description: str
    status: str
    created: str
    updated: str


class TaskData(TypedDict):
    """DB dict for saving tasks."""
    tasks: list[Task]
    curr_id: int


def main() -> None:
    """Main function of app."""
    # create db if it doesn't exist
    check_db(DB_FILE)
    
    # should be at least 2 args
    if len(sys.argv) < TWO_ARGS:
        help()
        return
    
    try:
        # cli args without main cmd 'tasker'
        _run_cmd(*sys.argv[1:])
    except CommandNotFoundError as err:
        print(err)
    except IndexError:
        print("There isn't task with this id!")
    except ValueError as err:
        print(err)
    except TypeError as err:
        print(err)


def check_db(path: str) -> None:
    """Create a database file in the current directory if it does not exist."""
    if path not in os.listdir():
        tasks = {"tasks": [], "curr_id": 0}
        write_db(path, tasks)


def read_db(path: str) -> TaskData:
    """Read and convert json data from db to python object."""
    with open(path, encoding='utf-8') as file:
        json_data: TaskData = json.load(file)
    return json_data


def write_db(path: str, python_data: TaskData) -> None:
    """Convert and write python object to json data to db."""
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(python_data, file)


def _run_cmd(cmd: str, *args: tuple) -> None:
    """Run the provided command with arguments.

    Accesses the database for reading and writing.
    """
    # Read json data from db
    json_data: TaskData = read_db(DB_FILE)

    match cmd:
        case 'help':
            help()
            return
        case 'add':
            add(json_data, *args)
        case 'update':
            update(json_data, *args)
        case 'delete':
            delete(json_data, *args)
        case 'mark-in-progress':
            mark_in_progress(json_data, *args)
        case 'mark-done':
            mark_done(json_data, *args)
        case 'list':
            list(json_data, *args)
            return
        case _:
            raise CommandNotFoundError(cmd)

    # write data to db
    write_db(DB_FILE, json_data)


def help() -> None:
    """Help command."""
    commands = [
        ("add",
         "add a new task. 1 positional argument - description",
         '`add "go to job"`'),
        ("update",
         "update description of the task. 2 positional args: id, description",
         '`update 1 "go to job and gym"`'),
        ("delete",
         "delete a task. 1 positional arg - id",
         '`delete 1`'),
        ("mark-done",
         "mark a task as done. 1 positional arg - id",
         '`mark-done 1`'),
        ("mark-in-progress",
         "mark a task as in-progress. 1 positional arg - id",
         '`mark-in-progress 1`'),
        ("list",
         "print tasks. Nothing or 1 positional arg - done/in-progress/todo",
         '`list`, `list todo`'),
    ]

    for cmd, desc, example in commands:
        print(f"{cmd.ljust(18)}{desc}\n{' ' * 18}Example: {example}\n")


def add(json_data: TaskData, description: str) -> None:
    """Create and add a new task to the list of tracked tasks."""
    _is_valid_description(description)
    
    json_data['curr_id'] += 1
    now_time = _now_datetime()
    task = {
        'id': json_data['curr_id'],
        'description': description.strip(),
        'status': 'todo',
        'created': now_time,
        'updated': now_time
    }
    json_data['tasks'].append(task)


def _now_datetime() -> str:
    """Return the current timestamp as a string.
    
    Return format 'DD.MM.YYYY HH:MM' (e.g., '20.07.2025 15:56').
    """
    return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')


def _is_valid_description(desc: str) -> None:
    if len(desc) < MIN_LENGTH_OF_DESCRIPTION:
        raise ValueError('description must be longer than 4 symbols')


def update(
    json_data: TaskData,
    id: int,
    description: str) -> None:
    """Update the task description by ID."""
    _is_valid_id(id)
    _is_valid_description(description)
    _update_task(json_data, id, description=description.strip())


def _is_valid_id(id: int) -> None:
    if id < 1:
        raise ValueError('id must be int and more than 0')


def _update_task(json_data: TaskData, id: int, **fields: dict) -> None:
    index = _find_index_of_task(json_data, id)
    task = json_data['tasks'][index]
    task.update(fields)
    task['updated'] = _now_datetime()


def _find_index_of_task(json_data: TaskData, id: int) -> int:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            return i
    raise IndexError


def delete(json_data: TaskData, id: int) -> None:
    """Delete the task by ID."""
    _is_valid_id(id)
    index_of_task =_find_index_of_task(json_data, id)
    json_data['tasks'].pop(index_of_task)


def mark_in_progress(json_data: TaskData, id: int) -> None:
    """Mark task status to 'in-progress' by ID."""
    _is_valid_id(id)
    _update_task(json_data, id, status='in-progress')


def mark_done(json_data: TaskData, id: int) -> None:
    """Mark task status to 'done' by ID."""
    _is_valid_id(id)
    _update_task(json_data, id, status='done')          


def list(json_data: TaskData, status: str | None = None) -> None:
    """Show all tasks or tasks filtered by the given status in the console."""
    _is_valid_status(status)

    # Show names of task fields
    print(
        'id',
        'description'.rjust(30),
        'status'.rjust(11),
        'created'.rjust(16),
        'updated'.rjust(16),
        sep=' | ')
    # seperate line between names and values of task fields
    print('-'*87)
    
    # values of task fields
    for task in json_data['tasks']:
        if not status or task['status'] == status:
            print(
                str(task['id']).rjust(2),
                task['description'].rjust(30),
                task['status'].rjust(11),
                task['created'],
                task['updated'],
                sep=' | ')


def _is_valid_status(status: str) -> None:
    if status not in (None, 'todo', 'done', 'in-progress'):
        raise ValueError('Status must be done, todo, in-progrees or None')
