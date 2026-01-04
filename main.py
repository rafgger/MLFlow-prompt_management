from openai import OpenAI
import mlflow
from dotenv import load_dotenv
import os
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

# Test different versions
if __name__ == "__main__":
    # You can change this to test different versions
    PROMPT_VERSION = 3  # Change to 2, 3, etc. to test other versions
    
    # Or test multiple versions
    test_prompt_version(PROMPT_VERSION)
    
    # Uncomment to compare multiple versions:
    # for version in [1, 2]:
    #     test_prompt_version(version)