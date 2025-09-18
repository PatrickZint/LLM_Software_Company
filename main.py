from LLMReasoner import LLMReasoner
from GitHubManager import GitHubManager
import os

from agents.goal_analysis_agent import GoalAnalysisAgent
from agents.environment_analysis_agent import EnvironmentAnalysisAgent
from agents.spec_gen_agent import SpecificationGenerationAgent
from agents.architecture_design_agent import ArchitectureDesignAgent
from agents.code_gen_agent import CodeGenerationAgent

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
    project_name = 'python_notes_App_2_Featrues_openAi_o3_mini'
    base_dir = os.path.join('projects', project_name)
    inputs_dir = os.path.join(base_dir, 'inputs')
    outputs_dir = os.path.join(base_dir, 'outputs')

    """
    # Create directories if they don't exist
    goals_path = os.path.join(inputs_dir, 'goals.txt')
    env_path = os.path.join(inputs_dir, 'environment.txt')
    create_input_file(goals_path, f"Code a simple a lightweight news reader that fetches and displays top headlines from a public API. \n"
                                  f"The result should be a functional application with, so if necessary, create required config files. \n"
                                  f"Features: Basic UI: List of news headlines on the home screen Tappable item to view full article details. \n")
    create_input_file(env_path, "The system must be secure and provide a reasonable performance. "
                                "Technology stack: Use Python and Tkinter.")
    """

    # Initialize components
    llm_reasoner = LLMReasoner()
    # Initialize GitHub manager with a personal access token and repository name
    # These are from the newly created GitHub repository that will be used to store the generated code
    github_manager = GitHubManager(os.getenv('GITHUB_TOKEN'), 'LLM_Software_Company')

    # Agent Pipeline
    goal_agent = GoalAnalysisAgent(llm_reasoner, github_manager)
    goals_path = os.path.join(inputs_dir, 'goals.txt')
    refined_goals = goal_agent.process_goals(goals_path)
    #print("Refined Goals:", refined_goals)
    save_output(os.path.join(outputs_dir, 'refined_goals.txt'), refined_goals)

    env_agent = EnvironmentAnalysisAgent(llm_reasoner, github_manager)
    env_path = os.path.join(inputs_dir, 'environment.txt')
    env_profile = env_agent.analyze_environment(env_path)
    #print("Environment Profile:", env_profile)
    save_output(os.path.join(outputs_dir, 'refined_environment.txt'), env_profile)

    # Generate System Specifications
    spec_gen_agent = SpecificationGenerationAgent(llm_reasoner, github_manager)
    refined_goals_path = os.path.join(outputs_dir, 'refined_goals.txt')
    refined_env_path = os.path.join(outputs_dir, 'refined_environment.txt')
    specifications = spec_gen_agent.generate_specifications(refined_goals_path, refined_env_path)
    #print("System Specifications:", specifications)
    save_output(os.path.join(outputs_dir, 'system_specifications.txt'), specifications)

    # Design System Architecture
    arch_design_agent = ArchitectureDesignAgent(llm_reasoner, github_manager)
    architecture_design = arch_design_agent.design_architecture(os.path.join(outputs_dir, 'system_specifications.txt'))
    #print("System Architecture Design:", architecture_design)
    save_output(os.path.join(outputs_dir, 'system_architecture.txt'), architecture_design)

    # Generate Codebase
    code_gen_agent = CodeGenerationAgent(llm_reasoner, github_manager)
    architecture_path = os.path.join(outputs_dir, 'refined_goals.txt')
    specifications_path = os.path.join(outputs_dir, 'refined_environment.txt')
    codebase = code_gen_agent.generate_codebase(architecture_path, specifications_path, outputs_dir, inputs_dir)
    #print("Generated Codebase:", codebase)
    save_output(os.path.join(outputs_dir, 'generated_codebase.txt'), codebase)

if __name__ == "__main__":
    main()