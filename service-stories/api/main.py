from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
@app.get("/")
def get_stories():
    return [
        {"title": "Post 1", "url": "", "content": "This is the content of the first post"},
        {"title": "Post 2", "url": "", "content": "This is the content of the second post"},
    ]

@app.get("/ping")
def ping():
    return {"ping": "pong!"}