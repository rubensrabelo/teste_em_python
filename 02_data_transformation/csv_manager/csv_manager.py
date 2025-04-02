def save_csv(df, csv_path):
    """Salva o DataFrame em um arquivo CSV.

    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        csv_path (str): Caminho para salvar o arquivo CSV.

    Returns:
        bool: True se o CSV for salvo com sucesso, False caso contrário.
    """
    if df.empty:
        print("Erro: DataFrame vazio. O CSV não será salvo.\n")
        return False

    try:
        print("Gerando o CSV\n")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"CSV salvo em {csv_path}")
        return True
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")
        return False
