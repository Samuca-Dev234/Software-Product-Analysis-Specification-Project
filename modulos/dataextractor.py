import yfinance as yf
import pandas as pd
import numpy as np

class DataExtractor:
    def __init__(self):
        self.dataframe = None
        self.data_inicio = '2020-01-01'
        self.data_fim = '2023-08-11'
        self.simbolos = None


    def set_dados(self):
        self.dataframe = yf.download(self.simbolos, start=self.data_inicio, end=self.data_fim)['Adj Close']

    
    def set_acoes(self, simbolos: list):
        self.simbolos = simbolos

    def set_nome_acoes(self, labels: dict):
        self.dataframe.rename(columns=labels, inplace=True)

    def calcular_taxa_retorno_diaria(self):
        retorno_diario = self.dataframe.pct_change()

        for coluna in retorno_diario.columns:
            self.dataframe[f'{coluna}_retorno_diario'] = retorno_diario[coluna]


    def salvar_acoes(self, file_name: str):
        self.dataframe.to_csv(f"./base/{file_name}.csv")

    def set_nome_colunas(self, labels: dict):
        self.dataframe.rename(columns=labels, inplace=True)