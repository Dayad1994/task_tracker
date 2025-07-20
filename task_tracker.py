# main.py
import datetime
import json
import os
import sys


def _read_json():
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data


def _write_json(python_data):
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(python_data, file)


def _now_datetime():
    return datetime.datetime.now().strftime('%d.%m.%Y %H:%M')


def _add(json_data, description):
    json_data['curr_id'] += 1
    task = {
        'id': json_data['curr_id'],
        'description': description,
        'status': 'todo',
        'created': _now_datetime(),
        'updated': _now_datetime()
    }
    json_data['tasks'].append(task)


def _update(json_data, id, description):
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['updated'] = _now_datetime()
            json_data['tasks'][i]['description'] = description


def _delete(json_data, id):
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'].pop(i)
            break


def _mark_in_progress(json_data, id):
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['status'] = 'in-progress'
            json_data['tasks'][i]['updated'] = _now_datetime()


def _mark_done(json_data, id):
    for i in range(len(json_data['tasks'])):
        if json_data['tasks'][i]['id'] == int(id):
            json_data['tasks'][i]['status'] = 'done'
            json_data['tasks'][i]['updated'] = _now_datetime()


def _list(json_data, _, status=None):
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


def _check_json():
    if 'tasks.json' not in os.listdir():
        tasks = {"tasks": [], "curr_id": 0}
        _write_json(tasks)


def _run_cmd(cmd: list):
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
        case _:
            raise NotImplemented

    _write_json(json_data)


def main():
    _check_json()
    _run_cmd(sys.argv[1:])


if __name__ == "__main__":
    main()
