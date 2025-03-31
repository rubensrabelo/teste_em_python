from fastapi import APIRouter, Query
from starlette import status
import pandas as pd

from models import OperatorRequest
from repository.operator_repository import df_operator
from service.operator_service import search_operator_by_uf

router = APIRouter()


@router.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=list[OperatorRequest]
)
def find_all(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100)
):
    df_copy = df_operator.copy()
    df_copy = df_copy.map(lambda x: None if pd.isna(x) else x)
    lower = skip
    upper = lower + limit
    return df_copy.iloc[lower:upper].reset_index().to_dict(orient="records")


@router.get(
        "/uf",
        status_code=status.HTTP_200_OK,
        response_model=list[OperatorRequest]
)
def search_operators_by_uf(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    uf: str | None = Query(None, min_length=2, max_length=2)
):
    if not uf:
        results = df_operator.copy()
    else:
        results = search_operator_by_uf(uf)
    results = results.map(lambda x: None if pd.isna(x) else x)
    lower = skip
    upper = lower + limit
    return results.iloc[lower:upper].to_dict(orient="records")
