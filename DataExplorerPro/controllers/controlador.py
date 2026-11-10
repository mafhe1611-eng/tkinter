import pandas as pd

class Controlador:

    def calcular_total_registros(self, df):

        if df is not None:
            return len(df)

        return 0

    def calcular_soma_vendas(self, df):

        if df is not None and 'Quantidade' in df.columns and 'Valor' in df.columns:

            total = (df['Quantidade'] * df['Valor']).sum()

            return total

        return 0

    def filtrar_por_produto(self, df, nome_produto):

        if df is not None and nome_produto:

            df_filtrado = df[
                df['Produto'].astype(str).str.contains(
                    nome_produto,
                    case=False,
                    na=False
                )
            ]

            return df_filtrado

        return df

    def quantidade_total_produtos(self, df):

        if df is not None and 'Quantidade' in df.columns:
            return df['Quantidade'].sum()

        return 0

    def valor_medio_produtos(self, df):

        if df is not None and 'Valor' in df.columns:
            return df['Valor'].mean()

        return 0

    def produto_mais_vendido(self, df):

        if df is not None and 'Produto' in df.columns and 'Quantidade' in df.columns:
            return df.loc[df['Quantidade'].idxmax(), 'Produto']

        return ""

    def quantidade_produtos_diferentes(self, df):

        if df is not None and 'Produto' in df.columns:
            return df['Produto'].nunique()

        return 0

    def filtar_por_produto(self, df, nome_produto):
        return self.filtrar_por_produto(df, nome_produto)
    
    def quantidade_total_produtos(self):
        return self.df["Quantidade"].sum()

    def valor_medio_produtos(self):
        return self.df["Valor"].mean()

    def produto_mais_vendido(self):
        return self.df.loc[self.df["Quantidade"].idxmax(), "Produto"]

    def quantidade_produtos_diferentes(self):
        return self.df["Produto"].nunique()
