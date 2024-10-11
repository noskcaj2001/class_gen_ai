from dataclasses import dataclass, field
from typing import List

@dataclass
class Categoria:
    nome: str
    tipo: str  # 'baixa' ou 'alta'
    justificativas: List[str] = field(default_factory=list)

    def adicionar_justificativa(self, justificativa: str):
        self.justificativas.append(justificativa)

    def remover_justificativa(self, justificativa: str):
        if justificativa in self.justificativas:
            self.justificativas.remove(justificativa)

    def listar_justificativas(self) -> List[str]:
        return self.justificativas

    def to_dict(self):
        return {
            'nome': self.nome,
            'tipo': self.tipo,
            'justificativas': self.justificativas
        }