# main.py
import datetime
import json
import os


def parse_cmd(cmd: str):
    if not cmd.startswith('task-tracker '):
        print('Не верная команда')
        return
    cmd = cmd[13:]
    if cmd.startswith('add'):
        return ['add', cmd[5:-1]]
    if cmd.startswith('update'):
        arg1, arg2 = cmd[7:-1].split(' "')
        return ['update', arg1, arg2]
    if cmd.startswith('delete'):
        return cmd.split(' ')
    if cmd.startswith('mark'):
        return cmd.split(' ')
    if cmd.startswith('list '):
        return cmd.split(' ')
    if cmd.startswith('list'):
        return ['list', None]


def run_cmd(cmd: list):
    match cmd[0]:
        case 'add':
            add(cmd[1])
        case 'update':
            update(cmd[1], cmd[2])
        case 'delete':
            delete(cmd[1])
        case 'mark-in-progress':
            mark_in_progress(cmd[1])
        case 'mark-done':
            mark_done(cmd[1])
        case 'list':
            list(cmd[1])
        case _:
            raise Exception


def add(description):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        json_data['curr_id'] += 1
        id = json_data['curr_id']
        status = 'todo'
        now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
        created = now
        updated = now
        task = {
            'id': id,
            'description': description,
            'status': status,
            'created': created,
            'updated': updated
        }
        json_data['tasks'].append(task)
    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def update(id, description):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')

        for i in range(len(json_data['tasks'])):
            if json_data['tasks'][i]['id'] == int(id):
                json_data['tasks'][i]['updated'] = now
                json_data['tasks'][i]['description'] = description

    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def delete(id):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        for i in range(len(json_data['tasks'])):
            if json_data['tasks'][i]['id'] == int(id):
                json_data['tasks'].pop(i)
                json_data['curr_id'] -= 1
    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def mark_in_progress(id):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        for i in range(len(json_data['tasks'])):
            if json_data['tasks'][i]['id'] == int(id):
                json_data['tasks'][i]['status'] = 'in-progress'
    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def mark_done(id):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        for i in range(len(json_data['tasks'])):
            if json_data['tasks'][i]['id'] == int(id):
                json_data['tasks'][i]['status'] = 'done'
    
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(json_data, file)


def list(status):
    with open('tasks.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        for task in json_data['tasks']:
            if not status or task['status'] == status:
                print(task['id'], task['description'], task['status'])


def check_json():
    if 'tasks.json' not in os.listdir():
        with open('tasks.json', 'w', encoding='utf-8') as file:
            tasks = {"tasks": [], "curr_id": 0}
            json.dump(tasks, file)


if __name__ == "__main__":
    check_json()
    input_cmd = input('Введите команду: ')
    parsed_cmd = parse_cmd(input_cmd)
    run_cmd(parsed_cmd)
