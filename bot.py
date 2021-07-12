#biblioteca que possui o objeto Chatbot
from chatterbot import ChatBot
#SequenceMatcher compara pares de sequências de entrada 
from difflib import SequenceMatcher
#importa o método de seleção de resposta
from chatterbot.response_selection import get_most_frequent_response

# nível mínimo de similaridade da pergunta com as perguntas do banco
ACCEPTANCE = 0.95

# função que compara a pergunta do usuário com as perguntas do banco e retorna a similaridade, se houver
def comparate_messages(message, candidate_message):
    similarity = 0.0

    #se existir uma pergunta e uma resposta
    if message.text and candidate_message.text:
        message_text = message.text
        candidate_text = candidate_message.text

        #passamos as entradas para a função SequenceMatcher
        similarity = SequenceMatcher(
            None,
            message_text,
            candidate_text
        )
        #retorna a pontuação de similaridade entre as strings de entrada
        similarity = round(similarity.ratio(),2)

        #se a similaridade for menor que a definimos a pergunta não é a correta 
        if similarity < ACCEPTANCE:
            similarity = 0.0
        else:
            print("Mensagem do usuário:",message_text,", mensagem candidata:",candidate_message,", nível de confiança:", similarity)

    return similarity

# função que vai pegar a resposta correta
def select_response(message, list_response, storage=None):
    response = list_response[0]
    print("resposta escolhida:", response)

    return response

# função que vai executar o chatbot
def execute_bot():
    # criamos o chatbot
    bot = ChatBot("Robô do Brasileirão 2021",
        #se não quiser que o ser bot aprenda com as entradas, faça read_only=True,
        read_only=False,
        #definimos o método de comparação de mensagens, ou seja, a nossa função comparate-messages
        statement_comparison_function=comparate_messages,

        #definimos o método de seleção de resposta
        response_selection_method=get_most_frequent_response,
        #determinam a lógica de como o ChatterBot seleciona uma resposta
        logic_adapters=[
            {
                #seleciona uma resposta com base na correspondência mais conhecida
                #compara a entrada com as respostas conhecidas
                #depois de achar a correspondência com maior similaridade
                #chama a função select_response para pegar a resposta
                "import_path":"chatterbot.logic.BestMatch"
            }
        ],
        #database gerada pelo treinamento
        database_uri='sqlite:///db.sqlite3')

    while True:
        #recebe a pergunta do usuário
        chat_input = input("Digite alguma coisa...\n",)
        #chama a função para obter a resposta correta, caso exista
        response = bot.get_response(chat_input)

        #se a similaridade for maior que 0.95 imprime a resposta, se não for maior entra no else
        if response.confidence > 0.0:
            print(response.text)
        else:
            print("Ainda não sei como responder essa pergunta :(")
            print("Pergunte outra coisa...")

if __name__ == "__main__":
    execute_bot()
