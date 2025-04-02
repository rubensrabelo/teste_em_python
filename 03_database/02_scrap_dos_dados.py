import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile


def download_csv_from_table(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}\n")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", string="Relatorio_cadop.csv")  # Busca diretamente pelo link correto

    if link and link["href"]:
        csv_url = urljoin(url, link["href"])

        try:
            csv_response = requests.get(csv_url)
            csv_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao acessar {csv_url}: {e}\n")
            return

        csv_path = os.path.join(output_dir, "Relatorio_cadop.csv")

        with open(csv_path, "wb") as file:
            file.write(csv_response.content)
        print(f"CSV salvo em {csv_path}")
    else:
        print("Link do CSV não encontrado")


def download_and_extract_zip(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, os.path.basename(url))

    # Verificar se o ZIP já existe
    if os.path.exists(zip_path):
        print(f"Arquivo ZIP já existe: {zip_path}")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}\n")
        return

    with open(zip_path, "wb") as file:
        file.write(response.content)
    print(f"Arquivo ZIP salvo em {zip_path}")

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)
    print(f"Arquivos extraídos para {output_dir}")


def process_demonstracoes_contabeis(base_url, output_dir, years):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {base_url}: {e}\n")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    for year in years:
        year_folder = soup.find("a", href=True, string=lambda text: text and str(year) in text)
        if not year_folder:
            print(f"Pasta do ano {year} não encontrada.")
            continue

        try:
            year_url = urljoin(base_url, year_folder["href"])
            year_response = requests.get(year_url)
            year_response.raise_for_status()
        except requests.RequestException as e:
            print(f"Erro ao acessar {year_url}: {e}\n")
            continue

        year_soup = BeautifulSoup(year_response.text, "html.parser")
        zip_links = year_soup.find_all("a", href=True)

        year_output_dir = os.path.join(output_dir, str(year))
        os.makedirs(year_output_dir, exist_ok=True)

        found_zip = False
        for link in zip_links:
            if link["href"].endswith(".zip"):
                found_zip = True
                zip_url = urljoin(year_url, link["href"])
                download_and_extract_zip(zip_url, year_output_dir)

        if not found_zip:
            print(f"Nenhum arquivo ZIP encontrado para o ano {year}.")


if __name__ == "__main__":
    # Baixar CSV específico
    csv_page_url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
    csv_output_dir = "data/cadastros_empresas_ativas_na_ans"
    download_csv_from_table(csv_page_url, csv_output_dir)

    # Baixar e extrair demonstrações contábeis
    base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
    demonstracoes_output_dir = "data/demonstracoes_contabeis"
    process_demonstracoes_contabeis(base_url, demonstracoes_output_dir, [2023, 2024])
