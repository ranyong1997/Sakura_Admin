from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT
from typing import Optional

app = FastAPI()


class Settings(BaseModel):
    # 利用 import secrets
    # secrets.token_hex() 生成密钥
    authjwt_secret_key: str = "4e95f0a14cc530df519cb8c4d77e8eb029fd40ac56fa16be572c58b5ee0b55af"


@AuthJWT.load_config
def get_config():
    return Settings()


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@test.com",
                "password": "123456"
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "admin",
                "password": "123456"
            }
        }


users = []


@app.get("/")
async def read_root():
    return {"HelloWorld"}


# 创建用户
@app.post("/signup", status_code=201)
async def create_user(user: User):
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    users.append(new_user)
    return new_user


# 获取所有用户
@app.get("/users", response_model=List[User])
async def get_users():
    return users


# 登录
@app.post("/login")
async def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    for u in users:
        if (u["username"] == user.username) and (u["password"] == user.password):
            # 生成token
            access_token = Authorize.create_access_token(subject=user.username)
            # 刷新token
            refresh_token = Authorize.create_refresh_token(subject=user.username)
            return {"access_token": access_token, "refresh_token": refresh_token}
        raise HTTPException(status_code=401, detail="用户名或密码错误")


# 验证token
@app.get("/protected")
async def get_logged_in_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌无效") from e
    current_user = Authorize.get_jwt_subject()
    return {"当前用户": current_user}


# 更新token
@app.get('/new_token')
async def create_new_token(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="令牌无效") from e
    current_user = Authorize.get_jwt_subject()
    access_token = Authorize.create_access_token(subject=current_user)
    return {"新的访问令牌": access_token}


#
@app.post('/fresh_login')
async def fresh_login(user: UserLogin, Authorize: AuthJWT = Depends()):
    for u in users:
        if (u["username"] == user.username) and (u["password"] == user.password):
            # 生成新token
            fresh_token = Authorize.create_access_token(subject=user.username, fresh=True)
            return {"fresh_token": fresh_token}
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码无效")


@app.get('/fresh_url')
async def get_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.fresh_jwt_required()
    except Exception as e:
        raise HTTPException(status=status.HTTP_401_UNAUTHORIZED, detail="令牌无效") from e
    current_user = Authorize.get_jwt_subject()
    return {"当前用户": current_user}
