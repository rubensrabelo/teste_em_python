import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_BASE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


def get_links_pdfs(url_base):
    """
    Obtém os links dos arquivos PDF disponíveis na página especificada.

    Parâmetros:
        URL_BASE (str): URL da página contendo os links para download dos arquivos PDF.

    Retorna:
        list: Lista contendo os URLs dos arquivos PDF encontrados.
    """
    try:
        response = requests.get(url_base)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url_base}: {e}\n")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    div = soup.find("div", class_="cover-richtext-tile tile-content")

    if not div:
        print("Div de conteúdo não encontrada.\n")
        return []

    pdf_links = [
        urljoin(URL_BASE, a["href"]) for li in div.find_all("li")
        if (a := li.find("a", href=True)) and a["href"].endswith(".pdf")
    ]

    return pdf_links


def download_pdfs(pdf_links, destin_folder="files"):
    """
    Faz o download dos arquivos PDF a partir dos links fornecidos e os salva na pasta especificada.

    Parâmetros:
        pdf_links (list): Lista de URLs dos arquivos PDF a serem baixados.
        destin_folder (str): Caminho do diretório onde os arquivos serão armazenados. Padrão: "files".

    Retorna:
        str: Caminho da pasta onde os arquivos foram salvos.
    """
    os.makedirs(destin_folder, exist_ok=True)

    for pdf_url in pdf_links:
        pdf_name = os.path.join(destin_folder, pdf_url.split("/")[-1])

        try:
            print(f"Baixando: {pdf_url}.\n")
            pdf_response = requests.get(pdf_url)
            pdf_response.raise_for_status()

            with open(pdf_name, "wb") as file:
                file.write(pdf_response.content)
        except requests.RequestException as e:
            print(f"Erro ao acessar {pdf_url}: {e}")
            return []

    print("Download concluído.\n")
    return destin_folder


def compress_pdfs(destin_folder="files", zip_name="arquivos_pdfs.zip"):
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


if __name__ == "__main__":
    links_pdfs = get_links_pdfs(URL_BASE)

    if links_pdfs:
        destin_folder = download_pdfs(links_pdfs)
        compress_pdfs(destin_folder)
    else:
        print("Nenhum PDF encontrado para download.")
