import os
from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import requests
import sqlite3
from huggingface_hub import HfApi
from datasets import list_datasets, load_datasets
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
API_TOKEN = os.environ.get("API_TOKEN")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")
BASE_URL = os.environ.get("BASE_URL")


# FastAPI app
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming React is running on port 3000
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SQLite connection setup
def get_db():
    conn = sqlite3.connect('users.db')
    try:
        yield conn
    finally:
        conn.close()

# OAuth2PasswordBearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(BaseModel):
    email: str

# User registration
@app.post("/register/", response_model=User)
def register_user(email: str, password: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    hashed_password = pwd_context.hash(password)
    try:
        cursor.execute('''
            INSERT INTO users (email, hashed_password) VALUES (?, ?)
        ''', (email, hashed_password))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already registered")
    return User(email=email)

# User login
@app.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: sqlite3.Connection = Depends(get_db)):
    email = form_data.username
    password = form_data.password
    cursor = db.cursor()
    cursor.execute('''
        SELECT email, hashed_password FROM users WHERE email=?
    ''', (email,))
    user = cursor.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email")
    db_email, hashed_password = user
    if not pwd_context.verify(password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    return {"access_token": email, "token_type": "bearer"}

# Protected route example
@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    # You can fetch user data from the database if needed
    return {"message": "This is a protected route"}


@app.get("/dataset-not-valid/")
def dataset_not_valid(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/is-valid?dataset=allenai/WildChat-nontoxic"
        response = requests.get(API_URL, headers=headers)
        return response.json()

@app.get("/dataset-valid/")
def dataset_valid(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/is-valid?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()

@app.get("/splits/")
def dataset_split(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/splits?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()

@app.get("/first-row/")
def dataset_first_row(token: str = 'mm12705@gmail.com'):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/first-rows?dataset=rotten_tomatoes&config=default&split=train"
        response = requests.get(API_URL)
        return response.json()

@app.get("/dataset-slice/")
def dataset_slice(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/rows?dataset=rotten_tomatoes&config=default&split=train&offset=150&length=10"
        response = requests.get(API_URL)
        return response.json()

@app.get("/dataset-search/")
def dataset_search(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/search?dataset=rotten_tomatoes&config=default&split=train&query=cat"
        response = requests.get(API_URL)
        return response.json()

@app.get("/dataset-size/")
def dataset_size(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/size?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()

@app.get("/parguet-files/")
def parguet_files(token: str = Depends(oauth2_scheme)):
        headers = {"Authorization": f"Bearer {API_TOKEN}"}
        API_URL = BASE_URL + "/parquet?dataset=rotten_tomatoes"
        response = requests.get(API_URL)
        return response.json()

@app.get("/datasets/")
def get_datasets():
    try:
        datasets_list = list_datasets()
        return {"datasets": datasets_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datasets-10/")
def get_datasets():
    try:
        datasets_list = list_datasets()[:10]
        return {"datasets": datasets_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/")
def get_models():
    try:
        api = HfApi()  # Instantiate HfApi
        ds = load_dataset('rotten_tomatoes', split='train')  # Fetch list of datasets
        return ds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/datasets-filter/")
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
