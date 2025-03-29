import os
import requests
import zipfile
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def download_pdfs(url_base, destin_folder="pdfs"):
    response = requests.get(url_base)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    div = soup.find("div", class_="cover-richtext-tile tile-content")

    pdf_links = []

    if div:
        for li in div.find_all("li"):
            link = li.find("a", href=True)
            if link and link["href"].endswith(".pdf"):
                pdf_url = urljoin(url_base, link["href"])
                pdf_links.append(pdf_url)

    os.makedirs(destin_folder, exist_ok=True)

    for pdf_url in pdf_links:
        pdf_name = os.path.join(destin_folder, pdf_url.split("/")[-1])
        print(f"Baixando: {pdf_url}.")
        print()

        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()

        with open(pdf_name, "wb") as file:
            file.write(pdf_response.content)

    print("Download concluído.")

    return destin_folder


def compress_pdfs(destin_folder="pdfs", zip_name="arquivos_pdfs.zip"):
    zip_path = os.path.join(destin_folder, zip_name)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(destin_folder):
            for file in files:
                if file.endswith(".pdf"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, destin_folder))
    
    print()
    print(f"Arquivos compactados em {zip_path}")

url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

destin_folder = download_pdfs(url_base)
compress_pdfs(destin_folder)