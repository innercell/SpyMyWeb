#Antonio Gean Rodrigues, Thiago Oliveira Cabral, Tiago Roberti Sampaio 
#201111722003, 201011722035, 201011722037

import urllib
import socket
import os

#Definicao de variaveis e proxy

cfg = open('config.cfg','r')
config = cfg.read()
cfg.close()

HOST = config.split('\n')[0].split(':')[1].split('#')[0].strip()
PORTA = int(config.split('\n')[1].split(':')[1].split('#')[0].strip())
pacotes = config.split('\n')[3].split(':')[1].split('#')[0].strip()
proxy = config.split('\n')[4].split(':')[1].split('#')[0].strip()
usuario = config.split('\n')[5].split(':')[1].split('#')[0].strip()
senha = config.split('\n')[6].split(':')[1].split('#')[0].strip()

if proxy == 'true':
   os.environ['http_proxy'] = 'http://'+usuario+':'+senha+'@10.0.16.1:3128'

def enviaPacote(arq,ext,url,sourceIP):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um Socket do tipo TCP
   #Estabelece  conexao
   s.connect((HOST,PORTA))   
   ac = 0 #Acumulador para contar a qtde de pacotes recebidos
   pacote = montaPost(arq,ext,url,sourceIP) #Chama a funcao para montar o pacote seja POST ou GET
   
   acabou = 0 #Flag para controloar o fim dos pacotes
   while 1:
      try:
	     print "Enviando pacote n",ac
	     if len(pacote) < 1024: #Se o tamanho do pacote for menor que 1024 nao ha necessidade de dividi-lo
		    s.send(pacote) #Envia um pacote < que 1024 bytes
		    acabou = 1 #Alerta que este e o ultimo pacote
	     else:
	        packet = pacote[0:1024] #Le um pacote de tamanho 1024
	        if len(packet) == 0:
	           break
	        #print packet
	        s.send(packet) #Envia um pacote de 1024 bytes     
      except:
	     print "Ultimo pacote!"
      
      ac = ac + 1
      
      if acabou == 1:
	     #print "acabou os apcotes\n"
	     break
      try:
         pacote = pacote[1024:] #Remove os 1024 bytes ja enviados do pacote
      except:
         #print "fim de pacotes\n"
         break
#Fecha conexao
   s.close()

def montaPost(file,ext,url,sourceIP):
   #Define cabecalho POST
   header = "POST /index.html HTTP/1.1\r\nSource: "+sourceIP+"\r\nConnection: keep-alive\r\nContent-Type: image/"+ext[1:]+"\r\nFilename: "+file+"\r\nURL: "+url+"\r\n\r\n"
   f = open(file,"rb") #Abre o arquivo para agregar seu conteudo ao cabecalho   
   content = f.read() #Recebe todo o conteudo do arquivo
   f.close()
   lol = header + content #Pacote completo!
   return lol
   
def ExtractAndDownload():
   print "Extracting URLs from Packets...\n"
   f = open("pacotes.txt")
   dados = f.read()
   catchURL = 0 #Flag para controle de captura URL
   count = 0
   sourceIP = ""
   exts = ["jpg","jpeg","gif","png"] #Extensoes aceitas
   for line in dados.split("\n"): #Percorre linha a linha
      if ("Source: " in line) : #Caputura o IP de origem de quem fez a requisicao GET
         sourceIP = line[8:]
      if "Accept: image/" in line: #Alerta que uma imagem foi encontrada
         catchURL = 1
      elif ("Full request URI:" in line) & (catchURL == 1): #Captura a URL completa
	     print "\tDownloading URL n"+`count`+" ..."
	     ext = line[23:-1].split("/")[-1].split(".")[-1] #Captura a extensao da imagem
	     if ext not in exts:
		     print "Extensao nao aceita!"
		     continue
	     if len(ext) > 4 & len(ext) > 2:
		     print "Extensao nao aceita!"
		     continue
	     ext = "."+ext
	     urllib.urlretrieve(line[23:-1], "images/img"+`count`+ext) #Baixa a imagem pelo URL e a salva na pasta /images
	     print "\tDONE! ("+line[23:-1]+")\n"
	     print "\tUploading img"+`count`+ext+" to Web Server at "+HOST+":"+`PORTA`+" ..."
	     enviaPacote("images/img"+`count`+ext,ext,line[23:-1],sourceIP) #Efetua o upload da imagem para o servidor via POST
	     print "\tDONE!\n"
	     count = count + 1
	     catchURL = 0		 
ExtractAndDownload()
