from fastapi import APIRouter, Query
from starlette import status
import pandas as pd

from models import OperatorRequest
from repository.operator_repository import df_operator
from service.operator_service import (
    search_operator_by_uf, search_operator_by_cnpj, search_by_company_name
)

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
        skip (int): Número de registros a serem ignorados no início
            (default: 0, deve ser >= 0).
        limit (int): Número máximo de registros a serem retornados
            (default: 10, máximo: 100).

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
        skip (int): Número de registros a serem ignorados no início
            (default: 0, deve ser >= 0).
        limit (int): Número máximo de registros a serem retornados
            (default: 10, máximo: 100).
        uf (str | None): Sigla do estado (UF) para busca
            (opcional, deve ter 2 caracteres).

    Returns:
        list[OperatorRequest]: Lista de operadores filtrados por
            UF e paginados.
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
    "/operators/name",
    status_code=status.HTTP_200_OK,
    summary="Buscar operadores por nome",
    description="Retorna operadores que possuem parte do nome informado.",
)
def get_operators_by_name(
    name: str | None = Query(None, min_length=1, max_length=250),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
):
    """
     Busca operadores pelo nome com paginação.

    Args:
        name (str | None): Parte do nome do operador a ser buscado
            (opcional, mínimo: 1 caractere, máximo: 250).
        skip (int): Número de registros a serem ignorados no início
            (default: 0, deve ser >= 0).
        limit (int): Número máximo de registros a serem retornados
            (default: 10, máximo: 100).

    Returns:
        list[dict]: Lista de operadores que possuem parte do nome informado,
            com paginação aplicada.
    """
    if not name:
        results = df_operator.copy()
    else:
        results = search_by_company_name(name)
    return results.iloc[skip: skip + limit].to_dict(orient="records")


@router.get(
        "/cnpj/{cnpj}",
        status_code=status.HTTP_200_OK,
        response_model=list[OperatorRequest]
)
def search_operators_by_cnpj(cnpj: str):
    """
    Busca operadores pelo CNPJ.

    Args:
        cnpj (str): Número do CNPJ a ser buscado
            (deve ter exatamente 14 caracteres).

    Returns:
        list[OperatorRequest]: Lista de operadores correspondentes
            ao CNPJ informado.
        Retorna uma lista vazia caso o CNPJ não tenha 14 caracteres
            ou não haja resultados.
    """
    if len(cnpj) != 14:
        return []

    results = search_operator_by_cnpj(cnpj)

    if results.empty:
        return []

    return results.to_dict(orient="records")
