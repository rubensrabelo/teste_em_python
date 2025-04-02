import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("CSV_PATH_OP")

OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(
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
            "Regiao_de_Comercializacao": "Int64",
            "Data_Registro_ANS": "string"
        }
    )

df['Regiao_de_Comercializacao'] = pd.to_numeric(df['Regiao_de_Comercializacao'], errors='coerce').astype('Int64')


operadoras = df[["Registro_ANS", "CNPJ", "Razao_Social", "Nome_Fantasia", "Modalidade", "DDD", "Telefone", "Fax", "Endereco_eletronico", "Regiao_de_Comercializacao", "Data_Registro_ANS"]]
enderecos = df[["Registro_ANS", "Logradouro", "Numero", "Complemento", "Bairro", "Cidade", "UF", "CEP"]]
representantes = df[["Registro_ANS", "Representante", "Cargo_Representante"]]

operadoras.to_csv(f"{OUTPUT_DIR}/operadoras.csv", index=False, sep=";")
enderecos.to_csv(f"{OUTPUT_DIR}/enderecos.csv", index=False, sep=";")
representantes.to_csv(f"{OUTPUT_DIR}/representantes.csv", index=False, sep=";")

print(f"Arquivo separados e salvos em: {OUTPUT_DIR}")
