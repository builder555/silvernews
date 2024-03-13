from fastapi import Depends, HTTPException
from api.db_interactor import DB, StoryNotFound, CommentNotFound
from api.story import StoryModel, CommentModel
from api import app


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
def add_new_story(story: StoryModel, db=Depends(get_db)):
    db.add_story(story.model_dump())
    return {"message": "Story added successfully!"}


@app.get("/{story_id}")
def get_story(story_id: int, db=Depends(get_db)):
    try:
        return db.get_story(story_id)
    except StoryNotFound:
        raise HTTPException(status_code=404, detail="Story not found")


@app.post("/{story_id}/comments")
def add_new_comment_to_story(story_id: int, comment: CommentModel, db=Depends(get_db)):
    try:
        db.get_story(story_id)
        db.add_comment(story_id, comment.model_dump())
        return {"message": "Comment added successfully!"}
    except StoryNotFound:
        raise HTTPException(status_code=404, detail="Story not found")


@app.post("/{story_id}/comments/{comment_id}")
def add_nested_comment(story_id: int, comment_id: int, comment: CommentModel, db=Depends(get_db)):
    try:
        db.get_comment(comment_id)
        comment.parent = comment_id
        db.add_comment(story_id, comment.model_dump())
        return {"message": "Comment added successfully!"}
    except StoryNotFound:
        raise HTTPException(status_code=404, detail="Story not found")
    except CommentNotFound:
        raise HTTPException(status_code=404, detail="Comment not found")


@app.get("/{story_id}/comments")
def get_comments(story_id: int, db=Depends(get_db)):
    try:
        return db.get_comments(story_id)
    except StoryNotFound:
        raise HTTPException(status_code=404, detail="Story not found")
