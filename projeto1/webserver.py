# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 13:27:10 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

from socket import *

serverName = 'redesServer'

#Criacao dos sockets
daemonCliente1 = socket(AF_INET, SOCK_STREAM)
daemonCliente1.connect(("127.0.0.1", 9001))
daemonCliente2 = socket(AF_INET, SOCK_STREAM)
daemonCliente2.connect(("127.0.0.1", 9002))
daemonCliente3 = socket(AF_INET, SOCK_STREAM)
daemonCliente3.connect(("127.0.0.1", 9003))

#Eventos
sentence = input('Input lowercase sentence:')
daemonCliente1.send(sentence.encode())
modifiedSentence = daemonCliente1.recv(1024)
print ('From Server1:', modifiedSentence.decode())

sentence = input('Input lowercase sentence:')
daemonCliente2.send(sentence.encode())
modifiedSentence = daemonCliente2.recv(1024)
print ('From Server2:', modifiedSentence.decode())

sentence = input('Input lowercase sentence:')
daemonCliente3.send(sentence.encode())
modifiedSentence = daemonCliente3.recv(1024)
print ('From Server3:', modifiedSentence.decode())

#Encerrando os sockets
daemonCliente1.close()
daemonCliente2.close()
daemonCliente3.close()