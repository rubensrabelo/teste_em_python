import os

from df_manager.df_manager import extract_table_from_pdf, rename_columns
from csv_manager.csv_manager import save_csv
from zip_manager.zip_manager import compress_file

OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(SCRIPT_DIR, "..", "01_web_scraping", "files", "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf")
CSV_PATH = os.path.join(OUTPUT_DIR, "tabela_extraida.csv")
ZIP_PATH = os.path.join(OUTPUT_DIR, "Teste_Rubens_Rabelo.zip")


if __name__ == "__main__":
    df = extract_table_from_pdf(PDF_PATH)
    df = rename_columns(df)

    if save_csv(df, CSV_PATH):
        compress_file(CSV_PATH, ZIP_PATH)
