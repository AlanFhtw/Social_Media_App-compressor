from pydantic import BaseModel
from typing import Optional
from base64 import b64decode
from base64 import b64encode
import tempfile


class User(BaseModel):
    username: str
    password: str
    profile_info: str


class Comment(BaseModel):
    user_id: int
    post_id: int
    content: str

class Like(BaseModel):
    user_id: int
    post_id: int

class Login(BaseModel):
    username: str
    password: str
