### Descrição do projeto
O objetivo do projeto é permitir a consulta automatizada de dados de advogados(as) registrados no site oficial da OAB (Cadastro Nacional dos Advogados - CNA), utilizando técnicas de scraping, uma API compatível com uso por IA e um agente LLM com capacidade de interpretar perguntas em linguagem natural. 

A aplicação é composta por três principais componentes: um scraper utilizado para extrair dados do site do CNA, uma API construída com FastAPI que expõe a funcionalidade de consulta, e um agente LLM baseado em LangChain que utiliza a API para responder perguntas de forma automatizada e contextualizada.

### ⚠️ Limitações e Pendências da Implementação
Devido a limitações técnicas e de prazo, nem todas as implementações previstas para o projeto estão presentes ou totalmente funcionais.  

Como programador, por não ter experiência prévia com o Protocolo MCP, não obtive êxito em sua implementação e optei por utilizar um modelo de _Function Calling_ padrão, a fim de garantir um entregável mínimo dentro do prazo. Além disso, o modelo de IA que escolhi utilizar (`@cf/meta/llama-4-scout-17b-16e-instruct`) apresentou dificuldades em direcionar corretamente os parâmetros da ferramenta de busca, o que resultou em inconsistências nas operações de consulta via prompt.

Como melhorias futuras, pretendo reestruturar o modelo de chamada de função para seguir corretamente o Protocolo MCP, além de revisar o mecanismo de passagem de parâmetros da LLM para a ferramenta de busca.

### Estrutura do Projeto
```
.
├── scraper/ #modulos de scraping
│   ├── ocr.py   #utiliza easyocr para obter o status da busca
│   └── extractor.py  #extração de dados da página
├── agent/ #módulos do agente de IA
│   ├── client.py  #envia prompts para o modelo de linguagem hospedado no CF Workers AI
│   └── agent.py  #implementa o modelo de linguagem com a ferramenta fetch_oab
├── api/
│	├── app.py  #lógica da api
│	└── models.py  #basemodels utilizados pela api
├── run_agent.py  #inicia um agente LLM interativo no terminal
├── run_api.py  #inicializa a API FastAPI que expõe o endpoint /fetch_oab
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### Requisitos
Antes de executar o projeto, certifique-se de ter os seguintes requisitos instalados em sua máquina:

- **Docker** (versão mais recente recomendada)
    
- **Docker Compose** 
    
- **Conta no Cloudflare Workers AI**
    
- Conexão com a internet para realizar chamadas HTTP à API da Cloudflare e ao site da OAB

### Configurações de Ambiente
O projeto requer duas variáveis de ambiente configuradas para autenticação com o serviço de IA:
- `CF_ACCOUNT_ID`: ID da sua conta Cloudflare
- `CF_API_TOKEN`: Token de autenticação para acesso à API

Para obtê-las você deve:
- Criar ou entrar em sua conta do [Cloudflare](https://dash.cloudflare.com/)
- No URL da página, após ".com/" copiar o campo com sua chave ID - essa é sua `CF_ACCOUNT_ID`
- No painel `Manage Account > Account API Tokens`, selecionar as opções `Create Token > Create Custom Token`, na seção "Token Name" atribuir o nome do novo token, na seção "Permissions" marcar os campos como `Account - Workers AI - Read`, clicar em `Continue to Summary > Create Token` e copiar o token exibido na tela - esse é seu `CF_API_TOKEN`

Com as duas variáveis em mãos, você precisa criar um arquivo `.env` na pasta raiz do projeto, e colar as chaves como no exemplo:
```
CF_ACCOUNT_ID={SUA_CF_ACCOUNT_ID_AQUI}

CF_API_TOKEN={SEU_API_TOKEN_AQUI}
```

Após realizar o processo suas variáveis de ambiente já estão configuradas e prontas para uso.

### Instalação e Execução 
Siga os passos abaixo para rodar o projeto localmente utilizando Docker e Docker Compose:

1. **Clone** o repositório.
2. Configure as **variáveis de ambiente** seguindo a explicação acima.
3. **Construa** as imagens Docker (no terminal):
	```
	docker-compose build
	```
4. **Inicie os serviços** (no terminal):
	```
	docker-compose up
	```

Os seguintes serviços devem ser iniciados:
- **API** disponível em: http://localhots:8000 e http://127.0.0.1:8000
- **Agente LLM** interativo rodando no terminal

Para encerrar pressione **Ctrl + C** e então digite (no terminal):
```
docker-compose down
```

### Exemplos de uso via ``curl``
Você pode consultar diretamente API com um comando `curl` após iniciar os serviços:
```
(Linux/MAC)
curl -X POST http://localhost:8000/fetch_oab \
  -H "Content-Type: application/json" \
  -d '{"name": "FULANO DE TAL", "uf": "SP"}'

(Windows)
curl -X POST http://localhost:8000/fetch_oab -H "Content-Type: application/json" -d "{\"name\": \"FULANO DE TAL\", \"uf\": \"SP\"}"
```
Também é possível iniciar a API de forma independente com ``python run_api.py`` (se todas as dependências de requirements.txt estiverem devidamente instaladas).

### Exemplos de Uso com o Agente LLM
Com a API rodando (via docker-compose ou run_api) você pode interagir com a LLM por mmeio do terminal, como no exemplo:
```
Usuário: Qual a situação do advogado João registrado em MS?
IA: O advogado João se encontra com status REGULAR, registrado na OAB-MS com o número 123456.
```
⚠️ Devido aos problemas de implementação anteriormente mencionados, o agente LLM pode apresentar inconsistências na utilização da ferramenta de busca.

### Exemplos de utilização

**Exemplo de utilização do agente LLM via terminal (retornou 404 por conta de erro na request):**
![[image(4).jpg]]

**Exemplo da API rodando via terminal:**
![[image(3).jpg]]

**Exemplo de requisição via terminal (Windows):**
![[image(2).jpg]]

**Exemplos de requisições para a API via Swagger UI:**
![[Pasted image 20250711222918.png]]
![[Pasted image 20250711223102.png]]