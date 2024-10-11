from dataclasses import dataclass, field
from typing import Dict, List
from .categoria import Categoria

@dataclass
class Produto:
    nome_produto: str
    categorias_esforco: Dict[str, List[Categoria]] = field(default_factory=lambda: {'baixo': [], 'alto': []})
    categorias_satisfacao: Dict[str, List[Categoria]] = field(default_factory=lambda: {'baixo': [], 'alto': []})

    def criar_categoria(self, nome: str, tipo: str, categoria_tipo: str, nivel: str):
        categoria = Categoria(nome=nome, tipo=tipo)
        if categoria_tipo == 'esforco':
            self.categorias_esforco[nivel].append(categoria)
        else:
            self.categorias_satisfacao[nivel].append(categoria)
        return categoria

    def to_dict(self):
        return {
            'nome_produto': self.nome_produto,
            'categorias_esforco': {
                'baixo': [cat.to_dict() for cat in self.categorias_esforco['baixo']],
                'alto': [cat.to_dict() for cat in self.categorias_esforco['alto']]
            },
            'categorias_satisfacao': {
                'baixo': [cat.to_dict() for cat in self.categorias_satisfacao['baixo']],
                'alto': [cat.to_dict() for cat in self.categorias_satisfacao['alto']]
            }
        }