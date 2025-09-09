import json


class GoalAnalysisAgent:
    def __init__(self, llm_reasoner, github_manager):
        self.llm = llm_reasoner
        self.github = github_manager
    
    def process_goals(self, goals_file):
        # Read file locally
        with open(goals_file, 'r', encoding='utf-8') as f:
            goals_content = f.read()

        prompt = f"You are a requirements engineer. These are goals of a future software, analyze and refine them: {goals_content}"

        refined_goals = self.llm.get_chat_response(prompt)

        """
        goals_content = self.github.read_file(goals_file)
        prompt = f"You are a requirements engineer. These are goals of a future software, analyze and refine them: {goals_content}"
        
        refined_goals = self.llm.get_chat_response(prompt)
        
        # Save refined goals
        file_path = 'outputs/refined_goals.txt'
        commit_message = "Refined Goals"
        
        try:
            # Check if the file exists
            existing_file = self.github.get_contents(file_path)
            self.github.update_file(file_path, commit_message, refined_goals, existing_file.sha)
        except self.github.GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                self.github.create_file(file_path, commit_message, refined_goals)
            else:
                raise e
        """
        
        return refined_goals