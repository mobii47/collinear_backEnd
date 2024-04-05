import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import engine
from routers import users, datasets

load_dotenv()
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Assuming React is running on port 3000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Included routers
app.include_router(users.router, prefix="/user")
app.include_router(datasets.router, prefix="/dataset")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
