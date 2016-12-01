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
        data = clientsock.recv(BUFF_SIZE).decode()
        if data != '':
            print('commands received: ' + data)
            executionOfCommands = subprocess.Popen(data, stdout=subprocess.PIPE, shell=True)
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
    thread.start_new_thread(handler, (clientsock, addr))
    #Para pegar a execucao do comando
    #Fonte: https://www.cyberciti.biz/faq/python-execute-unix-linux-command-examples/
    #talvez eu preferisse o pexpect

