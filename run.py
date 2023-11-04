from modulos.finance_analysis import FinanceAnalysis
import numpy as np


dados = FinanceAnalysis()
dados.set_acoes(simbolos=['ROMI3.SA', 'RAPT4.SA', 'ITUB4.SA', 'GGBR4.SA', 'WEGE3.SA', '^BVSP'])

dados.set_dados()

column_mapping = {
    'ROMI3.SA': 'romi',
    'RAPT4.SA': 'rapt',
    'ITUB4.SA': 'itub',
    'GGBR4.SA': 'ggbr',
    'WEGE3.SA': 'Wweg',
    '^BVSP': 'ibov'
}


dados.set_nome_colunas(labels=column_mapping)

#dados.calcular_taxa_retorno_diaria()
#taxa_selic_historico = np.array([12.75, 14.25, 12.25, 6.5, 5.0, 2.0, 9.25, 13.75])
#dados.alocacao_portfolio(dinheiro_total=100000, sem_risco=taxa_selic_historico.mean() / 100, repeticoes=200)

dados.calcular_capm()

dados.salvar_acoes()
