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

def main():
    # Define project structure
    project_name = 'python_budget_planner_openAi_o3_mini'
    base_dir = os.path.join('projects', project_name)
    inputs_dir = os.path.join(base_dir, 'inputs')
    outputs_dir = os.path.join(base_dir, 'outputs')

    # Initialize components
    llm_reasoner = LLMReasoner()
    # Initialize GitHub manager with a personal access token and repository name
    # These are from the newly created GitHub repository that will be used to store the generated code
    github_manager = GitHubManager(os.getenv('GITHUB_TOKEN'), 'LLM_Software_Company')

    # Agent Pipeline
    goal_agent = GoalAnalysisAgent(llm_reasoner, github_manager)
    refined_goals = goal_agent.process_goals('inputs/goals.txt')
    #print("Refined Goals:", refined_goals)
    save_output('outputs/refined_goals.txt', refined_goals)

    env_agent = EnvironmentAnalysisAgent(llm_reasoner, github_manager)
    env_profile = env_agent.analyze_environment('inputs/environment.txt')
    #print("Environment Profile:", env_profile)
    save_output('outputs/refined_environment.txt', env_profile)

    # Generate System Specifications
    spec_gen_agent = SpecificationGenerationAgent(llm_reasoner, github_manager)
    specifications = spec_gen_agent.generate_specifications('outputs/refined_goals.txt',
                                                            'outputs/refined_environment.txt')
    #print("System Specifications:", specifications)
    save_output('outputs/system_specifications.txt', specifications)

    # Design System Architecture
    arch_design_agent = ArchitectureDesignAgent(llm_reasoner, github_manager)
    architecture_design = arch_design_agent.design_architecture('outputs/system_specifications.txt')
    #print("System Architecture Design:", architecture_design)
    save_output('outputs/system_architecture.txt', architecture_design)

    # Generate Codebase
    code_gen_agent = CodeGenerationAgent(llm_reasoner, github_manager)
    codebase = code_gen_agent.generate_codebase('outputs/system_architecture.txt', 'outputs/system_specifications.txt')
    #print("Generated Codebase:", codebase)
    save_output('outputs/generated_codebase.txt', codebase)

if __name__ == "__main__":
    main()