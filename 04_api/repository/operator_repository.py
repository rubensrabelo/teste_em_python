import pandas as pd
import os

from scraping.download_csv import download_csv_from_table

url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
output_dir = "data"
csv_path = download_csv_from_table(url, output_dir)


if csv_path and os.path.exists(csv_path):
    CSV_PATH = os.path.join("data", "Relatorio_cadop.csv")
    df_operator = pd.read_csv(
            CSV_PATH,
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
                "Regiao_de_Comercializacao": "string",
                "Logradouro": "string",
                "Numero": "string",
                "Complemento": "string",
                "Bairro": "string",
                "Cidade": "string",
                "UF": "string",
                "CEP": "string",
                "Representante": "string",
                "Cargo_Representante": "string"
            }
        )
