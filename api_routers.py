from fastapi import APIRouter, File, Form, HTTPException, File, UploadFile, Form
from datamodel import *
import sqlite3
import datetime as dt
import logging
import auth_utils
import db
from typing import Optional

router = APIRouter()

#API Extension
@router.post("/post/user")
def add_user(user: User):
    db = 'app.db'
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' INSERT INTO Users(username, password, profile_info) VALUES(?,?,?) '''
            user_data = (user.username, auth_utils.hash_password(user.password), user.profile_info)
            cur.execute(sql, user_data)
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        logging.error("add_user: Integrity Error")
        raise HTTPException(status_code=422, detail="Integrity Error")
    except sqlite3.OperationalError:
        logging.error("add_user: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("add_user: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("add_user: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("add_user: General Error")



#manadotry
@router.post("/post")
# def add_post(post: Post):
async def add_post(user_id: int = Form(...),  description: str = Form(...), image: Optional[UploadFile] = File(None)):
    db = 'app.db'
    if image:
        contents = await image.read()
    else:
        contents = None
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' INSERT INTO Posts(user_id, content, image)  VALUES(?,?,?) '''
            post_data = (user_id, description, b64encode(contents).decode('utf-8'))
            cur.execute(sql, post_data)
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        logging.error("add_post: Integrity Error")
        raise HTTPException(status_code=422, detail="Integrity Error")
    except sqlite3.OperationalError:
        logging.error("add_post: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("add_post: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("add_post: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("add_post: General Error")

#API Extension
@router.post("/post/comment")
def add_comment(comment: Comment):
    db = 'app.db'
    timestamp = dt.datetime.now()
    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' INSERT INTO Comments(user_id, post_id, content) VALUES(?,?,?) '''
            comment_data = (comment.user_id, comment.post_id, comment.content)
            cur.execute(sql, comment_data)
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        logging.error("add_comment: Integrity Error")
        raise HTTPException(status_code=422, detail="Integrity Error")
    except sqlite3.OperationalError:
        logging.error("add_comment: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("add_comment: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("add_comment: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("add_comment: General Error")

@router.get("/get/comment")
def get_comment(post_id: int):
    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' SELECT * FROM Comments WHERE post_id=? ORDER BY created_at DESC'''
            cur.execute(sql, (post_id, ))
            return cur.fetchall()
    except sqlite3.OperationalError:
        logging.error("get_comment: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("get_comment: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("get_comment: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("get_comment: General Error")




#API Extension
@router.post("/post/like")
def add_like(like: Like):
    db = 'app.db'
    try:
        with sqlite3.connect(db) as conn:  # Use a context manager to handle the connection
            cur = conn.cursor()
            sql = ''' INSERT INTO Likes(user_id, post_id) VALUES(?,?) '''
            like_data = (like.user_id, like.post_id)
            cur.execute(sql, like_data)
            conn.commit()
            return cur.lastrowid
    except sqlite3.IntegrityError:
        logging.error("add_like: Integrity Error")
        raise HTTPException(status_code=422, detail="Integrity Error")
    except sqlite3.OperationalError:
        logging.error("add_like: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("add_like: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("add_like: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("add_like: General Error")

@router.get("/get/like")
def get_like(post_id: int):
    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' SELECT * FROM Likes WHERE post_id=? ORDER BY created_at DESC'''
            cur.execute(sql, (post_id, ))
            return cur.fetchall()
    except sqlite3.OperationalError:
        logging.error("get_like: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("get_like: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("get_like: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("get_like: General Error")



#mandatory
@router.get("/get/posts/newest")
def get_newest_post():
    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' SELECT * FROM Posts ORDER BY created_at DESC LIMIT 1'''
            cur.execute(sql, )
            return cur.fetchone()
    except sqlite3.OperationalError:
        logging.error("get_newest_post: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("get_newest_post: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("get_newest_post: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("get_newest_post: General Error")


#mandatory
@router.get("/get/posts")
def get_all_posts():
    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:  # Use a context manager to handle the connection
            cur = conn.cursor()
            sql = ''' SELECT * FROM Posts'''
            cur.execute(sql, )
            return cur.fetchall()
    except sqlite3.OperationalError:
        logging.error("get_all_posts: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("get_all_posts: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("get_all_posts: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("get_all_posts: General Error")


#mandatory
@router.get("/get/post/user")
def get_post_byUser(user_id: int):
    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:  # Use a context manager to handle the connection
            cur = conn.cursor()
            sql = ''' SELECT * FROM Posts WHERE user_id=?'''
            cur.execute(sql, (user_id,))
            return cur.fetchall()
    except sqlite3.OperationalError:
        logging.error("get_post_byUser: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("get_post_byUser: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("get_post_byUser: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("get_post_byUser: General Error")