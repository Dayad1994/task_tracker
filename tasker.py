'''Main module of app'''

import datetime
import json
import os
import sys


from typing import TypedDict


class CommandNotFoundError(Exception):
    '''Exception raised when an unknown command is entered.'''
    
    def __init__(self, command: str):
        self.command = command
        super().__init__(f"Command '{command}' not exists.")


class Task(TypedDict):  
    id: int
    description: str
    status: str
    created: str
    updated: str


class TaskData(TypedDict):
    tasks: list[Task]
    curr_id: int


def main() -> None:
    '''Main function of app'''
    # create db if it doesn't exist
    _check_db()
    
    # check for args
    if len(sys.argv) < 2:
        _help()
        return
    
    try:
        # cli args without main cmd 'task-tracker'
        _run_cmd(*sys.argv[1:])
    except CommandNotFoundError as err:
        print(err)
    except IndexError as err:
        print("Нет задачи с таким id!")
    except ValueError as err:
        print('id must be number')
    except TypeError as err:
        print(err)


def _check_db() -> None:
    '''Creates the database file in the current directory if it doesn't exist.'''
    
    if 'tasks.json' not in os.listdir():
        tasks = {"tasks": [], "curr_id": 0}
        _write_db(tasks)


def _read_db() -> TaskData:
    '''Read and convert json data from db to python object.'''
    
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data: TaskData = json.load(file)
    return json_data


def _write_db(python_data: TaskData) -> None:
    '''Convert and write python object to json data to db.'''
    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(python_data, file)


def _run_cmd(cmd: str, *args: tuple) -> None:
    '''Runs the provided command with arguments, accessing the database for reading and writing.'''
    
    # Read json data from db
    json_data: TaskData = _read_db()

    match cmd:
        case 'help':
            _help()
            return
        case 'add':
            _add(json_data, *args)
        case 'update':
            _update(json_data, *args)
        case 'delete':
            _delete(json_data, *args)
        case 'mark-in-progress':
            _mark_in_progress(json_data, *args)
        case 'mark-done':
            _mark_done(json_data, *args)
        case 'list':
            _list(json_data, cmd, *args)
            return
        case _:
            raise CommandNotFoundError(cmd)

    # write data to db
    _write_db(json_data)


def _help() -> None:
    '''Help command'''
    
    print(
        'add               command add new task. includes one positional argument - description',
        '                  add "go to job"\n',
        'update            command update description of task. includes two positional args: id, description',
        '                  update 1 "got to job and gym"\n',
        'delete            command delete task. includes one positional arg - id',
        '                  delete 1\n',
        'mark-done         command mark status of task to done. includes one positional arg - id',
        '                  mark-done 1\n',
        'mark-in-progress  command mark status of task to in-progress. includes one positional arg - id',
        '                  mark-in-progress 1\n',
        'list              command print tasks. includes zero or one positional arg - done/in-progress/todo',
        '                  list - print all tasks',
        '                  list todo - print tasks with "todo" status\n',
        sep='\n'
    )


def _add(json_data: TaskData, description: str) -> None:
    '''Create and add a new task to the list of tracked tasks.'''
    
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
    '''Return the current timestamp in the following format: "20.07.2025 15:56"'''

    return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')


def _update(
    json_data: TaskData,
    id: int,
    description: str) -> None:
    '''Update the task description by ID.'''
    
    _update_task(json_data, id, description=description.strip())


def _find_index_of_task(json_data: TaskData, id: int) -> int:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            return i
    else:
        raise IndexError


def _update_task(json_data: TaskData, id: int, **fields) -> None:
    index = _find_index_of_task(json_data, id)
    task = json_data['tasks'][index]
    task.update(fields)
    task['updated'] = _now_datetime()


def _delete(json_data: TaskData, id: int) -> None:
    '''Delete the task by ID.'''
    
    index_of_task =_find_index_of_task(json_data, id)
    json_data['tasks'].pop(index_of_task)


def _mark_in_progress(json_data: TaskData, id: int) -> None:
    '''Mark task status to 'in-progress' by ID.'''

    _update_task(json_data, id, status='in-progress')


def _mark_done(json_data: TaskData, id: int) -> None:
    '''Mark task status to 'done' by ID.'''
    
    _update_task(json_data, id, status='done')          


def _list(json_data: TaskData, _, status=None) -> None:
    '''Show all tasks or tasks filtered by the given status in the console.'''
    
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
