import os
import pandas as pd
from glob import glob
from dotenv import load_dotenv


def load_configuration():
    """
    Carrega configurações e variáveis de ambiente necessárias.

    Returns:
        tuple: (CSV_PATH_DC, OUTPUT_DIR) - Caminho dos arquivos CSV e diretório de saída
    """
    load_dotenv()
    csv_path = os.getenv("CSV_PATH_DC")
    if not csv_path:
        raise ValueError("Variável de ambiente CSV_PATH_DC não definida")
    return csv_path, "files"


def find_csv_files(csv_path):
    csv_files = glob(os.path.join(csv_path, "**", "*.csv"), recursive=True)
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em {csv_path}")
    return csv_files


def process_csv_file(file_path):
    """
    Processa um único arquivo CSV de demonstração contábil.

    Args:
        file_path (str): Caminho completo para o arquivo CSV

    Returns:
        pd.DataFrame: DataFrame com os dados processados
    """
    df = pd.read_csv(
        file_path,
        delimiter=";",
        dtype={
            "REG_ANS": "string",
            "CD_CONTA_CONTABIL": "int",
            "DESCRICAO": "string",
            "VL_SALDO_INICIAL": "string",
            "VL_SALDO_FINAL": "string"
        }
    )

    df["DESCRICAO"] = df["DESCRICAO"].str.replace(r"\s+", " ", regex=True).str.strip()
    df["VL_SALDO_INICIAL"] = df["VL_SALDO_INICIAL"].str.replace(",", ".").astype(float)
    df["VL_SALDO_FINAL"] = df["VL_SALDO_FINAL"].str.replace(",", ".").astype(float)

    return df


# dataframes.append(df)
def consolidate_dataframes(dataframes):
    """
    Consolida múltiplos DataFrames em um único DataFrame.

    Args:
        dataframes (list): Lista de DataFrames a serem consolidados

    Returns:
        pd.DataFrame: DataFrame consolidado
    """
    return pd.concat(dataframes, ignore_index=True)


def save_consolidated_dataframe(df, output_dir, filename):
    """
    Salva o DataFrame consolidado em arquivo CSV.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo
        output_dir (str): Diretório de saída
        filename (str): Nome do arquivo de saída

    Returns:
        str: Caminho completo do arquivo salvo
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=False, sep=";")
    return output_path


def process_accounting_statements(csv_path=None, output_dir=None):
    """
    Função principal que orquestra todo o processamento.

    Args:
        csv_path (str, optional): Caminho para os arquivos CSV. Se None, usa variável de ambiente.
        output_dir (str, optional): Diretório de saída. Se None, usa "files".

    Returns:
        tuple: (df_consolidado, output_path) - DataFrame consolidado e caminho do arquivo salvo
    """
    if csv_path is None or output_dir is None:
        csv_path, output_dir = load_configuration()

    csv_files = find_csv_files(csv_path)
    dataframes = [process_csv_file(file) for file in csv_files]
    consolidate_df = consolidate_dataframes(dataframes)

    output_path = save_consolidated_dataframe(
        consolidate_df,
        output_dir,
        "demonstracoes_contabeis_consolidado.csv"
    )

    print(f"Arquivo consolidado salvo em: {output_path}")
    return consolidate_df, output_path


if __name__ == "__main__":
    try:
        process_accounting_statements()
    except Exception as e:
        print(f"Erro ao processar demonstrações contábeis: {str(e)}")