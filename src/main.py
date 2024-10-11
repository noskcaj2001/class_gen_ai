
#%%
import pandas as pd

#%%
from services.openai_service import OpenAIService
from services.data_processor import DataProcessor

def main():
    # Inicialização dos serviços
    openai_service = OpenAIService()
    data_processor = DataProcessor(openai_service)

    # Ler planilha de entrada
    df_input = pd.read_excel('data/input/base_pv.xlsx')
    
    # Processar dados
    df_output = data_processor.processar_planilha(df_input)
    
    # Salvar resultados
    df_output.to_excel('data/output/pesquisa_categorizada.xlsx', index=False)
    
    # Opcional: Salvar categorias em um arquivo JSON para referência
    import json
    with open('data/output/categorias.json', 'w', encoding='utf-8') as f:
        json.dump(data_processor.categorias_por_produto, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
# %%
