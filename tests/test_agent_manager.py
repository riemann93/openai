import os
import shutil
import unittest
import json
import tempfile

from src.file_manager import FileManager
from src.agent_manager import AgentManager
from unittest.mock import patch


class AgentManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.fm = FileManager(base_directory=self.temp_dir)
        self.am = AgentManager(self.fm)

        # Setup mock task and prompt directories
        os.makedirs(os.path.join(self.temp_dir, 'Tasks'))
        os.makedirs(os.path.join(self.temp_dir, 'Prompts'))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_load_task(self):
        mock_task = {"id": "123", "content": "Test task"}
        task_path = os.path.join(self.temp_dir, "Tasks", "123.json")
        with open(task_path, 'w') as f:
            json.dump(mock_task, f)

        task = self.am.load_task("123")
        self.assertEqual(task, mock_task)

    def test_save_task(self):
        mock_task = {"id": "123", "content": "Test task"}
        self.am.save_task(mock_task)
        with open(os.path.join(self.temp_dir, "Tasks", "123.json"), 'r') as f:
            saved_task = json.load(f)
        self.assertEqual(saved_task, mock_task)

    # ... Continue with other methods: append_as_sub_task, mark_task_resolved, etc.

    def test_load_prompt(self):
        mock_prompt = "Hello, OpenAI!"
        with open(os.path.join(self.temp_dir, "Prompts", "Resolver.txt"), 'w') as f:
            f.write(mock_prompt)

        loaded_prompt = self.am.load_prompt("Resolver")
        self.assertEqual(loaded_prompt, mock_prompt)

    def test_save_prompt(self):
        mock_prompt = "Hello, OpenAI!"
        self.am.save_prompt("Resolver", mock_prompt)

        # print out the contents of the directory
        print(os.listdir(os.path.join(self.temp_dir, "Prompts")))

        with open(os.path.join(self.temp_dir, "Prompts", "Resolver.txt"), 'r') as f:
            saved_prompt = f.read()
        self.assertEqual(saved_prompt, mock_prompt)

    @patch('src.agent_manager.OpenAIChatbot')
    def test_generate_agent(self, MockOpenAIChatbot):
        MockOpenAIChatbot.return_value = MockOpenAIChatbot()  # Mock it to return its instance.

        agent = self.am.generate_agent("Resolver")
        self.assertEqual(type(agent), type(MockOpenAIChatbot.return_value))


if __name__ == '__main__':
    unittest.main()
