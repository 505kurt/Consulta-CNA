from agent.agent import build_agent


def run_agent():
    agent = build_agent(verbose=False)

    while True:
        question = input("Usuário: ")
        
        if question.lower() in ['sair', 'encerrar', 'exit', 'quit']:
            print("Encerrando agente de IA...")
            break

        try:
            answer = agent.invoke({"input": question})
            print(f"IA: {answer['output']}")
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == '__main__':
    run_agent()