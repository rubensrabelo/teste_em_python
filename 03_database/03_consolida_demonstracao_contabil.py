import os
import pandas as pd
from glob import glob
from dotenv import load_dotenv

load_dotenv()

CSV_PATH_DC = os.getenv("CSV_PATH_DC")
OUTPUT_DIR = "files"

os.makedirs(OUTPUT_DIR, exist_ok=True)

csv_files = glob(os.path.join(CSV_PATH_DC, "**", "*.csv"), recursive=True)

dataframes = []

for file in csv_files:
    df = pd.read_csv(
        file,
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

    dataframes.append(df)

df_final = pd.concat(dataframes, ignore_index=True)
output_path = os.path.join(OUTPUT_DIR, "demonstracoes_contabeis_consolidado.csv")
df_final.to_csv(output_path, index=False, sep=";")

print(f"Arquivo consolidado salvo em: {output_path}")
