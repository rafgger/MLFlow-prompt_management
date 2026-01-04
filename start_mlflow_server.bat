@echo off
echo Starting MLFlow Tracking Server...
echo Backend: PostgreSQL
echo Host: 127.0.0.1:5000
echo.

mlflow server --backend-store-uri postgresql://postgres:123456@localhost:5432/mlflow_db --host 127.0.0.1 --port 5000
