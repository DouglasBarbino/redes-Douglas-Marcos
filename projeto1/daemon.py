# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on Wed Nov  2 11:58:50 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

import sys
from socket import *

#Pegar porta que foi passada como parametro
if (sys.argv[1] == "--port"):
    porta = sys.argv[2]

    #Criacao do socket
    daemonServer = socket(AF_INET,SOCK_STREAM)
    daemonServer.bind(('',int(porta)))
    daemonServer.listen(1)
    
    #Eventos
    while True:
         clienteSocket, endereco = daemonServer.accept()
         
         sentence = clienteSocket.recv(1024).decode()
         print('Sentence received: ',sentence)
         capitalizedSentence = sentence.upper()
         clienteSocket.send(capitalizedSentence.encode())
         clienteSocket.close()
else:
    print("Eh necessario passar alguma porta como parametro!")