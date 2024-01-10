import bcrypt
import sqlite3
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datamodel import *
import logging


router = APIRouter()

# has pw
def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

# verify pw
def check_password(hashed_password, user_password):
    user_password_bytes = user_password.encode('utf-8')
    return bcrypt.checkpw(user_password_bytes, hashed_password)

# user log in (check pw)
#API Extension
@router.post("/post/login")
def login_user(login: Login):

    db = 'app.db'

    try:
        with sqlite3.connect(db) as conn:
            cur = conn.cursor()
            sql = ''' SELECT password FROM Users WHERE username = ?'''
            cur.execute(sql, (login.username,))
            result = cur.fetchone()
            if result and check_password(result[0], login.password):
                return True
            else:
                return False
    except sqlite3.OperationalError:
        logging.error("login_user: Operational Error")
        raise HTTPException(status_code=500, detail="Operational Error")
    except sqlite3.DataError:
        logging.error("login_user: Data Error")
        raise HTTPException(status_code=500, detail="Data Error")
    except sqlite3.DatabaseError:
        logging.error("login_user: Database Error")
        raise HTTPException(status_code=500, detail="Database Error")
    except Exception as e:
        logging.error("login_user: General Error")
