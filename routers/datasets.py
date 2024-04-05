import os
from fastapi import APIRouter, Depends, HTTPException
import requests
from dotenv import load_dotenv
from huggingface_hub import HfApi
from datasets import list_datasets
from database import SessionLocal

router = APIRouter()

load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")
BASE_URL = os.environ.get("BASE_URL")

@router.get("/dataset-not-valid/")
def dataset_not_valid():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/is-valid?dataset=allenai/WildChat-nontoxic"
        response = requests.get(API_URL, headers=headers)
        return response.json()
    finally:
        db.close()

@router.get("/dataset-valid/")
def dataset_valid():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/is-valid?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/splits/")
def dataset_split():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/splits?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/first-row/")
def dataset_first_row():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/first-rows?dataset=rotten_tomatoes&config=default&split=train"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/dataset-slice/")
def dataset_slice():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/rows?dataset=rotten_tomatoes&config=default&split=train&offset=150&length=10"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/dataset-search/")
def dataset_search():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/search?dataset=rotten_tomatoes&config=default&split=train&query=cat"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/dataset-size/")
def dataset_size():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/size?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/parguet-files/")
def parguet_files():
    db = SessionLocal()
    try:
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/parquet?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()
    finally:
        db.close()

@router.get("/datasets/")
def get_datasets():
    try:
        datasets_list = list_datasets()
        return {"datasets": datasets_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets-10/")
def get_datasets():
    try:
        datasets_list = list_datasets()[:10]
        return {"datasets": datasets_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rotten_tomatoes_dataset/")
def get_RT_dataset():
    try:
        api = HfApi()  # Instantiate HfApi
        ds = load_dataset('rotten_tomatoes', split='train')  # Fetch list of datasets
        return ds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets-filter/")
def get_datasets_filter():
    try:
        api = HfApi()
        models = api.list_datasets(
            filter=DatasetsFilter(
            task="image-classification",
            library="pytorch",
            trained_dataset="imagenet"
        )
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
