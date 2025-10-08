from LLMReasoner import LLMReasoner
from GitHubManager import GitHubManager
import os

from agents.code_gen_agent import CodeGenerationAgent

def save_output(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(content, (dict, list)):
            import json
            json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            f.write(str(content))

def main():
    project_name = 'python_notes_App_5_Features_openAi_o3_mini'
    base_dir = os.path.join('projects', project_name)
    inputs_dir = os.path.join(base_dir, 'inputs')
    outputs_dir = os.path.join(base_dir, 'outputs_single')

    llm_reasoner = LLMReasoner()
    github_manager = GitHubManager(os.getenv('GITHUB_TOKEN'), 'LLM_Software_Company')

    code_gen_agent = CodeGenerationAgent(llm_reasoner, github_manager)
    goals_path = os.path.join(inputs_dir, 'goals.txt')
    environment_path = os.path.join(inputs_dir, 'environment.txt')

    codebase = code_gen_agent.generate_codebase(goals_path, environment_path, outputs_dir, inputs_dir)
    save_output(os.path.join(outputs_dir, 'generated_codebase.txt'), codebase)

if __name__ == "__main__":
    main()