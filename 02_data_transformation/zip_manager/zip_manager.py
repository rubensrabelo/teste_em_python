import os
import zipfile


def compress_file(csv_path, zip_path):
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
