import os
import pandas as pd
from dotenv import load_dotenv


def load_environment_variables():
    """
    Carrega variáveis de ambiente do arquivo .env.

    Returns:
        str: Caminho para o arquivo CSV obtido da variável de ambiente CSV_PATH_OP
    """
    load_dotenv()
    csv_path = os.getenv("CSV_PATH_OP")
    if not csv_path:
        raise ValueError("Variável de ambiente CSV_PATH_OP não definida")
    return csv_path


# OUTPUT_DIR = "files"

def load_data(csv_path):
    """
    Carrega e prepara os dados do arquivo CSV.

    Args:
        csv_path (str): Caminho para o arquivo CSV

    Returns:
        pd.DataFrame: DataFrame com os dados carregados e formatados
    """
    try:
        df = pd.read_csv(
                csv_path,
                delimiter=";",
                dtype={
                    "Registro_ANS": "string",
                    "CNPJ": "string",
                    "Razao_Social": "string",
                    "Nome_Fantasia": "string",
                    "Modalidade": "string",
                    "DDD": "string",
                    "Telefone": "string",
                    "Fax": "string",
                    "Endereco_eletronico": "string",
                    "Regiao_de_Comercializacao": "Int64",
                    "Data_Registro_ANS": "string"
                }
            )

        df['Regiao_de_Comercializacao'] = pd.to_numeric(
            df['Regiao_de_Comercializacao'],
            errors='coerce'
            ).astype('Int64')
        return df
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}") from e


def separar_dataframes(df):
    """
    Separa o DataFrame principal em três DataFrames especializados.

    Args:
        df (pd.DataFrame): DataFrame com todos os dados originais

    Returns:
        tuple: (operadoras_df, enderecos_df, representantes_df)
    """
    operator = df[
        ["Registro_ANS", "CNPJ", "Razao_Social", "Nome_Fantasia",
         "Modalidade", "DDD", "Telefone", "Fax", "Endereco_eletronico",
         "Regiao_de_Comercializacao", "Data_Registro_ANS"]
    ]
    address = df[
        ["Registro_ANS", "Logradouro", "Numero", "Complemento",
         "Bairro", "Cidade", "UF", "CEP"]
    ]
    representatives = df[
        ["Registro_ANS", "Representante", "Cargo_Representante"]
    ]
    return operator, address, representatives


def salvar_dataframes(operator, address, representatives, output_dir):
    """
    Salva os DataFrames em arquivos CSV separados.

    Args:
        operadoras (pd.DataFrame): Dados das operadoras
        enderecos (pd.DataFrame): Dados de endereço
        representantes (pd.DataFrame): Dados dos representantes
        output_dir (str): Diretório de saída

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    operator.to_csv(f"{output_dir}/operadoras.csv", index=False, sep=";")
    address.to_csv(f"{output_dir}/enderecos.csv", index=False, sep=";")
    representatives.to_csv(
        f"{output_dir}/representantes.csv", index=False, sep=";"
    )

    print(f"Arquivo separados e salvos em: {output_dir}")


def process_data_operators(csv_path=None, output_dir="files"):
    if csv_path is None:
        csv_path = load_environment_variables()

    df = load_data(csv_path)
    operadoras, enderecos, representantes = separar_dataframes(df)
    salvar_dataframes(operadoras, enderecos, representantes, output_dir)

    return operadoras, enderecos, representantes


if __name__ == "__main__":
    try:
        process_data_operators()
    except Exception as e:
        print(f"Erro ao processar dados: {str(e)}")
