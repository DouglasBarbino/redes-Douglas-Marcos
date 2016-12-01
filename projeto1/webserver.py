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

BUFFER_SIZE = 1024

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
    header_options              =   flags                           #xs - x is the number of chars

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


    return

#Lista dos comandos
comandos = ['ps', 'df', 'finger', 'uptime']



# contador de maquinas para possivel threading
machines_to_use = 0
# string para comandos nas maquinas
maq1Command = ''
maq2Command = ''
maq3Command = ''

cgitb.enable()

#Pegando os dados da pagina HTML
# a gente vai precisar cortar isso dps

requisicoes = cgi.FieldStorage()     

# maquina 1
maq1CheckboxPS = requisicoes.getvalue('maq1_ps') # checkbox ps
maq1CommandPS = requisicoes.getvalue('maq1-ps') # textbox ps
if(maq1CheckboxPS and maq1CommandPS):
    maq1Command += maq1CheckboxPS + ' ' + maq1CommandPS

maq1CheckboxDF = requisicoes.getvalue('maq1_df')
maq1CommandDF = requisicoes.getvalue('maq1-df')
if(maq1CheckboxDF):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_df') 
    if(maq1CommandDF):
        maq1Command += ' ' + requisicoes.getvalue('maq1-df')

maq1CheckboxUP = requisicoes.getvalue('maq1_uptime')

maq1CheckboxFINGER = requisicoes.getvalue('maq1_finger')

# finger nao ta funcionando
# up tambem nao

# maquina 2
maq2CheckboxPS = requisicoes.getvalue('maq2_ps') # checkbox ps
maq2CommandPS = requisicoes.getvalue('maq2-ps') # textbox ps
if(maq2CheckboxPS and maq2CommandPS):
    maq2Command += maq2CheckboxPS + ' ' + maq2CommandPS

maq2CheckboxDF = requisicoes.getvalue('maq2_df')
maq2CommandDF = requisicoes.getvalue('maq2-df')
if(maq2CheckboxDF):
    if(maq2Command):
        maq2Command += ' && '
    maq2Command += requisicoes.getvalue('maq2_df') 
    if(maq2CommandDF):
        maq2Command += ' ' + requisicoes.getvalue('maq2-df')

maq2CheckboxUP = requisicoes.getvalue('maq2_uptime')

maq2CheckboxFINGER = requisicoes.getvalue('maq2_finger')

# maquina 3
maq3CheckboxPS = requisicoes.getvalue('maq3_ps') # checkbox ps
maq3CommandPS = requisicoes.getvalue('maq3-ps') # textbox ps
if(maq3CheckboxPS and maq3CommandPS):
    maq3Command += maq3CheckboxPS + ' ' + maq3CommandPS

maq3CheckboxDF = requisicoes.getvalue('maq3_df')
maq3CommandDF = requisicoes.getvalue('maq3-df')
if(maq3CheckboxDF):
    if(maq3Command):
        maq3Command += ' && '
    maq3Command += requisicoes.getvalue('maq3_df') 
    if(maq3CommandDF):
        maq3Command += ' ' + requisicoes.getvalue('maq3-df')

maq3CheckboxUP = requisicoes.getvalue('maq3_uptime')

maq3CheckboxFINGER = requisicoes.getvalue('maq3_finger')



serverName = 'redesServer'

#Criacao dos sockets
daemonCliente1 = socket(AF_INET, SOCK_STREAM)
daemonCliente1.connect(("127.0.0.1", 9001))
daemonCliente2 = socket(AF_INET, SOCK_STREAM)
daemonCliente2.connect(("127.0.0.1", 9002))
daemonCliente3 = socket(AF_INET, SOCK_STREAM)
daemonCliente3.connect(("127.0.0.1", 9003))

#Eventos para enviar as mensagens
sentence = ''
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
