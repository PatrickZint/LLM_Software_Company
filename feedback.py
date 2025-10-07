from LLMReasoner import LLMReasoner
from GitHubManager import GitHubManager
import os

from agents.feedback_code_gen_agent import FeedbackCodeGenerationAgent

def save_output(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(content, (dict, list)):
            import json
            json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            f.write(str(content))

def create_input_file(filepath, placeholder):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(placeholder)

def main():
    # Define project structure
    project_name = 'python_notes_App_4_Features_openAi_o3_mini'
    base_dir = os.path.join('projects', project_name)
    inputs_dir = os.path.join(base_dir, 'inputs')
    outputs_dir = os.path.join(base_dir, 'outputs')

    # Initialize components
    llm_reasoner = LLMReasoner()
    # Initialize GitHub manager with a personal access token and repository name
    # These are from the newly created GitHub repository that will be used to store the generated code
    github_manager = GitHubManager(os.getenv('GITHUB_TOKEN'), 'LLM_Software_Company')

    # Generate Codebase
    code_gen_agent = FeedbackCodeGenerationAgent(llm_reasoner, github_manager)
    architecture_path = os.path.join(outputs_dir, 'refined_goals.txt')
    specifications_path = os.path.join(outputs_dir, 'refined_environment.txt')

    # Feedback-Agent: Feedback.txt wird automatisch berücksichtigt
    codebase = code_gen_agent.generate_codebase(architecture_path, specifications_path, outputs_dir, inputs_dir, use_existing_codebase=False)
    save_output(os.path.join(outputs_dir, 'generated_codebase_with_feedback.txt'), codebase)

if __name__ == "__main__":
    main()