import warnings

from langchain.agents import initialize_agent, AgentType, Tool
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.schema import SystemMessage, AIMessage, ChatResult, ChatGeneration
from langchain.memory import ConversationBufferMemory
from pydantic import ConfigDict

from agent.client import LLMClient
from agent.tools.call_fetch_oab import fetch_oab

warnings.filterwarnings('ignore', category=DeprecationWarning)


class CloudflareChatModel(BaseChatModel):
    client: LLMClient = None
    model_config = ConfigDict(extra='allow')


    def __init__(self):
        super().__init__()
        self.client = LLMClient()


    def _generate(self, messages, stop=None, **kwargs):
        system_prompt = SystemMessage(content=(
            '''
            Você é um assistente que responde sempre em português do Brasil.
            Quando for usar a ferramenta, apenas retorne a ação e aguarde a resposta.
            Não simule observações ou respostas finais sem antes executar a ferramenta.
            '''
        ))

        new_messages = [system_prompt]

        for msg in messages:
            if not isinstance(msg, SystemMessage):
                new_messages.append(msg)

        prompt_text = ''
        for msg in new_messages:
            prompt_text += f'{msg.content}\n'

        output = self.client.send_prompt(prompt_text)
        return self._create_chat_result(output)


    def _create_chat_result(self, content):
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content=content))]
        )


    @property
    def _llm_type(self) -> str:
        return 'cloudflare-chat'


def build_agent(verbose=True):
    llm = CloudflareChatModel()
    tools = [
        Tool(
            name='fetch_oab',
            func=fetch_oab,
            description=(
                'Consulta dados de advogados(as) no site da OAB. '
                'Use quando precisar encontrar informações como nome, número da OAB, estado ou categoria do advogado. '
                'Entrada: uma string contendo somente os parametros numero da oab, nome, uf(sigla do estado) e categoria'
                'Exemplo de entrada: \'"name": "FULANO", "uf": "SP"\''
            ),
            return_direct=True
        )
    ]
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        verbose=verbose,
        handle_parsing_errors=True,
    )
    return agent

if __name__ == '__main__':
    agent = build_agent(verbose=False)

    while True:
        question = input('Usuário: ')
        
        if question.lower() in ['sair', 'encerrar', 'exit', 'quit']:
            print('Encerrando agente de IA...')
            break

        try:
            answer = agent.invoke({'input': question})
            print(f'IA: {answer["output"]}')
        except Exception as e:
            print(f'Erro: {e}')
