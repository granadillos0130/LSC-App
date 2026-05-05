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

#composición: composition root conecta los modulos de la app

repo = DatabaseRepository()
dataset_service = DatasetService(repo)
dataset_service.load()

training_service = TrainingService(dataset_service)
classifier = SignClassifier(dataset_service)

#predict endpoint

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        letter, confidence = classifier.predict(req.l)

        return {
            "l": letter,
            "c":confidence
        }
    except Exception as e:
        raise HTTPException(500, str(e))
    
#example endpoint
@router.post("/examples")
def save_example(req: SaveExampleRequest):
    try:
        dataset_service.save_example(req.landmarks, req.letter)
        return {
            "status":"ok"
        }
    except Exception as e:
        raise HTTPException(500, str(e))

#endpoint training batch

@router.post("/training/batch", response_model=BatchResponse)
def save_batch(data: List[BatchItem]):
    try:
        batch = [item.dict() for item in data]
        training_service.save_batch(batch)
        return {
            "saved batch":len(batch)
        }
    except Exception as e:
        raise HTTPException(500, str(e))

#endpoint monitoreo/debug

@router.get("/dataset", response_model=DatasetInfoResponse)
def dataset_info():
    try:
        return{ 
            "samples":len(dataset_service.data)
        }
    except Exception as e:
        raise(500, str(e))