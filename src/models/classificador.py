import json
from typing import List, Dict
from .produto import Produto
from ..services.openai_service import OpenAIService
from config.config import Config

class Classificador:
    def __init__(self, openai_service: OpenAIService):
        self.produtos: List[Produto] = []
        self.openai_service = openai_service

    def criar_categorias_gerais(self, motivos: List[str]):
        prompt = Config.PROMPT_TEMPLATES['criar_categorias'].format(
            n_categorias=Config.N_CATEGORIAS,
            motivos=motivos
        )
        return self.openai_service.gerar_categorias(prompt)

    def criar_categorias_produto(self, produto: Produto, motivos: List[str]):
        prompt = Config.PROMPT_TEMPLATES['criar_categorias_produto'].format(
            nome_produto=produto.nome_produto,
            n_categorias_produto=Config.N_CATEGORIAS_PRODUTO,
            motivos_produto=motivos
        )
        return self.openai_service.gerar_categorias(prompt)

    def classificar_justificativa(self, transcricao: str, produto: Produto) -> str:
        categorias = [cat.nome for cat in produto.listar_categorias()]
        prompt = Config.PROMPT_TEMPLATES['classificar'].format(
            transcricao=transcricao,
            categorias=categorias
        )
        return self.openai_service.classificar(prompt)

    def salvar_em_json(self, caminho: str):
        dados = {
            'produtos': [produto.to_dict() for produto in self.produtos]
        }
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar_de_json(self, caminho: str):
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        self.produtos = []
        for produto_dict in dados['produtos']:
            produto = Produto(nome_produto=produto_dict['nome_produto'])
            for categoria_dict in produto_dict['categorias']:
                categoria = produto.criar_categoria(
                    nome=categoria_dict['nome'],
                    tipo=categoria_dict['tipo']
                )
                for justificativa in categoria_dict['justificativas']:
                    categoria.adicionar_justificativa(justificativa)
            self.produtos.append(produto)
