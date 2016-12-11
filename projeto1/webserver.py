#!/usr/bin/env python

"""
Created on Fri Nov 11 13:27:10 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

"""
TODO: 
    - need to verify checksum
    - need to verify if flags is 000 or 111
    - test everything
    - simplify the creation and connection of packets
    - simplify distributing commands through threads its too bloated
    - check if daemon still alright
    - alter how commands are being verified if they are valid, uptime for exampel
"""

#Funcao para verificar se tal comando foi requerido para ser executado no daemon        
from socket import *
from struct import *
#from queue import Queue
import threading
import cgi, cgitb
import string
import time

BUFF_SIZE = 1024
#string_lock = threading.Lock()
#q = Queue()
sentence = ''

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

#works dont ask me why or how
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
def send_command(socket, command, machine):
    #the following comments are flags for the pack and unpack proccess
    #we cut struct later we trim the code again
    header_version              =   2                                   #0
    header_ihdl                 =   8                                   #1
    header_tos                  =   0                                   #2
    header_total_length         =   0                                   #3
    header_identification       =   0                                   #4
    header_flags                =   000                                 #5
    header_fragment             =   0                                   #6
    header_ttl                  =   255                                 #7
    header_protocol             =   0 #adjust later                     #8
    header_checksum             =   0 #adjust later                     #9
    #header_sourceaddress        =   socket.getsockname()               #10
    header_sourceaddress        =   '0b01111111000000000000000000000001'  #Inteiro de 127.0.0.1   #10 2130706433
    #header_destinationaddress   =   socket.inet_aton ('127.0.0.1')     #11 - socket.inet_aton nao funciona
    header_destinationaddress   =   '0b01111111000000000000000000000001'                         #11 - '0b01111111000000000000000000000001' 
    header_options              =   0 #adjust later                     #12

    #Tem que ser uma struct binaria
    ip_header = pack('!BBBHHHHBBHLLL', header_version, header_ihdl, header_tos, header_total_length,
                header_identification, header_flags, header_fragment, header_ttl, header_protocol,
                header_checksum, header_sourceaddress, header_destinationaddress, header_options)
    
    socket.send(ip_header)
    socket.send(command.encode())
    
    packReceive = socket.recv(BUFF_SIZE)
    result = recv_all(socket)

    #append is faster than +=
    #with string_lock:
    sentence += machine
    sentence += ': '
    sentence += machine
    sentence += '<br>Command: '
    sentence += command
    sentence += '<br>Result: <br>'
    sentence += result
    sentence += '<br>'


####### MAIN ########

cgitb.enable()

# we fancy in html verification now
req = cgi.FieldStorage()     

commandMaq1 = verifyCheckboxHtml('1', req)
commandMaq2 = verifyCheckboxHtml('2', req)
commandMaq3 = verifyCheckboxHtml('3', req)

payloadMaq1 = ''
payloadMaq2 = ''
payloadMaq3 = ''
flagsHtml = ''

serverName = 'redesServer'

# se comando existe inicia thread
# precisa fazer verificacao de comandos que PRECISAM de flags e que nao
# tem como cortar isso?
if(commandMaq1):
    daemonCliente1 = socket(AF_INET, SOCK_STREAM)
    daemonCliente1.connect(("127.0.0.1", 9001))

    if(commandMaq1 & 1 == 1):
        flagsHtml = getFlagsHtml('1', 'ps', req)
        if (flagsHtml != None):
            payloadMaq1 = 'ps ' + flagsHtml
        else:
            payloadMaq1 = 'ps'
        '''t = threading.Thread(target=send_command, args=(daemonCliente1, payloadMaq1, 'Machine 1'))
        t.daemon = True
        t.start()'''
        send_command(daemonCliente1, payloadMaq1, 'Machine 1')

    if(commandMaq1 & 2 == 2):
        flagsHtml = getFlagsHtml('1', 'df', req)
        if (flagsHtml != None):
            payloadMaq1 = 'df ' + flagsHtml
        else:
            payloadMaq1 = 'df'
        send_command(daemonCliente1, payloadMaq1, 'Machine 1')

    if(commandMaq1 & 4 == 4):
        flagsHtml = getFlagsHtml('1', 'finger', req)
        if (flagsHtml != None):
            payloadMaq1 = 'finger ' + flagsHtml
        else:
            payloadMaq1 = 'finger'
        send_command(daemonCliente1, payloadMaq1, 'Machine 1')

    if(commandMaq1 & 8 == 8):
        flagsHtml = getFlagsHtml('1', 'uptime', req)
        if (flagsHtml != None):
            payloadMaq1 = 'uptime ' + flagsHtml
        else:
            payloadMaq1 = 'uptime'
        send_command(daemonCliente1, payloadMaq1, 'Machine 1')

if(commandMaq2):
    daemonCliente2 = socket(AF_INET, SOCK_STREAM)
    daemonCliente2.connect(("127.0.0.1", 9002))

    if(commandMaq2 & 1 == 1):
        flagsHtml = getFlagsHtml('2', 'ps', req)
        if (flagsHtml != None):
            payloadMaq2 = 'ps ' + flagsHtml
        else:
            payloadMaq2 = 'ps'
        '''t = threading.Thread(target=send_command, args=(daemonCliente2, payloadMaq2, 'Machine 2'))
        t.daemon = True
        t.start()'''
        send_command(daemonCliente2, payloadMaq2, 'Machine 2')

    if(commandMaq2 & 2 == 2):
        flagsHtml = getFlagsHtml('2', 'df', req)
        if (flagsHtml != None):
            payloadMaq2 = 'df ' + flagsHtml
        else:
            payloadMaq2 = 'df'
        send_command(daemonCliente2, payloadMaq2, 'Machine 2')

    if(commandMaq2 & 4 == 4):
        flagsHtml = getFlagsHtml('2', 'finger', req)
        if (flagsHtml != None):
            payloadMaq2 = 'finger ' + flagsHtml
        else:
            payloadMaq2 = 'finger'
        send_command(daemonCliente2, payloadMaq2, 'Machine 2')

    if(commandMaq2 & 8 == 8):
        flagsHtml = getFlagsHtml('2', 'uptime', req)
        if (flagsHtml != None):
            payloadMaq2 = 'uptime ' + flagsHtml
        else:
            payloadMaq2 = 'uptime'
        send_command(daemonCliente2, payloadMaq2, 'Machine 2')

if(commandMaq3):
    daemonCliente3 = socket(AF_INET, SOCK_STREAM)
    daemonCliente3.connect(("127.0.0.1", 9002))
    
    if(commandMaq3 & 1 == 1):
        flagsHtml = getFlagsHtml('3', 'ps', req)
        if (flagsHtml != None):
            payloadMaq3 = 'ps ' + flagsHtml
        else:
            payloadMaq3 = 'ps'
        '''t = threading.Thread(target=send_command, args=(daemonCliente3, payloadMaq3, 'Machine 3'))
        t.daemon = True
        t.start()'''
        send_command(daemonCliente3, payloadMaq3, 'Machine 3')

    if(commandMaq3 & 2 == 2):
        flagsHtml = getFlagsHtml('3', 'df', req)
        if (flagsHtml != None):
            payloadMaq3 = 'df ' + flagsHtml
        else:
            payloadMaq3 = 'df'
        send_command(daemonCliente3, payloadMaq3, 'Machine 3')

    if(commandMaq3 & 4 == 4):
        flagsHtml = getFlagsHtml('3', 'finger', req)
        if (flagsHtml != None):
            payloadMaq3 = 'finger ' + flagsHtml
        else:
            payloadMaq3 = 'finger'
        send_command(daemonCliente3, payloadMaq3, 'Machine 3')

    if(commandMaq3 & 8 == 8):
        flagsHtml = getFlagsHtml('3', 'uptime', req)
        if (flagsHtml != None):
            payloadMaq3 = 'uptime ' + flagsHtml
        else:
            payloadMaq3 = 'uptime'
        send_command(daemonCliente3, payloadMaq3, 'Machine 3')

#Eventos para enviar as mensagens
sentence = sentence.replace('\n', '<br />')

#Encerrando os sockets
if(commandMaq1):
    daemonCliente1.close()
if(commandMaq2):
    daemonCliente2.close()
if(commandMaq3):
    daemonCliente3.close()

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print(sentence)
