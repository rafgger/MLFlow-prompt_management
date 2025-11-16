import mlflow
from dotenv import load_dotenv
import os

load_dotenv()

# Configure MLflow to use PostgreSQL backend
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Create and register the summarization prompt
# Note: MLflow uses double curly braces {{variable}} for template variables
prompt_template = "Summarize the following text in {{num_sentences}} sentence(s): {{sentences}}"

# Register the prompt using the genai module
result = mlflow.genai.register_prompt(
    name="summarization-prompt",
    template=prompt_template,
    commit_message="Initial version of summarization prompt"
)

print(f"\nPrompt registered successfully!")
print(f"Name: {result.name}")
print(f"Version: {result.version}")
print(f"Load with: prompts:/summarization-prompt/{result.version}")
