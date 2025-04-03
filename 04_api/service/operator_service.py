from repository.operator_repository import df_operator
from unidecode import unidecode


def search_operator_by_uf(uf_value: str):
    """
    Filtra operadores de planos de saúde pelo estado (UF).

    Args:
        uf_value (str): A sigla do estado (UF) a ser pesquisada.

    Returns:
        pandas.DataFrame: Um DataFrame contendo os operadores que possuem a UF
        correspondente.
    """
    uf_value = uf_value.lower()
    results = df_operator[
        df_operator["UF"].str.lower().str.contains(uf_value, na=False)
    ]
    return results


def search_by_company_name(name: str):
    """
    Busca operadores de planos de saúde pelo nome (parcial ou completo).

    Args:
        name (str): Parte do nome da empresa a ser pesquisado.

    Returns:
        pandas.DataFrame: DataFrame contendo os operadores encontrados.
    """
    name = unidecode(name.lower())
    df_operator["Razao_Social_Normalized"] = (
        df_operator["Razao_Social"]
        .astype(str)
        .apply(lambda x: unidecode(x.lower()))
        )

    results = (
        df_operator[df_operator["Razao_Social_Normalized"]
                    .str
                    .contains(name, na=False, regex=True)]
        )

    return results.drop(columns=["Razao_Social_Normalized"])


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
