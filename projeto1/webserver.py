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

print("Content-Type: text/html;charset=utf-8\r\n\r\n")
print(modifiedSentence1)
print(modifiedSentence2)
print(modifiedSentence3)
