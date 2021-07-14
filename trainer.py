#library que possui o objeto Chatbot
from chatterbot import ChatBot
#classe que possui função para geração dos aruivos para treinamento
from Gera_Json import Gera_Json
#library que possui o objeto para lista de treinamento
from chatterbot.trainers import ListTrainer
#library para conversao de file para json
import json

CONVERSATION_SETTINGS=[
    "conversations\\inicio_conversa.json",
    "conversations\\Red Bull Bragantino.json",
    "conversations\\Athletico Paranaense.json",
    "conversations\\Palmeiras.json",
    "conversations\\Fortaleza.json",
    "conversations\\Atletico Mineiro.json",
    "conversations\\Flamengo.json",
    "conversations\\Juventude.json",
    "conversations\\Bahia.json",
    "conversations\\Atletico.json",
    "conversations\\Corinthians.json",
    "conversations\\Ceara.json",
    "conversations\\Fluminense.json",
    "conversations\\Internacional.json",
    "conversations\\America.json",
    "conversations\\Sao Paulo.json",
    "conversations\\Cuiaba.json",
    "conversations\\Chapecoense.json",
    "conversations\\Sport.json",
    "conversations\\Santos.json",
    "conversations\\Gremio.json"]
# inicializa a instancia do robô e criação da lista para treino
def initialize():
    global bot
    global trainer

    gerador = Gera_Json()
    bot = ChatBot("Robô do Brasileirão 2021")
    trainer = ListTrainer(bot)
#Adiciona e treina os arqquivos json
def load_conversations():
    conversations =[]
#Para cada arquivo adicione na liista de treino
    for setting_file in CONVERSATION_SETTINGS:
        with open(setting_file, 'r',encoding="utf-8") as file:
            configured_conversations = json.load(file)
            conversations.append(configured_conversations["conversations"])

            file.close()
    

    return conversations

#Recebe a lista de treino e realiza o  treinamento sobre ela
def train_bot(conversations):
    global trainer

    for conversation in conversations: 
       #Para cada conjunto de pergunta e respota treine o chatbot
        for message_response in conversation:
            messages = message_response["messages"]
            response = message_response["response"]

            print("Treinando o robô para responder a:'",messages, "' Com a resposta'",response,"'")
            for message in messages:
                trainer.train([message,response])


if __name__ == "__main__":
    initialize()
    conversations = load_conversations()
    if conversations:
        train_bot(conversations)
