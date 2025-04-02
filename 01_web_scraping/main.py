
from pdf_manager.pdf_manager import get_links_pdfs, download_pdfs
from zip_manager.zip_manager import compress_files

URL_BASE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"


if __name__ == "__main__":
    links_pdfs = get_links_pdfs(URL_BASE)

    if links_pdfs:
        destin_folder = download_pdfs(links_pdfs)
        compress_files(destin_folder)
    else:
        print("Nenhum PDF encontrado para download.")
