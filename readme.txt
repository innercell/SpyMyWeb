
Para utilizar o script configure os parametros necessários no arquivo de configuração "config.cfg", após isto, execute o "servidorWeb Logs.py" e logo em seguida o "packetExtractor.py", para executar um teste do zero aconselha-se copiar o conteudo de default.html dentro de index.html


-"packetExtractor.py": Lê o arquivo pacotes.txt e extrai os pacotes referentes a imagens, e utilizando do Full Request URI e do urllib é efetuado o download da imagem. Após cada download, a imagem é aberta e enviada anexada a um cabeçalho POST.

-"servidorWeb Logs.py": Espera por requisições GET ou POST, sendo que nesta última, a imagem recebida será gravada com o nome original da url e a cada nova imagem recebida a página index.html é atualizada para exibi-la; e também um log é criado mostrando como foi o processo de recebimento dos pacotes.

