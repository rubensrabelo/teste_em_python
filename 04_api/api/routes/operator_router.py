from fastapi import APIRouter, Query
from starlette import status
import pandas as pd

from models import OperatorRequest
from repository.operator_repository import df_operator
from service.operator_service import search_operator_by_uf, search_operator_by_cnpj

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
    """
    Retorna uma lista de operadores com paginação.

    Args:
        skip (int): Número de registros a serem ignorados no início (default: 0, deve ser >= 0).
        limit (int): Número máximo de registros a serem retornados (default: 10, máximo: 100).

    Returns:
        list[OperatorRequest]: Lista de operadores paginada.
    """
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
    """
    Busca operadores pelo estado (UF) com paginação.

    Args:
        skip (int): Número de registros a serem ignorados no início (default: 0, deve ser >= 0).
        limit (int): Número máximo de registros a serem retornados (default: 10, máximo: 100).
        uf (str | None): Sigla do estado (UF) para busca (opcional, deve ter 2 caracteres).

    Returns:
        list[OperatorRequest]: Lista de operadores filtrados por UF e paginados.
    """
    if not uf:
        results = df_operator.copy()
    else:
        results = search_operator_by_uf(uf)
    results = results.map(lambda x: None if pd.isna(x) else x)
    lower = skip
    upper = lower + limit
    return results.iloc[lower:upper].to_dict(orient="records")


@router.get(
        "/cnpj/{cnpj}",
        status_code=status.HTTP_200_OK,
        response_model=list[OperatorRequest]
)
def search_operators_by_cnpj(cnpj: str):
    if len(cnpj) != 14:
        return []

    results = search_operator_by_cnpj(cnpj)

    if results.empty:
        return []

    return results.to_dict(orient="records")
