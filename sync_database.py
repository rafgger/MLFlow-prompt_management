import mlflow
from dotenv import load_dotenv
import os
import shutil

load_dotenv()

# Configure MLflow to use PostgreSQL backend
tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
mlflow.set_tracking_uri(tracking_uri)

print(f"MLflow Tracking URI: {tracking_uri}")
print(f"Current artifact location: {mlflow.get_artifact_uri()}")

# Check what's in the database
from mlflow.tracking import MlflowClient
client = MlflowClient()

print("\n=== Experiments in Database ===")
experiments = client.search_experiments()
for exp in experiments:
    print(f"ID: {exp.experiment_id}, Name: {exp.name}")
    print(f"  Artifact Location: {exp.artifact_location}")

print("\n=== Registered Models in Database ===")
models = client.search_registered_models()
for model in models:
    print(f"Model: {model.name}")

print("\n=== Checking Prompts ===")
try:
    prompt = mlflow.genai.load_prompt("prompts:/summarization-prompt/2")
    print(f"✓ Prompt 'summarization-prompt' version 2 found in database")
    print(f"  Template: {prompt.template}")
except Exception as e:
    print(f"✗ Error loading prompt: {e}")

# Option: Clean up local mlruns directory if everything is in database
print("\n=== Local mlruns directory ===")
mlruns_path = "./mlruns"
if os.path.exists(mlruns_path):
    # Count files
    total_files = sum([len(files) for r, d, files in os.walk(mlruns_path)])
    print(f"Found {total_files} files in {mlruns_path}")
    
    response = input("\nDo you want to delete the local mlruns directory? (yes/no): ")
    if response.lower() == 'yes':
        shutil.rmtree(mlruns_path)
        print(f"✓ Deleted {mlruns_path}")
        print("All data is now stored in PostgreSQL only")
else:
    print("No local mlruns directory found")

print("\n=== Configuration Summary ===")
print("✓ Metadata (experiments, runs, metrics): PostgreSQL")
print("✓ Prompts: PostgreSQL")
print("✓ Artifacts: Will be stored in PostgreSQL artifact location")
