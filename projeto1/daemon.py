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
        
        '''print('0: ' + str(header_version) + '\r')
            print('1: ' + str(header_ihdl) + '\r')
            print('2: ' + str(header_tos) + '\r')
            print('3: ' + str(header_total_length) + '\r')
            print('4: ' + str(header_identification) + '\r')
            print('5: ' + str(header_flags) + '\r')
            print('6: ' + str(header_fragment) + '\r')
            print('7: ' + str(header_ttl) + '\r')
            print('8: ' + str(header_protocol) + '\r')
            print('9: ' + str(header_checksum) + '\r')
            print('10: ' + str(header_sourceaddress) + '\r')
            print('11: ' + str(header_destinationaddress) + '\r')
            print('12: ' + str(header_options) + '\r')'''
            
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
