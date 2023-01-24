from fastapi import APIRouter

router = APIRouter()


@router.get("")
def read_admin():
    return {"admin": "admin"}
