"""The extensions module is responsible for creating objects for Flask extensions."""

from flask_cors import CORS

from app.connector import MLFlowConnector
from app.inference import InferenceManager

cors = CORS()
connector = MLFlowConnector()
inference_manager = InferenceManager()
