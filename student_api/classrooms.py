from fastapi import APIRouter

class_router = APIRouter()
@class_router.get("/classrooms")
def get_classrooms():
    return {"classrooms": []}
