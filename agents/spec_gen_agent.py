class SpecificationGenerationAgent:
    def __init__(self, llm_reasoner, github_manager):
        self.llm = llm_reasoner
        self.github = github_manager

    def generate_specifications(self, goals_file, env_file):
        # Read file locally
        with open(goals_file, 'r', encoding='utf-8') as f:
            refined_goals = f.read()
        with open(env_file, 'r', encoding='utf-8') as f:
            env_profile = f.read()

        prompt = (
            f"You are a software engineer. Based on the following refined goals and environment profile, "
            f"generate detailed system specifications including functional requirements, non-functional requirements, "
            f"and system design recommendations.\n\n"
            f"Refined Goals:\n{refined_goals}\n\n"
            f"Environment Profile:\n{env_profile}"
        )

        specifications = self.llm.get_chat_response(prompt)

        """
        # Read refined goals and environment profile from GitHub
        refined_goals = self.github.read_file(goals_file)
        env_profile = self.github.read_file(env_file)

        # Generate specifications
        prompt = (
            f"You are a software engineer. Based on the following refined goals and environment profile, "
            f"generate detailed system specifications including functional requirements, non-functional requirements, "
            f"and system design recommendations.\n\n"
            f"Refined Goals:\n{refined_goals}\n\n"
            f"Environment Profile:\n{env_profile}"
        )
        specifications = self.llm.get_chat_response(prompt)

        # Save specifications
        file_path = 'outputs/system_specifications.txt'
        commit_message = "Generated System Specifications"
        
        try:
            # Check if the file exists
            existing_file = self.github.get_contents(file_path)
            self.github.update_file(file_path, commit_message, specifications, existing_file.sha)
        except self.github.GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                self.github.create_file(file_path, commit_message, specifications)
            else:
                raise e
        """
        return specifications