"Central configuration"
import os

FLASK_SECRET = "something-random"
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:5001")

# test if kubernetes discovery environment variables are present
# https://kubernetes.io/docs/concepts/services-networking/service/#environment-variables
if "DIRECTORY_SERVICE_SERVICE_HOST" in os.environ and "DIRECTORY_SERVICE_SERVICE_PORT" in os.environ:
    host = os.environ["DIRECTORY_SERVICE_SERVICE_HOST"]
    port = os.environ["DIRECTORY_SERVICE_SERVICE_PORT"]
    API_ENDPOINT =  f"http://{host}:{port}"
    print(f"Kubernetes API_ENDPOINT = {API_ENDPOINT}")
