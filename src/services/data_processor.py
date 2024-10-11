import pandas as pd
from typing import Dict, List, Tuple
from config.config import Config
from services.openai_service import OpenAIService

class DataProcessor:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
        self.categorias_por_produto = {}

    def processar_planilha(self, df: pd.DataFrame) -> pd.DataFrame:
        # Criar colunas para as categorias no DataFrame
        for coluna in Config.COLUNAS_OUTPUT:
            df[coluna] = ''
        
        # Processar por produto
        produtos_unicos = df[Config.COLUNAS['PRODUTO']].unique()
        for produto in produtos_unicos:
            df_produto = df[df[Config.COLUNAS['PRODUTO']] == produto]
            self._processar_produto(produto, df_produto)
        
        # Classificar cada linha
        for idx, row in df.iterrows():
            produto = row[Config.COLUNAS['PRODUTO']]
            categorias_produto = self.categorias_por_produto[produto]
            
            # Classificar esforço
            nota_esforco = row[Config.COLUNAS['NOTA_ESFORCO']]
            justificativa_esforco = row[Config.COLUNAS['JUSTIFICATIVA_ESFORCO']]
            nivel_esforco = 'baixo' if nota_esforco in Config.NOTAS_BAIXAS else 'alto'
            categoria_esforco = self._classificar_justificativa(
                justificativa_esforco, 
                categorias_produto['esforco'][nivel_esforco],
                'esforco'
            )
            df.at[idx, 'CATEGORIA_ESFORCO'] = categoria_esforco
            
            # Classificar satisfação
            nota_satisfacao = row[Config.COLUNAS['NOTA_SATISFACAO']]
            justificativa_satisfacao = row[Config.COLUNAS['JUSTIFICATIVA_SATISFACAO']]
            nivel_satisfacao = 'baixo' if nota_satisfacao in Config.NOTAS_BAIXAS else 'alto'
            categoria_satisfacao = self._classificar_justificativa(
                justificativa_satisfacao, 
                categorias_produto['satisfacao'][nivel_satisfacao],
                'satisfacao'
            )
            df.at[idx, 'CATEGORIA_SATISFACAO'] = categoria_satisfacao
            
            # Classificar combinada
            experiencia = 'negativa' if (nota_esforco in Config.NOTAS_BAIXAS or 
                                        nota_satisfacao in Config.NOTAS_BAIXAS) else 'positiva'
            categoria_combinada = self._classificar_justificativa_combinada(
                justificativa_esforco,
                justificativa_satisfacao,
                categorias_produto['combinada'][experiencia]
            )
            df.at[idx, 'CATEGORIA_COMBINADA'] = categoria_combinada
        
        return df

    def _processar_produto(self, produto: str, df_produto: pd.DataFrame):
        # Gerar categorias de esforço
        categorias_esforco = self._gerar_categorias_tipo(
            produto, df_produto, 'esforco')
        
        # Gerar categorias de satisfação
        categorias_satisfacao = self._gerar_categorias_tipo(
            produto, df_produto, 'satisfacao')
        
        # Gerar categorias combinadas
        categorias_combinadas = self._gerar_categorias_combinadas(
            produto, df_produto)
        
        self.categorias_por_produto[produto] = {
            'esforco': categorias_esforco,
            'satisfacao': categorias_satisfacao,
            'combinada': categorias_combinadas
        }

    def _gerar_categorias_tipo(self, produto: str, df: pd.DataFrame, tipo: str) -> Dict[str, List[str]]:
        coluna_justificativa = (Config.COLUNAS['JUSTIFICATIVA_ESFORCO'] if tipo == 'esforco' 
                               else Config.COLUNAS['JUSTIFICATIVA_SATISFACAO'])
        coluna_nota = (Config.COLUNAS['NOTA_ESFORCO'] if tipo == 'esforco' 
                      else Config.COLUNAS['NOTA_SATISFACAO'])
        
        justificativas_baixas = df[df[coluna_nota].isin(Config.NOTAS_BAIXAS)][coluna_justificativa].tolist()
        justificativas_altas = df[df[coluna_nota].isin(Config.NOTAS_ALTAS)][coluna_justificativa].tolist()
        
        prompt = (Config.PROMPT_TEMPLATES['criar_categorias_esforco'] if tipo == 'esforco'
                 else Config.PROMPT_TEMPLATES['criar_categorias_satisfacao'])
        
        categorias = self.openai_service.gerar_categorias(
            prompt.format(
                produto=produto,
                n_categorias=Config.N_CATEGORIAS,
                justificativas=justificativas_baixas + justificativas_altas
            )
        )
        
        return {
            'baixo': categorias['baixo'],
            'alto': categorias['alto']
        }

    def _gerar_categorias_combinadas(self, produto: str, df: pd.DataFrame) -> Dict[str, List[str]]:
        def get_experiencia(row):
            return ('negativa' if (row[Config.COLUNAS['NOTA_ESFORCO']] in Config.NOTAS_BAIXAS or 
                                  row[Config.COLUNAS['NOTA_SATISFACAO']] in Config.NOTAS_BAIXAS)
                    else 'positiva')
        
        df['experiencia'] = df.apply(get_experiencia, axis=1)
        
        justificativas_negativas = df[df['experiencia'] == 'negativa']
        justificativas_positivas = df[df['experiencia'] == 'positiva']
        
        categorias = self.openai_service.gerar_categorias(
            Config.PROMPT_TEMPLATES['criar_categorias_combinadas'].format(
                produto=produto,
                n_categorias=Config.N_CATEGORIAS,
                justificativas_esforco=justificativas_negativas[Config.COLUNAS['JUSTIFICATIVA_ESFORCO']].tolist() +
                                      justificativas_positivas[Config.COLUNAS['JUSTIFICATIVA_ESFORCO']].tolist(),
                justificativas_satisfacao=justificativas_negativas[Config.COLUNAS['JUSTIFICATIVA_SATISFACAO']].tolist() +
                                        justificativas_positivas[Config.COLUNAS['JUSTIFICATIVA_SATISFACAO']].tolist()
            )
        )
        
        return {
            'negativa': categorias['negativa'],
            'positiva': categorias['positiva']
        }

    def _classificar_justificativa(self, justificativa: str, categorias: List[str], tipo: str) -> str:
        return self.openai_service.classificar(
            Config.PROMPT_TEMPLATES['classificar'].format(
                tipo=tipo,
                justificativa=justificativa,
                categorias='\n'.join(categorias)
            )
        )

    def _classificar_justificativa_combinada(self, justificativa_esforco: str, 
                                            justificativa_satisfacao: str, 
                                            categorias: List[str]) -> str:
        justificativa_combinada = f"Esforço: {justificativa_esforco}\nSatisfação: {justificativa_satisfacao}"
        return self.openai_service.classificar(
            Config.PROMPT_TEMPLATES['classificar'].format(
                tipo='combinada',
                justificativa=justificativa_combinada,
                categorias='\n'.join(categorias)
            )
        )