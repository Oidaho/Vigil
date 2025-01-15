from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health")
def check_health(response: Response):
    return response
