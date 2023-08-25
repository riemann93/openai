# Assuming the necessary modules are in the same directory.
from agent_manager import AgentManager
from file_manager import FileManager  # if needed directly in the main

# Initialize the FileManager and AgentManager
file_manager = FileManager()
agent_manager = AgentManager(file_manager)


def main():
    # Define a main goal
    main_goal = {
        "id": "T1000",
        "description": "Develop a basic e-commerce website"
    }

    # Save the main goal using AgentManager
    agent_manager.save_task(main_goal)

    # Use the Decomposer agent to break down the main goal into sub-goals
    decomposer_agent = agent_manager.generate_agent("Decomposer")

    decomposer_response = decomposer_agent.get_response_from_chatbot(text_prompt=main_goal["description"])

    # Assuming the decomposer returns a list of sub-goals, we can save these with a reference back to the main task.
    sub_goals = decomposer_response['sub_tasks']

    for sub_goal in sub_goals:
        sub_goal['parent_task_id'] = main_goal['task_id']
        agent_manager.save_task(sub_goal)

    print("Main goal has been decomposed into sub-goals and saved successfully!")


if __name__ == "__main__":
    main()
