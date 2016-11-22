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
import subprocess


#Pegar porta que foi passada como parametro
if (sys.argv[1] != None):
    #Para o caso de nao ser digitado o --port
    if (sys.argv[1] == "--port"):
        porta = sys.argv[2]
    else:
        porta = sys.argv[1]

    #Criacao do socket
    daemonServer = socket(AF_INET,SOCK_STREAM)
    daemonServer.bind(('',int(porta)))
    daemonServer.listen(1)
    
    #Eventos
    while True:
        clienteSocket, endereco = daemonServer.accept()
         
        sentence = clienteSocket.recv(1024).decode()
         
        #Para pegar a execucao do comando
        #Fonte: https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
        execucao = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
        (output, err) = execucao.communicate()
        print('Sentence received: ', output, '\r')
        #Nao converte, pois a saida eh em bytes
        clienteSocket.send(output)
        clienteSocket.close()
else:
    print("Eh necessario passar alguma porta como parametro!")
