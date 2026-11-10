import pandas as pd

class LeitorCSV:
    def carregar(self, caminho_arquivo):
        try:
            df = pd.read_csv(caminho_arquivo, skipinitialspace=True)
            df.columns = [col.strip() for col in df.columns]
            return df
        except Exception as e:
            print(f"Erro ao carregar o arquivo CSV: {e}")
            return None