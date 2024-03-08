from fastapi import Depends, HTTPException
from api.db_interactor import DB, ItemNotFound
from api.story import StoryModel, CommentModel
from api import app


def get_db():
    db = DB("main.db")
    if not db._table_exists("stories"):
        db._create_table(
            """CREATE TABLE IF NOT EXISTS `stories`(
                    `id` integer PRIMARY KEY,
                    `title` text NOT NULL,
                    `content` text,
                    `url` text,
                    `poster` text NOT NULL
                )"""
        )
        db._create_table(
            """CREATE TABLE IF NOT EXISTS `comments`(
                                `id` integer PRIMARY KEY,
                                `story` integer NOT NULL,
                                `content` text,
                                `parent` integer,
                                `poster` text NOT NULL
                            )"""
        )
    yield db


@app.get("/")
def get_stories(db=Depends(get_db)):
    return db.get_stories()


@app.get("/ping")
def ping():
    return {"ping": "pong!"}


@app.post("/")
def add_new_story(story: StoryModel, db=Depends(get_db)):
    db.add_story(story.model_dump())
    return {"message": "Story added successfully!"}


@app.get("/{story_id}")
def get_story(story_id: int, db=Depends(get_db)):
    try:
        return db.get_story(story_id)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Story not found")

@app.post("/{story_id}/comments")
def add_new_comment(story_id: int, comment: CommentModel, db=Depends(get_db)):
    try:
        db.get_story(story_id)
        db.add_comment(story_id, comment.model_dump())
        return {"message": "Comment added successfully!"}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Story not found")

@app.get("/{story_id}/comments")
def get_comments(story_id: int, db=Depends(get_db)):
    try:
        return db.get_comments(story_id)
    except ItemNotFound:
        raise HTTPException(status_code=404, detail="Story not found")