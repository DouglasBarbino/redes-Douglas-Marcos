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
import argparse
import string
import thread

BUFF_SIZE = 1024

def handler(clientsock, addr):
    while True:
        data = clientsock.recv(BUFF_SIZE)
        command = clientsock.recv(BUFF_SIZE).decode()
        #if data != '':
        if command != '':
            #header = unpack('!BBBHHHHBBHLLL', data)
            print('commands received: ' + command)
            executionOfCommands = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (data, err) = executionOfCommands.communicate()
            print('output generated: ' + data + '\r')
            clientsock.send(data)
            break
        else:
            break
            
    clientsock.close()


parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="comando para porta.")
args = parser.parse_args()

#Criacao do socket
daemonServer = socket(AF_INET,SOCK_STREAM)
daemonServer.bind(('',int(args.port)))
daemonServer.listen(1)

#Eventos
while True:
    clientsock, addr = daemonServer.accept()
    #thread.start_new_thread(handler, (clientsock, addr))
    handler(clientsock, addr)
    #Para pegar a execucao do comando
    #Fonte: https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    #talvez eu preferisse o pexpect

    #clienteSocket, endereco = daemonServer.accept()
     
    #sentence = clienteSocket.recv(1024).decode()
    #print(sentence)
    
    ##Para pegar a execucao do comando
    ##Fonte: https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    ##talvez eu preferisse o pexpect
    #execucao = subprocess.Popen(sentence, stdout=subprocess.PIPE, shell=True)
    #(output, err) = execucao.communicate()
    #Nao converte, pois a saida eh em bytes
    #clienteSocket.send(output)
    #clienteSocket.close()
