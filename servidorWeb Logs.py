#Antonio Gean Rodrigues, Thiago Oliveira Cabral, Tiago Roberti Sampaio 
#201111722003, 201011722035, 201011722037

import socket, signal , threading as t, re, sys, os
from datetime import date
from time import gmtime, strftime

cfg = open('config.cfg','r')
config = cfg.read()
cfg.close()

import sys
sys.stderr = open('err.txt', 'w')

HOST = config.split('\n')[0].split(':')[1].split('#')[0].strip()
PORTA = int(config.split('\n')[1].split(':')[1].split('#')[0].strip())
OS = config.split('\n')[2].split(':')[1].split('#')[0].strip()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Socket do tipo TCP
servidor.bind((HOST, PORTA))

if OS == 'WINDOWS':
   clear = 'cls'
elif OS == 'LINUX':
   clear = 'clear'
elif OS == 'MAC':
   clear = 'clear'

#Variaveis necessarias para gerar o arquivo de LOG do servidor
today = date.today()
fileName = 'servidor.' + str(today) + strftime("-%H%M%S", gmtime())
logFile = open(fileName+'.log','w')
logFile.close()

def _print(fileName,log): #Imprime no arquivo de LOG
   print log
   logFile = open(fileName+'.log','a+')
   logFile.write(log+'\n')
   logFile.close()

   
def refreshPage(req_http,sizefile): #Atualiza a pagina HTML
    arq = req_http.split()[-1].split("/")[-1]
    url = req_http.split("\n")[5].split(": ")[1] #Extrai a url do cabecalho
    ctype = req_http.split("\n")[3].split(": ")[1] #Extrai o tipo do documento
    sourceIP = req_http.split("\n")[1].split(" ")[2] #Extrai o IP de origem
    f = open("index.html","r")
    html = f.read()
    html = html.split("\n") #Quebra o HTML por \n
    for i in range(0,len(html)): #Percorre todo o index.html
       if "svlog link" in html[i] : #Grava no html um hiperlink para o ultimo log gerado pelo servidor
          html[i] = "<!-- svlog link --><a href=\""+fileName+".log\">"
          continue
       if ("LastIMG" in html[i]): #Encontra o lugar para adicionar uma nova imagem
          novaIMG = "" #Define o conteudo HTML a ser inserido
          novaIMG = ("<!-- "+arq+" Start -->"
		           "<a href=\""+url+"\">"
						"<div class=\"home_post_cont post_box\">"
								"<div>"
									"<div class=\"home_post_content\">"
									"<img src=\"./serverFiles/"+arq+"\" style= \"z-index: -1; position: relative;font-size:12px;\" "
									"	title=\" <font size = 2>"
									            "<p>Source: "+sourceIP+" "
												"<p>Content-type: "+ctype+" "
												"<p>Content-length: "+`sizefile`+" bytes"												
												"</font>\" />"
									"""</div>
								</div>
						</div>
						</a>"""
						"<!-- "+arq+" End -->"
						"<!-- LastIMG -->")
          html[i] = novaIMG #Adiciona a nova imagem no HTML

    f.close()
    f = open("index.html","w")
    #_print(fileName, "****\tNOVO HTML****")
    for e in html: #Grava o index.html modificado
	   f.write(e+"\n")
    f.close()

def extrai_nome_doc(req): #Prototipo de funcao
	return req.split()[1][1:] #Extrai o nome do documento requisitado no cabecalho GET
	
def constroi_reposta(doc): #Constroi o cabecalho GET de resposta do servidor
   if doc == "": #Caso nao tenha sido requisito nenhum arquivo, redireciona o navegador par ao index
      try:
         _print(fileName, "Abrindo o index")
         f = open("index.html")
         dados = f.read()
         f.close()
         res = "HTTP/1.1 200 OK\r\n\r\n"+dados
      except:
         res = "HTTP/1.1 404 Not Found\r\n\r\n"
         return res
   else: #Retorna o documento requisitado
      try:
         _print(fileName, "Abrindo o documento requisitado"+doc)
         f = open(doc,"rb")
         dados = f.read()
         res = "HTTP/1.1 200 OK\r\n\r\n"+dados
      except:
         f = open('404.html','r')
         res = "HTTP/1.1 404 Not Found\r\n\r\n" + f.read()
         f.close()
      return res
   return res

def call_GET(pckt,conn): #Funcao que lida com GET
    doc = extrai_nome_doc(pckt) #Recebe o nome do documento requisitado
    _print(fileName, "Nome do arquivo: "+ doc)
    resposta = constroi_reposta(doc) #Recebe pacote de resposta
    conn.send(resposta) #Enviar a resposta do servidorWeb

def call_POST(pckt,conn): #Funcao que lida com POST
    count = 0
    tamanhoarq = len(pckt)
    nome = pckt.split()[-1].split("/")[-1] #Extrai o nome da imagem do cabecalho POST
    #nome = re.sub('%20',' ',nome)
    _print(fileName, nome)
    f = open("serverFiles/"+nome,"wb") #Prepara para escrever o arquivo recebido via POST
    f.write(pckt.split("\r\n\r\n")[1]) #Aqui e onde o upload comeca, o primeiro fragmento dos dados da imagem e inserido aqui
    while 1: #Loop para inserir os demais dados restantes da imagem
	   #_print(fileName, str(pckt.split()))
	   try:
	      pckt = conn.recv(1024) #Recebe um pacote com SOMENTE DADOS
	      if len(pckt) == 0: #Se for vazio, acabou os dados
	         f.close()
	         break
	      f.write(pckt) #Escreve os dados no arquivo
	      tamanhoarq = tamanhoarq + len(pckt) #Contabiliza o tamanho do arquivo
	      _print(fileName, "pckt"+str(count))
	   except:
	      break
	   count = count + 1
    return tamanhoarq

def novaConexao(conexao): #funcao principal, que sera chamada a cada nova conexao
	req_http = conexao.recv(1024)
	#_print(fileName, req_http)
	if "POST " in req_http: #Verifica se o que foi recebido se trata de um POST
	   _print(fileName, "***POST!")
	   sizefile = call_POST(req_http,conexao) #Trata o cabecalho e os dados recebidos
	   refreshPage(req_http,sizefile) #Atualiza a pagina HTML com a nova imagem
	elif "GET " in req_http: #Verifica se o que foi recebido se trata de um GET
	   _print(fileName, "***GET!")
	   call_GET(req_http,conexao) #Trata o cabecalho e os dados recebidos
	   
	else:
	   _print(fileName, "Que isso?\n") #O servidor recebeu algo inesperado
	   _print(fileName, req_http)
	conexao.close()

def handler(signum, frame):
   os.system(clear)
   _print(fileName, "Saindo...")
   sys.exit(0)
   
class MyThread(t.Thread): #Definicao de thread no contexto do servidor
   def __init__(self, c):
      t.Thread.__init__(self)
      self.conn = c
   def run(self):
      novaConexao(self.conn)

signal.signal(signal.SIGINT, handler)

os.system(clear)
while 1: #loop principal para manter o servidor ligado
   servidor.listen(5)
   servidor.settimeout(50)
   try:
      conexao, end_remoto = servidor.accept()
      conexao.setblocking(1)
      mt = MyThread(conexao) #Instancia uma nova thread
      mt.start() #Executa a thread
   except:
      os.system(clear)
      _print(fileName, "Socket timeout, reabrindo as conexoes")
