# -*- coding: utf-8 -*-
#!/usr/bin/env python

print("Content=Type: text/html;charset=utf-8\r\n\r\n")
print("Hello World!")
"""
Created on Fri Nov 11 13:27:10 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

#Funcao para verificar se tal comando foi requerido para ser executado no daemon
def verificaComando (pagina, maquina, comando):
    #Verifica se o checkbox do comando foi ativado
    checkbox = maquina + '_' + comando
    if pagina.getvalue(checkbox):
        #Checkbox ativo, hora de ver se foi digitado algum argumento opcional
        parametros = maquina + '-' + comando
        argumentos = pagina.getvalue(parametros)
        #Verifica se foi digitado algum argumento
        if argumentos == None:
            return comando
        else:
            return (comando + ' ' + argumentos)
        
        
from socket import *
import cgi, cgitb

#Lista dos comandos
comandos = ['ps', 'df', 'finger', 'uptime']
    
cgitb.enable()
#Pegando os dados da pagina HTML
requisicoes = cgi.FieldStorage()

serverName = 'redesServer'

#Criacao dos sockets
daemonCliente1 = socket(AF_INET, SOCK_STREAM)
daemonCliente1.connect(("127.0.0.1", 9001))
daemonCliente2 = socket(AF_INET, SOCK_STREAM)
daemonCliente2.connect(("127.0.0.1", 9002))
daemonCliente3 = socket(AF_INET, SOCK_STREAM)
daemonCliente3.connect(("127.0.0.1", 9003))

#Eventos
for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq1', comando)
#Verifica se enviado algum comando para aquele daemon:
if sentence != None:
    daemonCliente1.send(sentence.encode())
    modifiedSentence = daemonCliente1.recv(1024)
    print ('From Server1:', modifiedSentence.decode())

for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq2', comando)
#Verifica se enviado algum comando para aquele daemon:
if sentence != None:
    daemonCliente2.send(sentence.encode())
    modifiedSentence = daemonCliente2.recv(1024)
    print ('From Server2:', modifiedSentence.decode())

for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq3', comando)
#Verifica se enviado algum comando para aquele daemon:
if sentence != None:
    daemonCliente3.send(sentence.encode())
    modifiedSentence = daemonCliente3.recv(1024)
    print ('From Server3:', modifiedSentence.decode())

#Encerrando os sockets
daemonCliente1.close()
daemonCliente2.close()
daemonCliente3.close()