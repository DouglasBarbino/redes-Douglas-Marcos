#!/usr/bin/env python

"""
Created on Fri Nov 11 13:27:10 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

#Funcao para verificar se tal comando foi requerido para ser executado no daemon        
from socket import *
from threading import *
import cgi, cgitb
import string
import time
import struct
import thread

BUFFER_SIZE = 1024

# simplifying this html stuff (too long and too ugly)
def verifyCheckboxHtml(maqNumber, req):
    # using a binary flag because im fancy
    # 1 - ps | 2 - df | 4 - finger | 8 - uptime
    command = 0
    maqCheckbox = req.getvalue('maq' + maqNumber + '_ps')
    if(maqCheckbox):
        command = command | 1

    maqCheckbox = req.getvalue('maq' + maqNumber + '_df')
    if(maqCheckbox):
        command = command | 2

    maqCheckbox = req.getvalue('maq' + maqNumber + '_finger')
    if(maqCheckbox):
        command = command | 4

    maqCheckbox = req.getvalue('maq' + maqNumber + '_uptime')
    if(maqCheckbox):
        command = command | 8

    return command

def getFlagsHtml(maqNumber, command, req):
    return req.getvalue('maq' + maqNumber + '-' + command)

#works don't ask me why
def crcSixteen(buffer, crc = 0, poly = 0xa001):
    buffSize = len(buffer)
    
    for i in range(0, buffSize):
        char = ord(buffer[i])
        for unsiChar in range(0, 8):
            if(crc & 1) ^ (char & 1):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            char >>= 1

    return crc

# functions for network operations
def recv_all(socket, timeout=2):
    socket.setblocking(0)

    full_data = []
    data = ''
    begin=time.time()
    while True:
        #tenho dado, break depois do timeout
        if full_data and time.time()-begin > timeout:
            break
        #nao consegui dado, espero 2 vezes o timeout
        elif time.time()-begin > timeout * 2:
            break

        try:
            data = socket.recv(BUFFER_SIZE)
            if data:
                full_data.append(data)
                #timeout resetado
                begin = time.time()
            else:
                #dorme para mostrar atraso?
                time.sleep(0.1)
        except:
               pass
    return ''.join(full_data)

#threading send function
def send_command(socket, command, flags):
    #the following comments are flags for the pack and unpack proccess
    header_version              =   2                               #B - unsigned char
    header_ihdl                 =   8                               #B - unsigned char
    header_tos                  =   0                               #B - unsigned char
    header_total_length         =   0                               #H - unsigned short
    header_identification       =   0                               #H - unsigned short
    header_flags                =   000                             #H - unsigned short
    header_fragment             =   0                               #H - unsigned short
    header_ttl                  =   255                             #B - unsigned char
    header_protocol             =   command                         #B - unsigned char
    header_checksum             =   0 #adjust later                 #H - unsgined short
    header_sourceaddress        =   socket.getsockname()            #4s - 4 string chars
    header_destinationaddress   =   socket.inet_aton ('127.0.0.1')  #4s - 4 string chars
    header_options              =   command + " " + flags           #xs - x is the number of chars

    #remove duplicated spaces
    flags = " ".join(flags.split())
    #remove weird spaces
    flags = flags.strip()

    #get size of the amount of flags
    flags_pack = '' + len(flags)
    flags_pack = '!BBBHHHHBBH4s4s' + flags_pack + 's'

    ip_header = pack(flags_pack, header_version, header_ihdl, 
                header_tos, header_total_length, header_identification,
                header_flags, header_fragment, header_ttl, header_protocol,
                header_checksum, header_sourceaddress, header_destinationaddress,
                header_options, flags)

    socket.send(ip_header).encode()

    return

#Lista dos comandos
comandos = ['ps', 'df', 'finger', 'uptime']

# contador de maquinas para possivel threading
# machines_to_use = 0

# string que recebe as mensagens
sentence = ''

cgitb.enable()

# we fancy in html verification now

req = cgi.FieldStorage()     

commandMaq1 = verifyHtml('1', req)
commandMaq2 = verifyHtml('2', req)
commandMaq3 = verifyHtml('3', req)

payloadMaq1 = ''
payloadMaq2 = ''
payloadMaq3 = ''

serverName = 'redesServer'

# se comando existe inicia thread
# precisa fazer verificação de comandos que PRECISAM de flags e que não
if(commandMaq1):
    if(commandMaq1 & 1 == 1):
        payloadMaq1 = 'ps ' + getFlagsHtml('1', 'ps', req)
    # inicia thread
    if(commandMaq1 & 2 == 2):
        payloadMaq1 = 'ds ' + getFlagsHtml('1', 'df', req)
    if(commandMaq1 & 4 == 4):
        payloadMaq1 = 'finger ' + getFlagsHtml('1', 'finger', req)
    if(commandMaq1 & 8 == 8):
        payloadMaq1 = 'uptime ' + getFlagsHtml('1', 'uptime', req)


#Eventos para enviar as mensagens
modifiedSentence1 = 'Maquina 1:<br><br>'
if(maq1Command):
    daemonCliente1.send(maq1Command.encode())
    sentence = daemonCliente1.recv(1024)
    modifiedSentence1 += sentence.decode() + '<br><br>'

modifiedSentence2 = 'Maquina 2:<br><br>'
if(maq2Command):
    daemonCliente2.send(maq2Command.encode())
    sentence = daemonCliente2.recv(1024)
    modifiedSentence2 += sentence.decode() + '<br><br>'

modifiedSentence3 = 'Maquina 3:<br><br>'
if(maq3Command):
    daemonCliente3.send(maq3Command.encode())
    sentence = daemonCliente3.recv(1024)
    modifiedSentence3 += sentence.decode() + '<br><br>'

#Encerrando os sockets
daemonCliente1.close()
daemonCliente2.close()
daemonCliente3.close()

modifiedSentence1 = modifiedSentence1.replace('\n', '<br />')
modifiedSentence2 = modifiedSentence2.replace('\n', '<br />')
modifiedSentence3 = modifiedSentence3.replace('\n', '<br />')

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print(modifiedSentence1)
print(modifiedSentence2)
print(modifiedSentence3)
