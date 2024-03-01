from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.db_interactor import DB

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = DB("main.db")
    yield db


@app.get("/")
def get_stories(db=Depends(get_db)):
    return db.get_stories()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}


@app.post("/")
def add_new_story(story: dict, db=Depends(get_db)):
    db.add_story(story)
    return {"message": "Story added successfully!"}
