import os
import tabula
import pandas as pd
import zipfile

OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(SCRIPT_DIR, "..", "01_web_scraping", "files", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
CSV_PATH = os.path.join(OUTPUT_DIR, "tabela_extraida.csv")
ZIP_PATH = os.path.join(OUTPUT_DIR, "Teste_Rubens_Rabelo.zip")


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


def save_csv(df, csv_path):
    """Salva o DataFrame em um arquivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        csv_path (str): Caminho para salvar o arquivo CSV.

    Returns:
        bool: True se o CSV for salvo com sucesso, False caso contrário.
    """
    if df.empty:
        print("Erro: DataFrame vazio. O CSV não será salvo.\n")
        return False

    try:
        print("Gerando o CSV\n")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"CSV salvo em {csv_path}")
        return True
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")
        return False


def compress_csv(csv_path, zip_path):
    """Compacta o arquivo CSV em um arquivo ZIP.
    
    Args:
        csv_path (str): Caminho do arquivo CSV.
        zip_path (str): Caminho do arquivo ZIP de destino.

    Returns:
        bool: True se o ZIP for criado com sucesso, False caso contrário.
    """
    if not os.path.exists(csv_path):
        print("Erro: Arquivo CSV não encontrado. O ZIP não será criado.\n")
        return False

    try:
        print("Compactando o CSV em formato ZIP\n")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"Arquivo compactado como {zip_path}\n")
        return True
    except Exception as e:
        print(f"Erro ao compactar arquivos: {e}")
        return False


if __name__ == "__main__":
    df = extract_table_from_pdf(PDF_PATH)
    df = rename_columns(df)

    if save_csv(df, CSV_PATH):
        compress_csv(CSV_PATH, ZIP_PATH)
