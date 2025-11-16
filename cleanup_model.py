import mlflow
from dotenv import load_dotenv
import os

load_dotenv()

# Configure MLflow to use PostgreSQL backend
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

client = mlflow.MlflowClient()

# Delete the existing model
try:
    client.delete_registered_model("summarization-prompt")
    print("Deleted existing model 'summarization-prompt'")
except Exception as e:
    print(f"Error deleting model: {e}")
