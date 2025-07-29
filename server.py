from fastapi import FastAPI
from pydantic import BaseModel

users = {
    0: {"userid": "apple", "name": "김사과"},
    1: {"userid": "banana", "name": "반하나"},
    2: {"userid": "orange", "name": "오렌지"}
}

application = FastAPI()

@application.get("/users/{id}")
def find_user(id: int):
    user = users.get(id)
    if user is None:
        return {"error": "해당 id 없음"}
    return user

@application.get("/users/{id}/{key}")   # 경로를 통해 보냄
def find_user_by_key(id: int, key: str):
    user = users.get(id)
    if user is None or key not in user:
        return {"error": "잘못된 id 또는 key"}
    return user[key]

@application.get("/id-by-name")
def find_id_by_name(name: str): # 물음표(값)을 통해 보냄
    # items은 키와 값을 쌍으로 갖는 딕셔너리의 아이템들
    for idx, user in users.items():
        if user["name"] == name:
            return user
    return {"error": "데이터를 찾지 못함"}

# 무언가를 상속받아서 클래스를 정의할 때 사용
class User(BaseModel):
    # JSON의 키와 값을 정의
    userid: str
    name: str
    
@application.post("/users/{id}")
def create_user(id: int, user: User):
    if id in users:
        return {"error": "이미 존재하는 키"}
    # 클래스 형태로 그대로 새로 복사해서 만들면 dic에 추가
    users[id] = user.model_dump()
    return {"success": "ok"}

class UserForUpdate(BaseModel):
    userid: str | None = None
    name: str | None = None
    
@application.put("/users/{id}")
def update_user(id: int, user: UserForUpdate):
    if id not in users:
        return {"error": "id가 존재하지 않음"}
    if user.userid is not None:
        users[id]["userid"] = user.userid
    if user.name is not None:
        users[id]["name"] = user.name
        
    return {"success": "ok"}

@application.delete("/users/{id}")
def delete_user(id: int):
    if id not in users:
        return {"error": "id가 존재하지 않음"}
    del users[id]
    return {"success": "ok"}