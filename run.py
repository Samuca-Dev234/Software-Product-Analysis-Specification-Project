from modulos.dataextractor import DataExtractor



dados = DataExtractor()
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
dados.calcular_taxa_retorno_diaria()

dados.calcular_retorno_e_volatilidade_anual()


dados.salvar_acoes(file_name='teste')
