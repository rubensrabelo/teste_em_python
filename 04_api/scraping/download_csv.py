import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_csv_from_table(url, output_dir):
    """
    Baixa um arquivo CSV específico de uma página HTML.

    Args:
        url (str): URL da página que contém o link para o arquivo CSV
        output_dir (str): Diretório local onde o CSV será salvo

    Returns:
        str | None: Caminho do arquivo salvo ou None em caso de erro
    """
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "Relatorio_cadop.csv")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}\n")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", string=lambda text: text and "Relatorio_cadop" in text)

    if not link or not link.get("href"):
        print("Link do CSV não encontrado na página")
        return None

    csv_url = urljoin(url, link["href"])

    try:
        csv_response = requests.get(csv_url, timeout=10)
        csv_response.raise_for_status()

        content_type = csv_response.headers.get("Content-Type", "")
        if "text/csv" not in content_type and "application/octet-stream" not in content_type:
            print("O conteúdo baixado não é um CSV válido.")
            return None

        with open(csv_path, "wb") as file:
            file.write(csv_response.content)

        return csv_path

    except requests.RequestException as e:
        print(f"Erro ao baixar o CSV: {e}")
        return None
