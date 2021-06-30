#Código que captura a tabela atualizada do Campeonato Brasileiro
import unicodedata
import requests
import json
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=4)


n_partidas = 0
estado_correspondente = {'SC': 'Santa Catarina','SP': 'Sao Paulo', 'PR': 'Parana', 'CE': 'Ceara', 'GO': 'Goias', 'MG': 'Minas Gerais', 'RJ': 'Rio de Janeiro', 'BA': 'Bahia', 'RS': 'Rio Grande do Sul', 'PE': 'Pernambuco', 'MT': 'Mato Grosso'}
resultado = {'V': 'Venceu','E': 'Empatou', 'D':'Perdeu'}

def criaJson(perguntas, respostas):
  
  arquivo = open("conversations.json", "w")
  saida = "{\n     \"results\":[\n"

  print(len(respostas))
  print(len(perguntas))
 
  for i in range(300):
      saida += " "*15+"{\n"
      saida += " "* 20+"\"message\": ["
      for j in range(3):
        saida += "\""+ perguntas[i][j]
        saida +="\""
        if(j!=2):
          saida += ", "
        else:
          saida +="],\n"
      saida += " "* 20+"\"response\": "
      saida += "\""+respostas[i] + "\"\n"
      saida += " "*15+"}\n"
      if( i != 299):
        saida += "              ,"
        saida += "\n"
      
  saida += "     "+"]\n"
  saida += "}"
  
  arquivo.write(saida)
 

def init(soup):
        lista_data = []
        lista_partida = []
        lista_estadio = []
        time_casa = None
        time_fora = None
        gols_time_casa = None
        gols_time_fora = None
        data = None
        estadio = None
        serie = None

        global n_partidas
        
        #tabela = soup.find_all('t',class_ = "expand-trigger")
        #tabela = soup.find_all('span',class_ = "hidden-xs")
        tabela = soup.find_all('tr',class_ = "expand-trigger")
        
        arquivo_json = open('informacoes_times','w')
        
        perguntas = []
        respostas = []

        for dado in tabela:
                valores = dado.text.replace("\n","-").replace("-----","-").replace("----","-").replace("---","-").replace("--","-").split("-")
                del(valores[len(valores)-1])
                del(valores[0])
                
                time = valores[2]
                estado = valores[3].replace(" ","")
                pontos = valores[4]
                jogos = valores[5]
                vitorias = valores[6]
                empates = valores[7]
                derrotas = valores[8]
                gols_pro = valores[9]
                gols_contra = valores[10]
                saldo = valores[11]
                cartoes_amarelos = valores[12]
                cartoes_vermelhos = valores[13]
                aproveitamento = valores[14]
                ultima_partida = resultado[valores[17]]
                penultima_partida = resultado[valores[16]]
                ante_penultima_partida = resultado[valores[15]]

                time = unicodedata.normalize("NFD", time)
                time = time.encode("ascii", "ignore")
                time = time.decode("utf-8")

                perguntas.append(["Qual eh o estado do "+ time+" ?","O "+ time+"eh de qual o estado ?",
                "De onde o "+ time+" eh ?"])    
                perguntas.append(["Quantos pontos o time "+ time+" possui ?","Qual a pontuacao do time "+ time+" ?","O "+ time+" possui quantos pontos?"])
                perguntas.append(["Quantos jogos o time "+ time+" fez ?","Qual o numero de jogos do time "+ time+" ?"," O "+ time+" fez quantos jogos ?"])
                perguntas.append(["Quantas vitorias o time "+ time+" possui ?","Qual o numero de vitorias do time "+ time+" ?","O "+ time+" possui quantas vitorias ?"])
                perguntas.append(["Quantos empates o time "+ time+" possui ?","Qual o numero de empates do time "+ time+" ?","O "+ time+" possui quantos empates ?"])
                perguntas.append(["Quantas derrotas o time "+ time+" possui ?","Qual o numero de derrotas do time "+ time+" ?","O "+ time+" possui quantas derrotas?"])
                perguntas.append(["Quantos gols o time "+ time+" fez ?","Qual numero de gols que o time "+ time+" fez ?"," O "+ time+" fez quantos gols ?"])
                perguntas.append(["Quantos gols o time "+ time+" tomou ?","Qual o numero de gols que o time "+ time+" tomou ?","O "+ time+" tomou quantos gols?"])
                perguntas.append(["Quantos saldo de gols o time "+time+ " possui ?","Qual o saldo de gols do time "+time+ " ?","O "+time+ " possui quantos gols de saldo ?"])
                perguntas.append(["Quantos cartoes amarelo o time "+time+ " possui ?","Qual o numero de cartoes amarelo que o time "+time+ " possui ?","O "+time+ " possui quantos cartoes amarelo ?"])
                perguntas.append(["Quantos cartoes vermelho o time "+time+ " possui ?","Qual o numero de cartoes vermelho que o time "+time+ " possui ?","O "+time+ " possui quantos cartoes vermelho ?"])
                perguntas.append(["Quanto de aproveitamento o time "+ time+" possui ?", "Quantos porcento de aproveitamento o " + time+ " tem?", "Como estah o aproveitamento do " + time+ " ?"])
                perguntas.append(["O que aconteceu com o time "+ time+" Na ultima rodada ?", "O " + time+ " foi bem na ultima rodada?", "Na ultima rodada o " + time+ " foi bem?"])
                perguntas.append(["O que aconteceu com o time "+ time+" Na penultima rodada ?", "O " + time+ " foi bem na penultima rodada?", "Na penultima rodada o " + time+ " foi bem?"])
                perguntas.append(["O que aconteceu com o time "+ time+" na antepenultima rodada ?", "O " + time+ " foi bem na antepenultima rodada?", "Na antepenultima rodada o " + time+ " foi bem?"])
  
                respostas.append("O "+ time +"eh de "+ estado_correspondente[estado])
                respostas.append("O "+ time +"possui "+ pontos+ " pontos")
                respostas.append("O "+ time +"fez "+ jogos+" jogos")
                respostas.append("O "+ time +"possui "+ vitorias+" vitorias")
                respostas.append("O "+ time +"possui "+ empates+" empates")
                respostas.append("O "+ time +"possui "+ derrotas+" derrotas")
                respostas.append("O "+ time +"fez "+ gols_pro+" gols")
                respostas.append("O "+ time +"tomou "+ gols_contra+" gols")
                respostas.append("O "+ time +"possui "+ saldo+" de saldo de gols")
                respostas.append("O "+ time +"possui "+ cartoes_amarelos+" cartoes amarelo")
                respostas.append("O "+ time +"possui "+ cartoes_vermelhos+" cartoes vermelho")
                respostas.append("O "+ time +"tem "+ aproveitamento+" % de aproveitamento no campeonato")
                respostas.append("Na ultima rodada o "+ time +" "+ ultima_partida)
                respostas.append("Na penultima rodada o "+ time +" "+ penultima_partida)
                respostas.append("Na antepenultima rodada o "+ time +" "+ ante_penultima_partida)
                
        criaJson(perguntas , respostas)                      


                
               
                
                
        
link = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2021'
req = requests.get(link)

lista = []

content = req.content
soup = BeautifulSoup(content, 'html.parser')
init(soup)
                
    

