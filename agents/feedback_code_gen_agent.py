import json
import os
import zipfile


class FeedbackCodeGenerationAgent:
    def __init__(self, llm_reasoner, github_manager):
        self.llm = llm_reasoner
        self.github = github_manager

    def generate_codebase(self, architecture_file, specifications_file, outputs_dir, inputs_dir, use_existing_codebase):
        # Read file locally
        with open(architecture_file, 'r', encoding='utf-8') as f:
            architecture = f.read()
        with open(specifications_file, 'r', encoding='utf-8') as f:
            specifications = f.read()

        # Read feedback
        feedback_path = os.path.join(inputs_dir, 'Feedback.txt')
        feedback = None
        if os.path.exists(feedback_path):
            with open(feedback_path, 'r', encoding='utf-8') as f:
                feedback = f.read()
        else:
            feedback = ""

        # Read Codebase
        existing_codebase = None
        if use_existing_codebase:
            codebase_path = os.path.join(outputs_dir, 'generated_codebase.txt')
            if os.path.exists(codebase_path):
                with open(codebase_path, 'r', encoding='utf-8') as f:
                    existing_codebase = f.read()

        # Generate codebase
        prompt = (
            f"You are a software engineer. Based on the following system architecture, specifications, feedback "
            f"and existing codebase, regenerate all required Python-Files or modify them to implement the feedback. "
            f"Respond in JSON format with this structure:.\n\n"
            f"{{\n"
            f"  \"files\": [\n"
            f"    {{\n"
            f"      \"filename\": \"<filename>\",\n"
            f"      \"content\": \"<file-content>\"\n"
            f"    }},\n"
            f"    ...\n"
            f"  ]\n"
            f"}}\n\n"
            f"System Architecture:\n{architecture}\n\n"
            f"System Specifications:\n{specifications}"
        )
        if feedback:
            prompt += f"\nFeedback from previous run:\n{feedback}\n"
        if existing_codebase:
            prompt += f"\nCurrent Codebase:\n{existing_codebase}\n"

        codebase = self.llm.get_chat_response(prompt)

        print(codebase)

        # Save codebase
        txt_path = os.path.join(outputs_dir, 'generated_codebase.txt')

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(codebase)

        file_path = os.path.join(outputs_dir, 'generated_codebase.zip')

        codebase = save_codebase_as_zip(txt_path, file_path, inputs_dir)

        commit_message = "Generated Codebase"

        try:
            # Check if the file exists
            existing_file = self.github.get_contents(file_path)
            self.github.update_file(file_path, commit_message, codebase, existing_file.sha)
        except self.github.GithubException as e:
            if e.status == 404:
                # File does not exist, create it
                self.github.create_file(file_path, commit_message, codebase)
            else:
                raise e

        return codebase


def save_codebase_as_zip(codebase_json_path, zip_path, inputs_dir):
    # Lade das JSON aus der Datei
    with open(codebase_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # print(data)

    # Liste der Dateien aus dem JSON auslesen
    files = data.get("files", [])

    # ZIP-Datei erstellen
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        # Durch alle Einträge im Dictionary iterieren
        # Hier ist jeder Schlüssel ein Dateiname und jeder Wert der Dateiinhalt
        for file_info in files:
            filename = file_info.get("filename")
            content = file_info.get("content")
            if isinstance(content, list):
                content = "\n".join(content)
            zipf.writestr(filename, content)

        # Füge extra input-Dateien hinzu, falls vorhanden
        for extra_file in ["goals.txt", "environment.txt"]:
            file_path = os.path.join(inputs_dir, extra_file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as ef:
                    content = ef.read()
                    zipf.writestr(os.path.join("inputs", extra_file), content)
                # Im ZIP unter dem Ordner "inputs" ablegen

    # ZIP-Datei als Bytes zurückgeben
    with open(zip_path, 'rb') as f:
        return f.read()