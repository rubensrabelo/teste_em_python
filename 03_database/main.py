from modules.scrap_data_base import run_scrap_data_base
from modules.process_data_operators import run_process_data_operators
from modules.process_accounting_statements import run_process_accounting_statements


def main():
    """
    Executa o pipeline completo de processamento de dados.

    As funções são chamadas na seguinte ordem:
    1. `run_scrap_data_base()` - Realiza o scraping e download dos dados.
    2. `run_process_data_operators()` - Processa os dados das operadoras.
    3. `run_process_accounting_statements()` - Processa os dados contábeis.

    Returns:
        None
    """
    run_scrap_data_base()
    run_process_data_operators()
    run_process_accounting_statements()


if __name__ == "__main__":
    main()
