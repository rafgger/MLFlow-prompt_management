import os
import mlflow
from openai import OpenAI
from mlflow.genai import scorer
from mlflow.genai.scorers import Correctness, Guidelines
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()

# PostgreSQL connection setup
def get_postgres_connection():
    """Create and return a PostgreSQL connection"""
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

# Configure MLflow to use PostgreSQL backend
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# Enable automatic tracing for OpenAI calls
mlflow.openai.autolog()

# Set experiment
mlflow.set_experiment("summarization-tracing")

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

target_text = """
Artificial Intelligence and Data Science are transforming industries by enabling machines to learn 
from data and make intelligent decisions. Machine learning algorithms can identify patterns in vast 
datasets, while deep learning neural networks excel at complex tasks like image recognition and 
natural language processing. Data scientists use statistical methods, programming, and domain expertise 
to extract insights from structured and unstructured data. Modern AI systems leverage techniques such 
as supervised learning, unsupervised learning, and reinforcement learning to solve real-world problems 
ranging from predictive analytics to autonomous systems.
"""

# Load different versions of the prompt
def test_prompt_version(version, num_sentences=1):
    """Test a specific version of the summarization prompt"""
    print(f"\n{'='*60}")
    print(f"Testing Prompt Version {version}")
    print(f"{'='*60}")
    
    try:
        # Load the prompt from MLflow registry
        prompt = mlflow.genai.load_prompt(f"prompts:/summarization-prompt/{version}")
        print(f"✓ Loaded prompt version {version}")
        print(f"Template: {prompt.template[:100]}...")
        
        # Use the prompt with OpenAI
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt.format(num_sentences=num_sentences, sentences=target_text),
                }
            ],
            model="gpt-4o-mini",
        )
        
        result = response.choices[0].message.content
        print(f"\nResult:\n{result}")
        return result
        
    except Exception as e:
        print(f"✗ Error loading version {version}: {e}")
        return None


def test_prompt_version_with_trace(version, num_sentences=1):
    """Test a specific version of the summarization prompt with MLflow Tracing"""
    print(f"\n{'='*60}")
    print(f"Testing Prompt Version {version} WITH AUTOMATIC TRACES")
    print(f"{'='*60}")
    
    try:
        # Load the prompt from MLflow registry
        prompt = mlflow.genai.load_prompt(f"prompts:/summarization-prompt/{version}")
        print(f"✓ Loaded prompt version {version}")
        print(f"Template: {prompt.template[:100]}...")
        
        # Format and use the prompt with OpenAI
        formatted_prompt = prompt.format(num_sentences=num_sentences, sentences=target_text)
        
        # OpenAI call is automatically traced by mlflow.openai.autolog()
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": formatted_prompt,
                }
            ],
            model="gpt-4o-mini",
        )
        
        result = response.choices[0].message.content
        print(f"\nResult:\n{result}")
        print(f"\n✓ Trace logged automatically by mlflow.openai.autolog()!")
        return result
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

# Test different versions
if __name__ == "__main__":
    # You can change this to test different versions
    PROMPT_VERSION = 2  # Change to 2, 3, etc. to test other versions
    
    print("\n" + "="*60)
    print("MLflow Tracing with OpenAI Autologging")
    print("="*60)
    
    # Test with automatic tracing enabled
    test_prompt_version_with_trace(PROMPT_VERSION)
    # test_prompt_version(PROMPT_VERSION)
    
    print("\n" + "="*60)
    print("✓ Check MLflow UI at http://localhost:5000")
    print("  to view the traces!")
    print("="*60)
    
    # Uncomment to test multiple versions:
    # for version in [1, 2]:
    #     with mlflow.start_run():
    #         test_prompt_version_with_trace(version)