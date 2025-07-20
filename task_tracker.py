# main.py
import datetime
import json
import os
import sys


class CommandNotFoundError(Exception):
    '''Исключение, вызываемое при вводе несуществующей команды.'''
    def __init__(self, command: str):
        self.command = command
        super().__init__(f"Команда '{command}' не существует.")


def _read_json() -> dict[str: list, str: int]:
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def _write_json(python_data: dict[str: list, str: int]) -> None:
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(python_data, file)


def _now_datetime() -> str:
    return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')


def _add(json_data: dict[str: list, str: int], description: str) -> None:
    json_data['curr_id'] += 1
    task = {
        'id': json_data['curr_id'],
        'description': description.strip(),
        'status': 'todo',
        'created': _now_datetime(),
        'updated': _now_datetime()
    }
    json_data['tasks'].append(task)


def _update(
    json_data: dict[str: list, str: int],
    id: int,
    description: str) -> None:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['updated'] = _now_datetime()
            json_data['tasks'][i]['description'] = description.strip()
            break
    else:
        raise IndexError


def _delete(json_data: dict[str: list, str: int], id: int) -> None:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'].pop(i)
            break
    else:
        raise IndexError


def _mark_in_progress(json_data: dict[str: list, str: int], id: int) -> None:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['status'] = 'in-progress'
            json_data['tasks'][i]['updated'] = _now_datetime()
            break
    else:
        raise IndexError


def _mark_done(json_data: dict[str: list, str: int], id: id) -> None:
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['status'] = 'done'
            json_data['tasks'][i]['updated'] = _now_datetime()
            break
    else:
        raise IndexError


def _list(json_data: dict[str: list, str: int], _, status=None) -> None:
    print(
        'id',
        'description'.rjust(30),
        'status'.rjust(11),
        'created'.rjust(16),
        'updated'.rjust(16),
        sep=' | ')
    print('-'*87)

    for task in json_data['tasks']:
        if not status or task['status'] == status:
            print(
                str(task['id']).rjust(2),
                task['description'].rjust(30),
                task['status'].rjust(11),
                task['created'].rjust(16),
                task['updated'].rjust(16),
                sep=' | ')


def _help() -> None:
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


def _check_json() -> None:
    if 'tasks.json' not in os.listdir():
        tasks = {"tasks": [], "curr_id": 0}
        _write_json(tasks)


def _run_cmd(cmd: list) -> None:
    json_data = _read_json()

    match cmd[0]:
        case 'add':
            _add(json_data, cmd[1])
        case 'update':
            _update(json_data, cmd[1], cmd[2])
        case 'delete':
            _delete(json_data, cmd[1])
        case 'mark-in-progress':
            _mark_in_progress(json_data, cmd[1])
        case 'mark-done':
            _mark_done(json_data, cmd[1])
        case 'list':
            _list(json_data, *cmd)
            return
        case 'help':
            _help()
            return
        case _:
            raise CommandNotFoundError(cmd[0])

    _write_json(json_data)


def main() -> None:
    _check_json()
    
    try:
        _run_cmd(sys.argv[1:])
    except CommandNotFoundError as err:
        print(err)
    except IndexError as err:
        print("Нет задачи с таким id!")
    except ValueError as err:
        print('id must be number')
