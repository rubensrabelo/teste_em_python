import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile
from dotenv import load_dotenv


def load_environment_variables():
    """
    Carrega as variáveis de ambiente do arquivo .env.

    Returns:
        dict: Dicionário contendo as seguintes chaves:
            - CSV_PAGE_URL (str): URL da página contendo o link do CSV.
            - CSV_OUTPUT_DIR (str): Diretório de saída do arquivo CSV.
            - BASE_URL (str): URL base para os demonstrativos contábeis.
            - DEMONSTRACOES_OUTPUT_DIR (str): Diretório de saída dos demonstrativos contábeis.
            - YEARS (list): Lista de anos a serem processados.
    """
    load_dotenv()
    return {
        "CSV_PAGE_URL": os.getenv("CSV_PAGE_URL"),
        "CSV_OUTPUT_DIR": os.getenv("CSV_OUTPUT_DIR"),
        "BASE_URL": os.getenv("BASE_URL"),
        "DEMONSTRACOES_OUTPUT_DIR": os.getenv("DEMONSTRACOES_OUTPUT_DIR"),
        "YEARS": list(map(int, os.getenv("YEARS", "").split(',')))
    }


def download_csv_from_table(url, output_dir):
    """
    Faz o scraping de uma página da web para baixar um arquivo CSV.

    Args:
        url (str): URL da página contendo o link do CSV.
        output_dir (str): Diretório onde o arquivo CSV será salvo.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}\n")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("a", string="Relatorio_cadop.csv")

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
    """
    Faz o download de um arquivo ZIP e extrai seu conteúdo.

    Se o arquivo ZIP já existir no diretório, ele não será baixado novamente.

    Args:
        url (str): URL do arquivo ZIP.
        output_dir (str): Diretório onde o arquivo será salvo e extraído.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, os.path.basename(url))

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


def process_accounting_statements(base_url, output_dir, years):
    """
    Faz o scraping dos demonstrativos contábeis de uma série de anos.

    O processo busca na página principal as pastas correspondentes aos anos desejados,
    localiza os arquivos ZIP dentro dessas pastas e faz o download e extração.

    Args:
        base_url (str): URL base onde estão localizados os demonstrativos contábeis.
        output_dir (str): Diretório onde os arquivos extraídos serão armazenados.
        years (list): Lista de anos a serem processados.

    Returns:
        None
    """
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


def run_scrap_data_base():
    """
    Executa o processo de scraping de dados.

    Este processo inclui:
    1. O download de um arquivo CSV contendo informações de operadoras.
    2. O processamento e download de demonstrações contábeis organizadas por ano.

    As URLs e diretórios de saída são carregados a partir das variáveis de ambiente.

    Returns:
        None
    """
    env_vars = load_environment_variables()
    download_csv_from_table(env_vars["CSV_PAGE_URL"], env_vars["CSV_OUTPUT_DIR"])
    process_accounting_statements(env_vars["BASE_URL"], env_vars["DEMONSTRACOES_OUTPUT_DIR"], env_vars["YEARS"])
