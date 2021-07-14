#importamos todos os componentes da biblioteca bot
from bot import * 
#importamos o Flask que cria aplicativos Web
from flask import Flask

VERSION = "1.0"


bot = ChatBot("Robô do Brasileirão 2021",
    #se não quiser que o ser bot aprenda com as entradas, faça read_only=True,

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
    ])
#criamos uma instância do Flask    
bot_service = Flask(__name__)

@bot_service.route("/version", methods=["GET"])
def get_version():
    return VERSION

@bot_service.route("/response/<message>", methods=["GET"])
def get_response(message):
    response = bot.get_response(message)
    if response.confidence > 0.0:
          return response.text
          
    return "Ainda não sei a resposta dessa pergunta, tente outra coisa!"

if __name__ == "__main__":
    bot_service.run()
