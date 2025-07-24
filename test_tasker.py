import unittest
from unittest.mock import patch
from tasker import _add, TaskData


class TestAddFunction(unittest.TestCase):
    
    def setUp(self):
        self.json_data: TaskData = {"tasks": [], "curr_id": 0}
        return super().setUp()

    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_for_adding_correct_task(self, mocked_time):
        _add(self.json_data, "Buy milk")
        task = self.json_data["tasks"][0]
        
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Buy milk")
        self.assertEqual(task["status"], "todo")
        self.assertEqual(task["created"], "01.01.2025 12:00")
        self.assertEqual(task["updated"], "01.01.2025 12:00")
    
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_raises_value_type_error(self, mocked_time):
        _add(self.json_data, "Buy milk")
        
        with self.assertRaises(ValueError):
            _add(self.json_data, "to ")
        with self.assertRaises(ValueError):
            _add(self.json_data, "")
        with self.assertRaises(TypeError):
            _add(self.json_data)
        with self.assertRaises(TypeError):
            _add(self.json_data, "buy groceries", 1)
            
    @patch('tasker._now_datetime', return_value="01.01.2025 12:00")
    def test_add_side_effect_changes_in_json_data(self, mocked_time):
        _add(self.json_data, "Buy milk")
        
        self.assertEqual(len(self.json_data["tasks"]), 1)
        self.assertEqual(self.json_data["curr_id"], 1)


if __name__ == "__main__":
    unittest.main()
