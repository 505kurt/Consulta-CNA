import os
import requests

from dotenv import load_dotenv

load_dotenv()

CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID')
CF_API_TOKEN = os.getenv('CF_API_TOKEN')

BASE_URL = f'https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run'


class LLMClient:
    def __init__(self, model_name='@cf/meta/llama-4-scout-17b-16e-instruct'):
        self.model_name = model_name
        self.endpoint = f'{BASE_URL}/{self.model_name}'
        self.headers = {
            'Authorization': f'Bearer {CF_API_TOKEN}',
            'Content-Type': 'application/json'
        }


    def send_prompt(self, prompt: str):
        payload = {
            'messages': [
                {'role': 'system', 'content': 
                 '''
                    Você é um assistente que responde sempre em português do Brasil.
                    Quando for usar a ferramenta, apenas retorne a ação e aguarde a resposta.
                    Não simule observações ou respostas finais sem antes executar a ferramenta.
                '''
                },
                {'role': 'user', 'content': prompt}
            ],
            'function_call': 'auto'
        }

        response = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return data.get('result', {}).get('response', "").strip()
        else:
            raise Exception(f'Erro na API LLM: {response.status_code} - {response.text}')
