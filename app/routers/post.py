from fastapi import FastAPI, Body,  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""Select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("insert into posts (title, content, published) values (%s, %s, %s) returning *", (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.dict(), owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Previous psycopg2 implementation (kept for reference):
    # cursor.execute("select * from posts where id = %s", (id,))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Post not found"}

    return post

@router.delete('/{id}', status_code = status.HTTP_200_OK)
async def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # Previous psycopg2 implementation (kept for reference):
    # cursor.execute("delete from posts where id = %s returning *", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted"}

@router.put('/{id}', status_code = status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),   current_user = Depends(oauth2.get_current_user)):
    # Previous psycopg2 implementation (kept for reference):
    # cursor.execute(
    #     'update posts set title = %s, content = %s, published = %s where id = %s returning *',
    #     (post.title, post.content, post.published, id),
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_db = post_query.first()

    if not post_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )
    
    if post_db.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()