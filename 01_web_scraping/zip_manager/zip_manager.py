import os
import zipfile


def compress_files(destin_folder="files", zip_name="arquivos_pdfs.zip"):
    """
    Compacta os arquivos PDF baixados em um único arquivo ZIP.

    Parâmetros:
        destin_folder (str): Caminho do diretório contendo os arquivos a serem compactados. Padrão: "files".
        zip_name (str): Nome do arquivo ZIP a ser gerado. Padrão: "arquivos_pdfs.zip".

    Retorna:
        None
    """
    zip_path = os.path.join(destin_folder, zip_name)

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(destin_folder):
                for file in files:
                    if file.endswith(".pdf"):
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(
                            file_path,
                            destin_folder
                        ))
        print(f"Arquivos compactados em {zip_path}")
    except Exception as e:
        print(f"Erro ao compactar arquivos: {e}")
