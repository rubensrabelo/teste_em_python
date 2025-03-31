import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_BASE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


def get_links_pdfs(URL_BASE):
    try:
        response = requests.get(URL_BASE)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {URL_BASE}: {e}\n")
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
            print(f"Erro ao acessar {URL_BASE}: {e}")
            return []

    print("Download concluído.\n")
    return destin_folder


def compress_pdfs(destin_folder="files", zip_name="arquivos_pdfs.zip"):
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
