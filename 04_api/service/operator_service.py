from repository.operator_repository import df_operator


def search_operator_by_uf(uf_value: str):
    uf_value = uf_value.lower()
    results = df_operator[
        df_operator["UF"].str.lower().str.contains(uf_value, na=False)
    ]
    return results
