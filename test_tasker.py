import unittest

from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
from tasker import _add, _update, _delete, _mark_done, _mark_in_progress, _list, TaskData


class TestAddFunction(unittest.TestCase):
    
    def setUp(self):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        return super().setUp()

    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_for_adding_correct_task(self, _):
        _add(self.json_data, "Buy milk")
        task = self.json_data["tasks"][0]
        
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Buy milk")
        self.assertEqual(task["status"], "todo")
        self.assertEqual(task["created"], "01.01.2025 12:00")
        self.assertEqual(task["updated"], "01.01.2025 12:00")
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_raises_value_type_error(self, _):
        _add(self.json_data, "Buy milk")
        
        with self.assertRaises(ValueError):
            # arg must be more than 4 symbols
            _add(self.json_data, "tooo")
        with self.assertRaises(ValueError):
            _add(self.json_data, "")
        with self.assertRaises(TypeError):
            _add(self.json_data)
        with self.assertRaises(TypeError):
            _add(self.json_data, "buy groceries", 1)
            
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_side_effect_changes_in_json_data(self, _):
        _add(self.json_data, "Buy milk")
        
        self.assertEqual(len(self.json_data["tasks"]), 1)
        self.assertEqual(self.json_data["curr_id"], 1)
        
        _add(self.json_data, "Buy milk")
        
        self.assertEqual(len(self.json_data["tasks"]), 2)
        self.assertEqual(self.json_data["curr_id"], 2)


class TestUpdateFunction(unittest.TestCase):
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def setUp(self, _):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        _add(self.json_data, "Buy milk")
        task = self.json_data["tasks"][0]
        self.id = task['id']
        self.desc = task['description']
        self.status = task['status']
        self.created = task['created']
        self.updated = task['updated']
        return super().setUp()

    @patch('tasker._now_datetime', return_value="01.01.2025 14:00")
    def test_update_for_correct_updating_task(self, _):
        _update(self.json_data, 1, "Buy water")
        task = self.json_data["tasks"][0]
        
        self.assertEqual(task["id"], self.id)
        self.assertNotEqual(task["description"], self.desc)
        self.assertEqual(task["status"], self.status)
        self.assertEqual(task["created"], self.created)
        self.assertNotEqual(task["updated"], self.updated)

    @patch('tasker._now_datetime', return_value="01.01.2025 14:00")
    def test_update_raises_value_type_index_error(self, _):
        _update(self.json_data, 1, "Buy water")
        
        with self.assertRaises(TypeError):
            _update(self.json_data)
        with self.assertRaises(TypeError):
            _update(self.json_data, 1)
        with self.assertRaises(TypeError):
            _update(self.json_data, 1, "Buy water", 'done')
        with self.assertRaises(ValueError):
            # arg must be more than 4 symbols
            _update(self.json_data, 1, "tooo")
        with self.assertRaises(TypeError):
            _update(self.json_data, "", "Buy water")
        with self.assertRaises(TypeError):
            _update(self.json_data, "hi", "Buy water")
        with self.assertRaises(ValueError):
            _update(self.json_data, 0, "Buy water")
        with self.assertRaises(IndexError):
            _update(self.json_data, 100, "Buy water")
    
    @patch('tasker._now_datetime', return_value="01.01.2025 14:00")
    def test_update_side_effect_not_changes_in_json_data(self, _):
        _update(self.json_data, 1, "Buy water")
        
        self.assertEqual(len(self.json_data["tasks"]), 1)
        self.assertEqual(self.json_data["curr_id"], 1)


class TestDeleteFunction(unittest.TestCase):
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def setUp(self, _):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        _add(self.json_data, "Buy milk")
        return super().setUp()

    def test_delete_for_correct_delete_task(self):
        _delete(self.json_data, 1)
        
        with self.assertRaises(IndexError):
            self.json_data["tasks"][1]

    def test_delete_raises_value_type_index_error(self):
        _delete(self.json_data, 1)
        
        with self.assertRaises(TypeError):
            _delete(self.json_data)
        with self.assertRaises(TypeError):
            _delete(self.json_data, 1, 1)
        with self.assertRaises(TypeError):
            _delete(self.json_data, "Buy water")
        with self.assertRaises(TypeError):
            _delete(self.json_data, "")
        with self.assertRaises(IndexError):
            _delete(self.json_data, 100)
        with self.assertRaises(ValueError):
            _delete(self.json_data, 0)

    def test_delete_side_effect_changes_in_json_data(self):
        _delete(self.json_data, 1)
        
        self.assertEqual(len(self.json_data["tasks"]), 0)
        self.assertEqual(self.json_data["curr_id"], 1)


class TestMarkInProgressFunction(unittest.TestCase):
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def setUp(self, _):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        _add(self.json_data, "Buy milk")
        task = self.json_data["tasks"][0]
        self.id = task['id']
        self.desc = task['description']
        self.created = task['created']
        self.updated = task['updated']
        return super().setUp()

    @patch('tasker._now_datetime', return_value="01.01.2025 14:00")
    def test_mark_in_progress_for_correct_updating_task(self, _):
        _mark_in_progress(self.json_data, 1)
        task = self.json_data["tasks"][0]
        
        self.assertEqual(task["id"], self.id)
        self.assertEqual(task["description"], self.desc)
        self.assertEqual(task["status"], 'in-progress')
        self.assertEqual(task["created"], self.created)
        self.assertNotEqual(task["updated"], self.updated)

    def test_mark_in_progress_raises_value_type_index_error(self):
        _mark_in_progress(self.json_data, 1)
        
        with self.assertRaises(TypeError):
            _mark_in_progress(self.json_data)
        with self.assertRaises(TypeError):
            _mark_in_progress(self.json_data, 1, 1)
        with self.assertRaises(TypeError):
            _mark_in_progress(self.json_data, "Buy water")
        with self.assertRaises(TypeError):
            _mark_in_progress(self.json_data, "")
        with self.assertRaises(IndexError):
            _mark_in_progress(self.json_data, 100)
        with self.assertRaises(ValueError):
            _mark_in_progress(self.json_data, 0)

    def test_mark_in_progress_side_effect_changes_in_json_data(self):
        _mark_in_progress(self.json_data, 1)

        self.assertEqual(len(self.json_data["tasks"]), 1)
        self.assertEqual(self.json_data["curr_id"], 1)


class TestMarkDoneFunction(unittest.TestCase):
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def setUp(self, _):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        _add(self.json_data, "Buy milk")
        task = self.json_data["tasks"][0]
        self.id = task['id']
        self.desc = task['description']
        self.created = task['created']
        self.updated = task['updated']
        return super().setUp()

    @patch('tasker._now_datetime', return_value="01.01.2025 14:00")
    def test_mark_done_for_correct_updating_task(self, _):
        _mark_done(self.json_data, 1)
        task = self.json_data["tasks"][0]
        
        self.assertEqual(task["id"], self.id)
        self.assertEqual(task["description"], self.desc)
        self.assertEqual(task["status"], 'done')
        self.assertEqual(task["created"], self.created)
        self.assertNotEqual(task["updated"], self.updated)

    def test_mark_done_raises_value_type_index_error(self):
        _mark_done(self.json_data, 1)
        
        with self.assertRaises(TypeError):
            _mark_done(self.json_data)
        with self.assertRaises(TypeError):
            _mark_done(self.json_data, 1, 1)
        with self.assertRaises(TypeError):
            _mark_done(self.json_data, "Buy water")
        with self.assertRaises(TypeError):
            _mark_done(self.json_data, "")
        with self.assertRaises(IndexError):
            _mark_done(self.json_data, 100)
        with self.assertRaises(ValueError):
            _mark_done(self.json_data, 0)

    def test_mark_done_side_effect_changes_in_json_data(self):
        _mark_done(self.json_data, 1)

        self.assertEqual(len(self.json_data["tasks"]), 1)
        self.assertEqual(self.json_data["curr_id"], 1)


class TestListFunction(unittest.TestCase):
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def setUp(self, _):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        _add(self.json_data, "Buy milk")
        _add(self.json_data, "Buy water")
        _mark_in_progress(self.json_data, 2)
        _add(self.json_data, "Buy bread")
        _mark_done(self.json_data, 3)
        return super().setUp()
    
    def test_list_prints_all_tasks(self):
        output = StringIO()
        with redirect_stdout(output):
            _list(self.json_data)
        output_lines = output.getvalue().splitlines()
        task_keys = ' | '.join([
            'id',
            'description'.rjust(30),
            'status'.rjust(11),
            'created'.rjust(16),
            'updated'.rjust(16)])
        seperate_line = '-' * 87
        
        self.assertEqual(output_lines[0], task_keys)
        self.assertEqual(output_lines[1], seperate_line)
        
        for i in range(3):
            task = self.json_data["tasks"][i]
            task_line = ' | '.join([
                str(task['id']).rjust(2),
                task['description'].rjust(30),
                task['status'].rjust(11),
                task['created'],
                task['updated']])
            self.assertEqual(output_lines[2 + i], task_line)
    
    def test_list_prints_todo_tasks(self):
        output = StringIO()
        with redirect_stdout(output):
            _list(self.json_data, 'todo')
        output_lines = output.getvalue().splitlines()
        task_keys = ' | '.join([
            'id',
            'description'.rjust(30),
            'status'.rjust(11),
            'created'.rjust(16),
            'updated'.rjust(16)])
        seperate_line = '-' * 87
        
        self.assertEqual(output_lines[0], task_keys)
        self.assertEqual(output_lines[1], seperate_line)
    
        task = self.json_data["tasks"][0]
        task_line = ' | '.join([
            str(task['id']).rjust(2),
            task['description'].rjust(30),
            task['status'].rjust(11),
            task['created'],
            task['updated']])
        self.assertEqual(output_lines[2], task_line)
    
    def test_list_prints_in_progress_tasks(self):
        output = StringIO()
        with redirect_stdout(output):
            _list(self.json_data, 'in-progress')
        output_lines = output.getvalue().splitlines()
        task_keys = ' | '.join([
            'id',
            'description'.rjust(30),
            'status'.rjust(11),
            'created'.rjust(16),
            'updated'.rjust(16)])
        seperate_line = '-' * 87
        
        self.assertEqual(output_lines[0], task_keys)
        self.assertEqual(output_lines[1], seperate_line)
    
        task = self.json_data["tasks"][1]
        task_line = ' | '.join([
            str(task['id']).rjust(2),
            task['description'].rjust(30),
            task['status'].rjust(11),
            task['created'],
            task['updated']])
        self.assertEqual(output_lines[2], task_line)
    
    def test_list_prints_done_tasks(self):
        output = StringIO()
        with redirect_stdout(output):
            _list(self.json_data, 'done')
        output_lines = output.getvalue().splitlines()
        task_keys = ' | '.join([
            'id',
            'description'.rjust(30),
            'status'.rjust(11),
            'created'.rjust(16),
            'updated'.rjust(16)])
        seperate_line = '-' * 87
        
        self.assertEqual(output_lines[0], task_keys)
        self.assertEqual(output_lines[1], seperate_line)
    
        task = self.json_data["tasks"][2]
        task_line = ' | '.join([
            str(task['id']).rjust(2),
            task['description'].rjust(30),
            task['status'].rjust(11),
            task['created'],
            task['updated']])
        self.assertEqual(output_lines[2], task_line)

    def test_list_raises_value_type_index_error(self):
        with self.assertRaises(TypeError):
            _list(self.json_data, 'done', 1)
        with self.assertRaises(ValueError):
            _list(self.json_data, 0)
        with self.assertRaises(ValueError):
            _list(self.json_data, '')
        with self.assertRaises(ValueError):
            _list(self.json_data, "Buy water")


if __name__ == "__main__":
    unittest.main()
