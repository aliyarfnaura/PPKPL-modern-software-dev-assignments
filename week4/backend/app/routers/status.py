from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
def get_status() -> dict:
    return {"status": "running"}