import yfinance as yf
import pandas as pd
import numpy as np
import sys
import os


class FinanceAnalysis:
    def __init__(self):
        self.dataframe = None
        self.data_inicio = '2020-01-01'
        self.data_fim = '2023-08-11'
        self.simbolos = None


    def set_dados(self):
        if not os.path.exists('./base/acoes.csv'):
            self.dataframe = yf.download(self.simbolos, start=self.data_inicio, end=self.data_fim)['Adj Close']
        else:
            self.dataframe = pd.read_csv("./base/acoes.csv", index_col=0)
    
    def set_acoes(self, simbolos: list):
        self.simbolos = simbolos

    def set_nome_acoes(self, labels: dict):
        self.dataframe.rename(columns=labels, inplace=True)

    def calcular_taxa_retorno_diaria(self):
        retorno_diario = self.dataframe.pct_change()

        for coluna in retorno_diario.columns:
            self.dataframe[f'{coluna}_retorno_diario'] = retorno_diario[coluna]

    def alocacao_portfolio(self, dinheiro_total, sem_risco, repeticoes):
        dataset = self.dataframe.copy()
        dataset_original = self.dataframe.copy()
        

        melhor_sharpe_ratio = -sys.maxsize
        melhores_pesos = None
        melhor_volatilidade = 0
        melhor_retorno = 0

        lista_retorno_esperado = []
        lista_volatilidade_esperada = []
        lista_sharpe_ratio = []

        for _ in range(repeticoes):
            pesos = np.random.random(len(dataset.columns) - 1)
            pesos = pesos / pesos.sum()

            for i in dataset.columns[1:]:
                dataset[i] = dataset[i] / dataset[i][0]

            for i, acao in enumerate(dataset.columns[1:]):
                dataset[acao] = dataset[acao] * pesos[i] * dinheiro_total

            dataset.drop(columns='ibov', inplace=True)

            # Cálculos de retorno e volatilidade
            retorno_carteira = np.log(dataset / dataset.shift(1))
            matriz_covariancia = retorno_carteira.cov()

            retorno_esperado = np.sum(retorno_carteira.mean() * pesos) * 246
            volatilidade_esperada = np.sqrt(np.dot(pesos, np.dot(matriz_covariancia * 246, pesos)))

            # Cálculo do Sharpe Ratio
            sharpe_ratio = (retorno_esperado - sem_risco) / volatilidade_esperada

            # Atualizar o melhor Sharpe Ratio e os melhores pesos
            if sharpe_ratio > melhor_sharpe_ratio:
                melhor_sharpe_ratio = sharpe_ratio
                melhores_pesos = pesos
                melhor_volatilidade = volatilidade_esperada
                melhor_retorno = retorno_esperado

            lista_retorno_esperado.append(retorno_esperado)
            lista_volatilidade_esperada.append(volatilidade_esperada)
            lista_sharpe_ratio.append(sharpe_ratio)

            dataset = dataset_original.copy()
            
            
        nome_acoes_pesos = {acao: peso for acao, peso in zip(dataset.columns[:-1], pesos)}
        
        output_folder = './analises/'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Salvar resultados em um arquivo de texto
        with open(f"./analises/calculo_Markowitz _alocacao_ativos.txt", 'w') as file:
            file.write(f"Foi feito o cálculo de Markowitz com {repeticoes} repetições.\n")
            file.write(f"O Sharpe Ratio foi de {melhor_sharpe_ratio:.2f}.\n")
            file.write(f"Os pesos são:\n")
            for acao, peso in nome_acoes_pesos.items():
                file.write(f"{acao}: {peso:.2f}\n")
            file.write(f"A volatilidade foi de {melhor_volatilidade:.2f}.\n")
            file.write(f"O retorno foi de {melhor_retorno:.2f}.\n")
            file.write("\nLembrando que retornos passados não são garantia de retornos futuros.\n")
            

        return melhor_sharpe_ratio, melhores_pesos, lista_retorno_esperado, lista_volatilidade_esperada, lista_sharpe_ratio, melhor_volatilidade, melhor_retorno

    def salvar_acoes(self):
        if not os.path.exists('./base/acoes.csv'):
            self.dataframe.to_csv("./base/acoes.csv")
        
        

    def set_nome_colunas(self, labels: dict):
        self.dataframe.rename(columns=labels, inplace=True)