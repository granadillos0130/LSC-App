from fastapi import APIRouter, HTTPException 
from typing import List

#schemas
from .schemas import (
    PredictRequest,
    PredictResponse,
    SaveExampleRequest,
    BatchItem,
    BatchResponse,
    DatasetInfoResponse
)

#servicios
from infrastructure.db import DatabaseRepository
from application.services.dataset_service import DatasetService
from application.services.training_service import TrainingService
from domain.classifier import SignClassifier

rotuer = APIRouter(prefix="/api")

#composición

repo = DatabaseRepository()
dataset_service = DatasetService(repo)
dataset_service.load()

training_service = TrainingService(dataset_service)
classifier = SignClassifier(dataset_service)