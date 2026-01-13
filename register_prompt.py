import mlflow
from dotenv import load_dotenv
import os

load_dotenv()

# Configure MLflow to use PostgreSQL backend
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Create and register multiple versions of the summarization prompt
# Note: MLflow uses double curly braces {{variable}} for template variables

prompt_name = "summarization-prompt"

# Version 1: Basic summarization
prompt_template_v1 = "Summarize the following text in {{num_sentences}} sentence(s): {{sentences}}"

# Version 2: More detailed instructions
prompt_template_v2 = "Create a concise summary of {{num_sentences}} sentence(s) from the text below. Focus on the main ideas and key points:\n\n{{sentences}}"

# Version 3: With constraints
prompt_template_v3 = "Summarize the following text in exactly {{num_sentences}} sentence(s). Ensure clarity and maintain all key concepts:\n\n{{sentences}}"

versions = [
    (1, prompt_template_v1, "Initial version of summarization prompt"),
    (2, prompt_template_v2, "Enhanced version with better instructions"),
    (3, prompt_template_v3, "Version with strict sentence count requirement"),
]

print("\n" + "="*60)
print("Registering Summarization Prompt Versions")
print("="*60)

for version_num, template, message in versions:
    try:
        if version_num == 1:
            # First version: use register_prompt
            result = mlflow.genai.register_prompt(
                name=prompt_name,
                template=template,
                commit_message=message
            )
        else:
            # Subsequent versions: use update_prompt
            result = mlflow.genai.update_prompt(
                name=prompt_name,
                template=template,
                commit_message=message
            )
        
        print(f"\n✓ Version {result.version} registered successfully!")
        print(f"  Name: {result.name}")
        print(f"  Load with: prompts:/{prompt_name}/{result.version}")
    except Exception as e:
        print(f"\n✗ Error registering version {version_num}: {e}")

print("\n" + "="*60)
print("All versions registered! You can now test them in main.py")
print("="*60)
