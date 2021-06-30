from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

#ver o nome da variavel
CONVERSATION_SETTINGS = [
  #endereço do inicio_conversa
  #"C:\\Users\\"
]

def inicializa():
  global bot
  global trainer

  bot = ChatBot("Robô do Brasileirão 2021")
  trainer = ListTrainer(bot)

def carrega_conversa():
  conversas = []

  #ver nomes dos arquivos
  for setting_file in CONVERSATION_SETTINGS:
    with open(setting_file, 'r', encoding = "utf-8") as file:
      conversas_configuradas = json.load(file)
      conversas.append(conversas_configuradas["conversas"])

      file.close()
  
  return conversas;

def treina_bot(conversas):
  global trainer

  for conversa in conversas:
    for message_response in conversa:
      messages = message_response["messages"]
      response = message_response["response"]

      print("Aqui estamos treinando o Robô para responder a:", messages, "'com a resposta'", response)

      for message in messages:
        trainer.train([message, response])

if __name__ == "__main__":
  inicializa()
  conversas = carrega_conversa()
  if conversas:
    treina_bot(conversas)
