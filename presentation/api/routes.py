from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from typing import List
import io
import os
import subprocess
import tempfile
import traceback
import numpy as np
import speech_recognition as sr

#schemas
from .schemas import (
    PredictRequest,
    PredictResponse,
    SaveExampleRequest,
    BatchItem,
    BatchResponse,
    DatasetInfoResponse,
    LandmarksResponse,
    STTResponse,
)

#servicios
from infrastructure.db.dataset_repo import DatabaseRepository
from application.services.dataset_service import DatasetService
from application.services.training_service import TrainingService
from domain.classifier import SignClassifier

router = APIRouter(prefix="/api")

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
        dataset_service.save_example(req.landmrks, req.letter)
        return {
            "status":"ok"
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, str(e))

#endpoint training batch

@router.post("/training/batch", response_model=BatchResponse)
def save_batch(data: List[BatchItem]):
    try:
        batch = [item.dict() for item in data]
        training_service.save_batch(batch)
        return {
            "saved":len(batch)
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

#letras disponibles en memoria

@router.get("/landmarks")
def list_landmarks():
    available = sorted(set(dataset_service.letters))
    return {"letters": available, "total": len(dataset_service.data)}

#landmarks promedio por letra (usado por el frontend Voice → Seña)

@router.get("/landmarks/{letter}", response_model=LandmarksResponse)
def get_landmarks(letter: str):
    key = letter.upper()
    samples = [
        dataset_service.data[i]
        for i, lbl in enumerate(dataset_service.letters)
        if lbl == key
    ]
    if not samples:
        raise HTTPException(status_code=404, detail=f"No hay ejemplos para la letra '{key}'")
    avg = np.mean(samples, axis=0).tolist()
    return {"letter": key, "landmarks": avg}

#transcripción de voz (Speech-To-Text)

@router.post("/stt")
async def speech_to_text(request: Request):
    body = await request.body()
    print("llego, bytes:", len(body))
    return {"text": "test"}