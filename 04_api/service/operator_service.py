from repository.operator_repository import df_operator


def search_operator_by_uf(uf_value: str):
    """
    Filtra operadores de planos de saúde pelo estado (UF).

    Args:
        uf_value (str): A sigla do estado (UF) a ser pesquisada.

    Returns:
        pandas.DataFrame: Um DataFrame contendo os operadores que possuem a UF correspondente.
    """
    uf_value = uf_value.lower()
    results = df_operator[
        df_operator["UF"].str.lower().str.contains(uf_value, na=False)
    ]
    return results


def search_operator_by_cnpj(cnpj: str):
    """
    Busca um operador pelo CNPJ exato.

    Args:
        cnpj (str): CNPJ do operador (14 caracteres).

    Returns:
        DataFrame: DataFrame contendo o operador correspondente ao CNPJ.
    """
    results = df_operator[df_operator["CNPJ"] == cnpj]
    return results
