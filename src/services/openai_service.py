import openai
from config.config import Config

class OpenAIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def gerar_categorias(self, prompt: str) -> list:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de feedback de clientes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip().split('\n')

    def classificar(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em classificação de feedback de clientes."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()