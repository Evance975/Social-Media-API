from app import oauth2
from .. import models, schemas, oauth2
from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts", #to avoid repetition of codes
    tags=['Posts']
)

# function for getting all the post from the db
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int=Depends(oauth2.get_current_user)):
    #cursor.execute(""" SELECT * FROM posts""")
    #to run the SQL querry
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


#code for creating a brand new post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO  posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    
    #conn.commit()
    print(current_user.email)
    new_post = models.Post(**post.dict()) #converts all our entries into a dictionary instead of typing them manualy one by one incase we add another field in our model
    db.add(new_post)  #add the newly created post to our database
    db.commit() # push the changes back to the data base
    db.refresh(new_post) # reload the table and view the newly created post
    
    return new_post


# getting a single post by id
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first() # returns the first instance of the id required
    
    # print(id)
    #post = find_post(id)
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}
    return post


#code for deleting a post from the db
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # deleting post
    #index = find_index_post(id)
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#code for updating a post
@router.put("/{id}", response_model=schemas.Post) # the response_model parameter returns the data from the database in our defined terms
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    #index = find_index_post(id)
    
    post_query = db.query(models.Post).filter(models.Post.id == id) # query to find the post with a spcific id
    post = post_query.first() #taking the first post
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #post_dict = post.dict()
    #post_dict["id"] = id
    #my_posts[index] = post_dict
    return post_query.first()