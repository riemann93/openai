import os
import json
from src.services.chatgpt.chatgpt_service import OpenAIChatbot


class AgentManager:

    def __init__(self, file_manager):
        self.file_manager = file_manager
        self.agents = {}

    # Task Management
    def _get_task_path(self, task_id, parent_id=None):
        """Helper function to get the correct path based on parent_id."""
        if parent_id:
            return os.path.join("Tasks", parent_id, f"{task_id}.json")
        return os.path.join("Tasks", f"{task_id}.json")

    def load_task(self, task_id, parent_id=None):
        task_path = self._get_task_path(task_id, parent_id)
        try:
            task_content = self.file_manager.read_file(task_path)
            return json.loads(task_content)
        except Exception as e:
            raise ValueError(f"Error loading task: {e}")

    def save_task(self, task):
        """Saves a task. If the task has a parent_id, it will be saved in a subdirectory named after the parent_id."""
        try:
            task_content = json.dumps(task)
            task_path = self._get_task_path(task['id'], task.get('parent_id'))

            # Ensure directory exists
            dir_name = os.path.dirname(task_path)
            if not os.path.exists(dir_name):
                self.file_manager.create_directory(dir_name)

            self.file_manager.write_file(task_path, task_content)
        except Exception as e:
            raise ValueError(f"Error saving task: {e}")

    def append_as_sub_task(self, parent_task_id, sub_task):
        """Appends a task as a sub-task to another task."""
        sub_task["parent_id"] = parent_task_id
        self.save_task(sub_task)

    def mark_task_resolved(self, task_id, parent_id=None):
        task_path = self._get_task_path(task_id, parent_id)
        try:
            self.file_manager.move_file(task_path, os.path.join("Tasks", "Resolved", f"{task_id}.json"))
        except Exception as e:
            raise ValueError(f"Error marking task as resolved: {e}")

    # Prompt Management
    def load_prompt(self, agent_type, context=None):
        try:
            prompt_content = self.file_manager.read_file(f"Prompts/{agent_type}.txt")
            return prompt_content
        except Exception as e:
            raise ValueError(f"Error loading prompt: {e}")

    def save_prompt(self, agent_type, prompt_content):
        try:
            self.file_manager.write_file(f"Prompts/{agent_type}.txt", prompt_content)
        except Exception as e:
            raise ValueError(f"Error saving prompt: {e}")

    # Agent Generation
    def generate_agent(self, agent_type):
        agent = OpenAIChatbot()
        self.agents[agent_type] = agent
        return agent

    # ChatGPT Interfacing

    # Miscellaneous
    def list_all_tasks(self):
        return self.file_manager.list_directory_contents("Tasks")

    def list_resolved_tasks(self):
        return self.file_manager.list_directory_contents("Tasks/Resolved")

# Usage:
# am = AgentManager()
# agent = am.generate_agent("Resolver")
# response = am.send_prompt_to_agent(agent, "Hello, how are you?")
# print(response)
