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
# string que recebe as mensagens
sentence = ''

cgitb.enable()

#Pegando os dados da pagina HTML
# a gente vai precisar cortar isso dps

requisicoes = cgi.FieldStorage()     

# maquina 1
maq1CheckboxPS = requisicoes.getvalue('maq1_ps') # checkbox ps
maq1CommandPS = requisicoes.getvalue('maq1-ps') # textbox ps
if(maq1CheckboxPS):
    maq1Command += requisicoes.getvalue('maq1_ps')
    if(maq1CommandPS):
        maq1Command += ' ' + requisicoes.getvalue('maq1-ps')

maq1CheckboxDF = requisicoes.getvalue('maq1_df') # checkbox df
maq1CommandDF = requisicoes.getvalue('maq1-df') # textbox df
if(maq1CheckboxDF):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_df') 
    if(maq1CommandDF):
        maq1Command += ' ' + requisicoes.getvalue('maq1-df')
        
maq1CheckboxUPTIME = requisicoes.getvalue('maq1_uptime') # checkbox uptime
maq1CommandUPTIME = requisicoes.getvalue('maq1-uptime') # textbox uptime
if(maq1CheckboxUPTIME):
    if(maq1Command):
        maq1Command += ' && '
    maq1Command += requisicoes.getvalue('maq1_uptime') 
    if(maq1CommandUPTIME):
        maq1Command += ' ' + requisicoes.getvalue('maq1-uptime')

# finger nao ta funcionando

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
        
maq2CheckboxUPTIME = requisicoes.getvalue('maq2_uptime') # checkbox uptime
maq2CommandUPTIME = requisicoes.getvalue('maq2-uptime') # textbox uptime
if(maq2CheckboxUPTIME):
    if(maq2Command):
        maq2Command += ' && '
    maq2Command += requisicoes.getvalue('maq2_uptime') 
    if(maq2CommandUPTIME):
        maq2Command += ' ' + requisicoes.getvalue('maq2-uptime')

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
        
maq3CheckboxUPTIME = requisicoes.getvalue('maq3_uptime') # checkbox uptime
maq3CommandUPTIME = requisicoes.getvalue('maq3-uptime') # textbox uptime
if(maq3CheckboxUPTIME):
    if(maq3Command):
        maq3Command += ' && '
    maq3Command += requisicoes.getvalue('maq3_uptime') 
    if(maq3CommandUPTIME):
        maq3Command += ' ' + requisicoes.getvalue('maq3-uptime')

serverName = 'redesServer'

#Criacao dos sockets
daemonCliente1 = socket(AF_INET, SOCK_STREAM)
daemonCliente1.connect(("127.0.0.1", 9001))
daemonCliente2 = socket(AF_INET, SOCK_STREAM)
daemonCliente2.connect(("127.0.0.1", 9002))
daemonCliente3 = socket(AF_INET, SOCK_STREAM)
daemonCliente3.connect(("127.0.0.1", 9003))

#Eventos para enviar as mensagens
modifiedSentence1 = 'Maquina 1:<br><br>'
if(maq1Command):
    daemonCliente1.send(maq1Command.encode())
    sentence = daemonCliente1.recv(2048)
    modifiedSentence1 += sentence.decode() + '<br><br>'

modifiedSentence2 = 'Maquina 2:<br><br>'
if(maq2Command):
    daemonCliente2.send(maq2Command.encode())
    sentence = daemonCliente2.recv(2048)
    modifiedSentence2 += sentence.decode() + '<br><br>'

modifiedSentence3 = 'Maquina 3:<br><br>'
if(maq3Command):
    daemonCliente3.send(maq3Command.encode())
    sentence = daemonCliente3.recv(2048)
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
