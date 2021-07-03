from chatterbot import ChatBot
from Gera_Json import Gera_Json
from chatterbot.trainers import ListTrainer
import json

CONVERSATION_SETTINGS=[
    "conversations\inicio_conversa.json",
    "conversations\conversations.json"]

def initialize():
    global bot
    global trainer

    gerador = Gera_Json()
    bot = ChatBot("Robô do Brasileirão 2021")
    trainer = ListTrainer(bot)

def load_conversations():
    conversations =[]

    for setting_file in CONVERSATION_SETTINGS:
        with open(setting_file, 'r',encoding="utf-8") as file:
            configured_conversations = json.load(file)
            conversations.append(configured_conversations["conversations"])

            file.close()
    

    return conversations;


def train_bot(conversations):
    global trainer

    for conversation in conversations:
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