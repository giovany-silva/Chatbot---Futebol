#Código que captura a tabela atualizada do Campeonato Brasileiro
import unicodedata
import requests
import json
from bs4 import BeautifulSoup
nomes = []

#Classe geradora de arquivos para treinamento
class Gera_Json:
    def criaJson(self,perguntas, respostas,nome):
      arquivo = open("conversations\\"+nome.strip()+".json", "w")
      saida = "{\n     \"conversations\":[\n"

      
      tam = len(perguntas) 
    
      for i in range(tam):
          saida += " "*15+"{\n"
          saida += " "* 20+"\"messages\": ["
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
          if( i != tam-1):
            saida += "              ,"
            saida += "\n"
          
      saida += "     "+"]\n"
      saida += "}"
      
      arquivo.write(saida)
      arquivo.close()
  

    def iniciar(self,perguntas,respostas):
          link = 'https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie'
          req = requests.get(link)

          lista = []

          content = req.content
          soup = BeautifulSoup(content, 'html.parser')
          
          estado_correspondente = {'SC': 'Santa Catarina','SP': 'Sao Paulo', 'PR': 'Parana', 'CE': 'Ceara', 'GO': 'Goias', 'MG': 'Minas Gerais', 'RJ': 'Rio de Janeiro', 'BA': 'Bahia', 'RS': 'Rio Grande do Sul', 'PE': 'Pernambuco', 'MT': 'Mato Grosso'}
          resultado = {'V': 'Venceu','E': 'Empatou', 'D':'Perdeu'}
          
          tabela = soup.find_all('tr',class_ = "expand-trigger")
          arquivo_json = open('conversations\\conversations','w')
          

          for dado in tabela:
            #Captura os dados
                  valores = dado.text.replace("\n","-").replace("-----","-").replace("----","-").replace("---","-").replace("--","-").split("-")
            #Deleção da primeira posição
                  del(valores[len(valores)-1])
                  del(valores[0])
            #armazenamento das variáveis
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

                  #Pega os nomes dos times e retira os acentos
                  time = unicodedata.normalize("NFD", time)
                  time = time.encode("ascii", "ignore")
                  time = time.decode("utf-8")
                  nomes.append(time)

                  #Criação das perguntas que serão adicionadas a lista de treinamento
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
                  perguntas.append(["Quantos cartoes amarelo o time "+time+ " possui ?","Qual o numero de cartoes amarelo que o time "+time+ " possui ?","O "+time+ " possui quantos cartoes amarelos ?"])
                  perguntas.append(["Quantos cartoes vermelho o time "+time+ " possui ?","Qual o numero de cartoes vermelho que o time "+time+ " possui ?","O "+time+ " possui quantos cartoes vermelhos ?"])
                  perguntas.append(["Quanto de aproveitamento o time "+ time+" possui ?", "Quantos porcento de aproveitamento o " + time+ " tem?", "Como estah o aproveitamento do " + time+ " ?"])
                  perguntas.append(["O que aconteceu com o time "+ time+" Na ultima rodada ?", "O " + time+ " foi bem na ultima rodada?", "Na ultima rodada o " + time+ " foi bem?"])
                  perguntas.append(["O que aconteceu com o time "+ time+" Na penultima rodada ?", "O " + time+ " foi bem na penultima rodada?", "Na penultima rodada o " + time+ " foi bem?"])
                  perguntas.append(["O que aconteceu com o time "+ time+" na antepenultima rodada ?", "O " + time+ " foi bem na antepenultima rodada?", "Na antepenultima rodada o " + time+ " foi bem?"])
    
                  #Criação das perguntas que serão adicionadas a lista de treinamento
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
                  
                                


                  
                
                  
                  
    def __init__(self):
      perguntas = []
      respostas = []
      
      #Para cada grupo de perguntas associe as respostas e crie um arquivo 
      self.iniciar(perguntas,respostas)
      self.criaJson(perguntas[0:15] , respostas[0:15],nomes[0])
      self.criaJson(perguntas[15:30] , respostas[15:30],nomes[1])
      self.criaJson(perguntas[30:45] , respostas[30:45],nomes[2])
      self.criaJson(perguntas[45:60] , respostas[45:60],nomes[3])
      self.criaJson(perguntas[60:75] , respostas[60:75],nomes[4])
      self.criaJson(perguntas[75:90] , respostas[75:90],nomes[5])
      self.criaJson(perguntas[90:105] , respostas[90:105],nomes[6])
      self.criaJson(perguntas[105:120] , respostas[105:120],nomes[7])
      self.criaJson(perguntas[120:135] , respostas[120:135],nomes[8])
      self.criaJson(perguntas[135:150] , respostas[135:150],nomes[9])
      self.criaJson(perguntas[150:165] , respostas[150:165],nomes[10])
      self.criaJson(perguntas[165:180] , respostas[165:180],nomes[11])
      self.criaJson(perguntas[180:195] , respostas[180:195],nomes[12])
      self.criaJson(perguntas[195:210] , respostas[195:210],nomes[13])
      self.criaJson(perguntas[210:225] , respostas[210:225],nomes[14])
      self.criaJson(perguntas[225:240] , respostas[225:240],nomes[15])
      self.criaJson(perguntas[240:255] , respostas[240:255],nomes[16])
      self.criaJson(perguntas[255:270] , respostas[255:270],nomes[17])
      self.criaJson(perguntas[270:285] , respostas[270:285],nomes[18])
      self.criaJson(perguntas[285:300] , respostas[285:300],nomes[19])



                  
      

