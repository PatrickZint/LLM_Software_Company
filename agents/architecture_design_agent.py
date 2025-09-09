class ArchitectureDesignAgent:
    def __init__(self, llm_reasoner, github_manager):
        self.llm = llm_reasoner
        self.github = github_manager

    def design_architecture(self, specifications_file):
        # Read file locally
        with open(specifications_file, 'r', encoding='utf-8') as f:
            specifications = f.read()

        prompt = (
            f"You are a system architect. Based on the following system specifications, "
            f"create a high-level system architecture including component design and technology stack selection.\n\n"
            f"System Specifications:\n{specifications}"
        )

        architecture_design = self.llm.get_chat_response(prompt)

        """
        # Read system specifications from GitHub
        specifications = self.github.read_file(specifications_file)

        # Generate architecture design
        prompt = (
            f"You are a system architect. Based on the following system specifications, "
            f"create a high-level system architecture including component design and technology stack selection.\n\n"
            f"System Specifications:\n{specifications}"
        )
        architecture_design = self.llm.get_chat_response(prompt)

        # Save architecture design
        file_path = 'outputs/system_architecture.txt'
        commit_message = "Generated System Architecture"
        
        try:
            # Check if the file exists
            existing_file = self.github.get_contents(file_path)
            self.github.update_file(file_path, commit_message, architecture_design, existing_file.sha)
        except self.github.GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                self.github.create_file(file_path, commit_message, architecture_design)
            else:
                raise e
        """

        return architecture_design