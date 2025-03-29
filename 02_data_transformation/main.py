import os
import tabula
import pandas as pd
import zipfile
from io import BytesIO

pdf_path = "../01_web_scraping/pdfs/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
csv_path = "tabela_extraida.csv"
zip_name = "Teste_Rubens_Rabelo.zip"


def extract_table_from_pdf(pdf_path):
    tables = tabula.read_pdf(pdf_path, pages="3-181", multiple_tables=True)
    filtered_tables = [table for table in tables if table.shape[1] == 13]
    for i, table in enumerate(filtered_tables):
        table.columns = table.columns.str.replace(r"\s+", " ", regex=True).str.strip()
        table.columns = table.columns.str.replace(r"RN\s*\(alteração\)", "RN", regex=True)
        table.columns = table.columns.str.replace(r"\t", "", regex=True)
    df = pd.concat(filtered_tables, ignore_index=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def rename_columns(df):
    df.rename(columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=True)
    return df


def save_csv(df, csv_path):
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"CSV salvo em {csv_path}")


def compress_csv(csv_path, zip_name):
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))
    print(f"Arquivo compactado como {zip_name}")

df = extract_table_from_pdf(pdf_path)
df = rename_columns(df)
save_csv(df, csv_path)
compress_csv(csv_path, zip_name)