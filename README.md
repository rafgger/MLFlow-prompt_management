# MLflow Template with PostgreSQL

A Python project that integrates MLflow with PostgreSQL backend for experiment tracking and uses OpenAI's GPT models for text summarization.

Experiment with 2 prompts.

<a href="https://youtu.be/DkegCtqncd4" target="_blank">
  <img src="https://github.com/user-attachments/assets/bb3f1ec3-0442-432d-8321-02e7726e3a89" alt="MLFlow video example" width="500"/>
</a>




## Features

- MLflow tracking with PostgreSQL backend
- OpenAI GPT-4o-mini integration
- Text summarization capabilities
- PostgreSQL database connection utilities

## Prerequisites

- Python 3.11 or 3.12 (recommended for Windows compatibility)
- PostgreSQL 17.6+
- OpenAI API key

**Note:** Python 3.13 has known compatibility issues with MLflow UI on Windows. Use Python 3.11 or 3.12 for best results.

## Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
```bash
psql -U postgres -c "CREATE DATABASE mlflow_db;"
```

5. Initialize MLflow tables:
```bash
mlflow db upgrade postgresql://postgres:your_password@localhost:5432/mlflow_db
```

6. Configure environment variables in `.env`:
```
OPENAI_API_KEY=your-actual-openai-api-key

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=mlflow_db

# MLflow Tracking URI - point to MLflow server (not directly to PostgreSQL)
MLFLOW_TRACKING_URI=http://127.0.0.1:5000
```

## Usage

### 1. Start the MLflow Tracking Server

Run the MLflow server with PostgreSQL backend:
```bash
start_mlflow_server.bat
```

Or manually:
```bash
mlflow server --backend-store-uri postgresql://postgres:your_password@localhost:5432/mlflow_db --host 127.0.0.1 --port 5000
```

The server will:
- Store **metadata** (runs, parameters, metrics) in PostgreSQL
- Store **artifacts** (mo      # Main application script
├── register_prompt.py         # Register prompts to MLflow
├── sync_database.py           # Sync and verify database
├── cleanup_model.py           # Clean up models
├── start_mlflow_server.bat    # Start MLflow tracking server
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
├── mlartifacts/               # Local artifact storage
└── README.md       
In a separate terminal:
```bash
python main.py
```

The script will:
- Connect to the MLflow tracking server
- Use OpenAI's GPT-4o-mini to summarize text
- Track experiments with metadata in PostgreSQL and artifacts locally

## Project Structure

```
.
├── main.py              # Main application script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Database Connection

The project includes a `get_postgres_connection()` function in `main.py` for direct PostgreSQL access:

```python
conn = get_postgres_connection()
# Use connection for custom queries
```

## Dependencies

- mlflow - Experiment tracking and model registry
- openai - Tracking Server Architecture

This project uses the MLflow Tracking Server architecture as described in the [official documentation](https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/):

- **Backend Store**: PostgreSQL database stores all metadata (experiments, runs, parameters, metrics)
- **Artifact Store**: Local filesystem (`./mlartifacts`) stores artifacts (models, files, plots)
- **Tracking Server**: HTTP server that proxies requests between clients and storage

To access the MLflow UI, simply navigate to http://127.0.0.1:5000 after starting the server.

**Note:** If you encounter `OSError: [WinError 10022]`, use Python 3.11 or 3.12 instead of 3.13 (known compatibility issue with uvicorn on Windows).tions:**
1. Use Python 3.11 or 3.12 instead of 3.13
2. Or run MLflow UI with the `--host` flag:
   ```bash
   mlflow ui --backend-store-uri postgresql://postgres:password@localhost:5432/mlflow_db --host 127.0.0.1
   ```

## Creating prompt versions

After `mlflow ui`, you go in the UI into Prompts -> Create Prompt. Then you create a second version of it, using the right-upper corner (Create version) in the given prompt.

### PostgreSQL Connection Issues

If you get authentication errors:
- Verify your password in `.env` matches your PostgreSQL password
- Ensure PostgreSQL service is running
- Check that the database `mlflow_db` exists

### Sources
https://mlflow.org/docs/3.4.0/ml/tracking/quickstart/notebooks/tracking_quickstart/

https://mlflow.org/docs/3.4.0/ml/tracking/



## License

MIT
