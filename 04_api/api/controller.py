from fastapi import APIRouter

from .routes.operator_router import router as operator_router

api_router = APIRouter()

api_router.include_router(
    operator_router,
    prefix="/operators",
    tags=["Operator"]
)
