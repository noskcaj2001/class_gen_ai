#%%
import os
from dotenv import load_dotenv


#%%
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('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')
    N_CATEGORIAS = 5
    
    # Definição das faixas de notas
    NOTAS_BAIXAS = [1, 2, 3]
    NOTAS_ALTAS = [4, 5]
    
    # Colunas da planilha
    COLUNAS = {
        'PRODUTO': 'NM_PROD',
        'JUSTIFICATIVA_ESFORCO': 'JUSTIFICATIVA_ESFORCO',
        'JUSTIFICATIVA_SATISFACAO': 'JUSTIFICATIVA_SATISFACAO',
        'NOTA_ESFORCO': 'NOTA_ESFORCO(1-5)',
        'NOTA_SATISFACAO': 'NOTA_SATISFACAO(1-5)'
    }
    
    # Novas colunas para o output
    COLUNAS_OUTPUT = [
        'CATEGORIA_ESFORCO',
        'CATEGORIA_SATISFACAO',
        'CATEGORIA_COMBINADA'
    ]
    
    PROMPT_TEMPLATES = {
        'criar_categorias_esforco': """
        Analise as justificativas de esforço fornecidas para o produto {produto}.
        Crie {n_categorias} categorias que expliquem a causa raiz das notas atribuídas.
        
        Divida em:
        - Notas Baixas (1, 2 e 3)
        - Notas Altas (4 e 5)
        
        Formato da resposta:
        NOTAS BAIXAS:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        NOTAS ALTAS:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        Justificativas:
        {justificativas}
        """,
        
        'criar_categorias_satisfacao': """
        Analise as justificativas de satisfação fornecidas para o produto {produto}.
        Crie {n_categorias} categorias que expliquem a causa raiz das notas atribuídas.
        
        Divida em:
        - Notas Baixas (1, 2 e 3)
        - Notas Altas (4 e 5)
        
        Formato da resposta:
        NOTAS BAIXAS:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        NOTAS ALTAS:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        Justificativas:
        {justificativas}
        """,
        
        'criar_categorias_combinadas': """
        Analise as justificativas de esforço E satisfação fornecidas para o produto {produto}.
        Crie {n_categorias} categorias que expliquem a experiência geral do cliente com o produto.
        
        Divida em:
        - Experiência Negativa (quando pelo menos uma das notas é baixa: 1, 2 ou 3)
        - Experiência Positiva (quando ambas as notas são altas: 4 ou 5)
        
        Formato da resposta:
        EXPERIÊNCIA NEGATIVA:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        EXPERIÊNCIA POSITIVA:
        1. [Categoria 1]
        2. [Categoria 2]
        ...
        
        Justificativas de Esforço:
        {justificativas_esforco}
        
        Justificativas de Satisfação:
        {justificativas_satisfacao}
        """,
        
        'classificar': """
        Classifique a seguinte justificativa em uma das categorias fornecidas.
        Se não se encaixar em nenhuma categoria, retorne 'Outros'.
        
        Tipo: {tipo}
        Justificativa: {justificativa}
        
        Categorias:
        {categorias}
        
        Responda apenas com o nome da categoria mais apropriada.
        """
    }
# %%
