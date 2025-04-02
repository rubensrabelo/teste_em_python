import tabula
import pandas as pd


def extract_table_from_pdf(pdf_path):
    """Extrai tabelas de um arquivo PDF e retorna um DataFrame consolidado.

    Args:
        pdf_path (str): Caminho para o arquivo PDF de origem.

    Returns:
        pd.DataFrame: DataFrame contendo os dados extraídos do PDF.
    """
    print("Transformando a tabela do Anexo 1 em DataFrame\n")
    try:
        tables = tabula.read_pdf(pdf_path, pages="3-181", multiple_tables=True, lattice=True)

        if not tables:
            raise ValueError("Nenhuma tabela encontrada no PDF.")

        filtered_tables = [table for table in tables if table.shape[1] == 13]

        for table in filtered_tables:
            table.columns = table.columns.str.replace(r"\s+", " ", regex=True).str.strip()
            table.columns = table.columns.str.replace(r"RN\s*\(alteração\)", "RN", regex=True)
            table.columns = table.columns.str.replace(r"\t", "", regex=True)

        df = pd.concat(filtered_tables, ignore_index=True)

        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        df = df.map(lambda x: " ".join(str(x).split()) if isinstance(x, str) else x)

        return df
    except Exception as e:
        print(f"Erro ao extrair a tabela do PDF: {e}\n")
        return pd.DataFrame()


def rename_columns(df):
    """Renomeia colunas específicas do DataFrame.

    Args:
        df (pd.DataFrame): DataFrame com os dados extraídos.

    Returns:
        pd.DataFrame: DataFrame com colunas renomeadas.
    """
    if df.empty:
        print("DataFrame vazio. Nenhuma coluna será renomeada.\n")
        return df

    return df.rename(
        columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}
    )
