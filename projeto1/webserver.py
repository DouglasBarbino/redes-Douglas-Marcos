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

#Funcao de divisao do pacote
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

#Pegando os dados da pagina HTML
# a gente vai precisar cortar isso dps

requisicoes = cgi.FieldStorage()     

# maquina 1
maq1Checkbox = requisicoes.getvalue('maq1_ps') # checkbox ps
maq1Command = requisicoes.getvalue('maq1-ps') # textbox ps
if(maq1Checkbox and maq1Command):
    daemonCliente1 = socket(AF_INET, SOCK_STREAM)
    daemonCliente1.connect(("127.0.0.1", 9001))    
    thread.start_new_thread(send_command, (daemonCliente1, maq1Checkbox, maq1Command))

sentence += thread.start_new_thread(recv_all, (daemonCliente1))


maq1CheckboxDF = requisicoes.getvalue('maq1_df') # checkbox df
maq1CommandDF = requisicoes.getvalue('maq1-df') # textbox df
if(maq1CheckboxDF):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_df') 
    if(maq1CommandDF):
        maq1Command += ' ' + requisicoes.getvalue('maq1-df')

maq1CheckboxFINGER = requisicoes.getvalue('maq1_finger') # checkbox finger
maq1CommandFINGER = requisicoes.getvalue('maq1-finger') # textbox finger
if(maq1CheckboxFINGER):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_finger') 
    if(maq1CommandFINGER):
        maq1Command += ' ' + requisicoes.getvalue('maq1-finger')        
        
maq1CheckboxUPTIME = requisicoes.getvalue('maq1_uptime') # checkbox uptime
maq1CommandUPTIME = requisicoes.getvalue('maq1-uptime') # textbox uptime
if(maq1CheckboxUPTIME):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_uptime') 
    if(maq1CommandUPTIME):
        maq1Command += ' ' + requisicoes.getvalue('maq1-uptime')

#verify if machine 1 is resquisited by the page
requisitionMaq1 = (maq1CheckboxPS or maq1CheckboxUPTIME or maq1CheckboxFINGER or maq1CheckboxDF)

# maquina 2
maq2CheckboxPS = requisicoes.getvalue('maq2_ps') # checkbox ps
maq2CommandPS = requisicoes.getvalue('maq2-ps') # textbox ps
if(maq2CheckboxPS):
    maq2Command += requisicoes.getvalue('maq2_ps')
    if(maq2CommandPS):
        maq2Command += ' ' + requisicoes.getvalue('maq2-ps')

maq2CheckboxDF = requisicoes.getvalue('maq2_df') # checkbox df
maq2CommandDF = requisicoes.getvalue('maq2-df') #textbox df
if(maq2CheckboxDF):
    if(maq2Command):
        maq2Command += ' && '
    maq2Command += requisicoes.getvalue('maq2_df') 
    if(maq2CommandDF):
        maq2Command += ' ' + requisicoes.getvalue('maq2-df')
        
maq2CheckboxFINGER = requisicoes.getvalue('maq2_finger') # checkbox finger
maq2CommandFINGER = requisicoes.getvalue('maq2-finger') # textbox finger
if(maq2CheckboxFINGER):
    if(maq2Command):
        maq2Command += ' && '
    maq2Command += requisicoes.getvalue('maq2_finger') 
    if(maq2CommandFINGER):
        maq2Command += ' ' + requisicoes.getvalue('maq2-finger')  
        
maq2CheckboxUPTIME = requisicoes.getvalue('maq2_uptime') # checkbox uptime
maq2CommandUPTIME = requisicoes.getvalue('maq2-uptime') # textbox uptime
if(maq2CheckboxUPTIME):
    if(maq2Command):
        maq2Command += ' && '
    maq2Command += requisicoes.getvalue('maq2_uptime') 
    if(maq2CommandUPTIME):
        maq2Command += ' ' + requisicoes.getvalue('maq2-uptime')

#verify if machine 2 is resquisited by the page
requisitionMaq2 = (maq2CheckboxPS or maq2CheckboxUPTIME or maq2CheckboxFINGER or maq2CheckboxDF)

# maquina 3
maq3CheckboxPS = requisicoes.getvalue('maq3_ps') # checkbox ps
maq3CommandPS = requisicoes.getvalue('maq3-ps') # textbox ps
if(maq3CheckboxPS):
    maq3Command += requisicoes.getvalue('maq3_ps')
    if(maq3CommandPS):
        maq3Command += ' ' + requisicoes.getvalue('maq3-ps')

maq3CheckboxDF = requisicoes.getvalue('maq3_df') # checkbox df
maq3CommandDF = requisicoes.getvalue('maq3-df') # textbox df
if(maq3CheckboxDF):
    if(maq3Command):
        maq3Command += ' && '
    maq3Command += requisicoes.getvalue('maq3_df') 
    if(maq3CommandDF):
        maq3Command += ' ' + requisicoes.getvalue('maq3-df')
        
maq3CheckboxFINGER = requisicoes.getvalue('maq3_finger') # checkbox finger
maq3CommandFINGER = requisicoes.getvalue('maq3-finger') # textbox finger
if(maq3CheckboxFINGER):
    if(maq3Command):
        maq3Command += ' && '
    maq3Command += requisicoes.getvalue('maq3_finger') 
    if(maq3CommandFINGER):
        maq3Command += ' ' + requisicoes.getvalue('maq3-finger')  
        
maq3CheckboxUPTIME = requisicoes.getvalue('maq3_uptime') # checkbox uptime
maq3CommandUPTIME = requisicoes.getvalue('maq3-uptime') # textbox uptime
if(maq3CheckboxUPTIME):
    if(maq3Command):
        maq3Command += ' && '
    maq3Command += requisicoes.getvalue('maq3_uptime') 
    if(maq3CommandUPTIME):
        maq3Command += ' ' + requisicoes.getvalue('maq3-uptime')

#verify if machine 3 is resquisited by the page
requisitionMaq3 = (maq3CheckboxPS or maq3CheckboxUPTIME or maq3CheckboxFINGER or maq3CheckboxDF)

serverName = 'redesServer'



#Criacao dos sockets
#only if its needed
#if(requisitionMaq1):


if(requisitionMaq2):
    daemonCliente2 = socket(AF_INET, SOCK_STREAM)
    daemonCliente2.connect(("127.0.0.1", 9002))

if(requisitionMaq3):
    daemonCliente3 = socket(AF_INET, SOCK_STREAM)
    daemonCliente3.connect(("127.0.0.1", 9003))

send_command

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
