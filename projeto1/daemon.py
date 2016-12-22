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
from struct import *
import subprocess
import argparse
import string
import thread
import time

BUFF_SIZE = 1024

def handler(clientsock, addr):
    while True:
        #Recebe o cabecalho e o comando que sera executado
        data = clientsock.recv(BUFF_SIZE)
        command = clientsock.recv(BUFF_SIZE).decode()
        #Descompactando o cabecalho
        header = unpack('!BBBHHHHBBHLLL', data)
        header_version              =   header[0]                           #0
        header_ihdl                 =   header[1]                           #1
        header_tos                  =   header[2]                           #2
        header_total_length         =   header[3]                           #3
        header_identification       =   header[4]                           #4
        header_flags                =   header[5]                           #5
        header_fragment             =   header[6]                           #6
        header_ttl                  =   header[7]                           #7
        header_protocol             =   header[8]                           #8
        header_checksum             =   header[9]                           #9
        header_sourceaddress        =   header[10]                          #10 
        header_destinationaddress   =   header[11]                          #11 - '0b01111111000000000000000000000001' 
        header_options              =   header[12]                          #12
            
        #Montagem do cabecalho (no caso apenas os campos que mudam,
        #o resto segue o mesmo valor que recebeu)
        header_flags                =   7                                   #5
        header_ttl                  =   header_ttl - 1                      #7
        
        #Tem que ser uma struct binaria
        daemon_header = pack('!BBBHHHHBBHLLL', header_version, header_ihdl, header_tos, header_total_length,
                        header_identification, header_flags, header_fragment, header_ttl, header_protocol,
                        header_checksum, header_sourceaddress, header_destinationaddress, header_options)
            
        clientsock.send(daemon_header)
        #Tempo para chegar o cabecalho no webserver
        time.sleep(1.0)
        if command != '':
            print('commands received: ' + command)
            executionOfCommands = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (data, err) = executionOfCommands.communicate()
            print('output generated: ' + data + '\r')
            
            clientsock.send(data)
            break
        else:
            break
            
    clientsock.close()

####### MAIN ########

#Recebendo os parametros
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
