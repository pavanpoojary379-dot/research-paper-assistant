from fastapi import APIRouter

router = APIRouter(
    prefix="/papers",
    tags=["Research Papers"]
)


@router.get("/")
def test():
    return {
        "message": "Paper Module Working"
    }