import mlflow
import inspect

print("MLflow version:", mlflow.__version__)
print("\nSignature of register_prompt:")
print(inspect.signature(mlflow.genai.register_prompt))
print("\nDocstring:")
print(mlflow.genai.register_prompt.__doc__)
