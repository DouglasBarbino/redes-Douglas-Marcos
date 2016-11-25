#!/usr/bin/env python

"""
Created on Fri Nov 11 13:27:10 2016
@author: Douglas Antonio Martins Barbino - 551511
         Marcos Vinicius Azevedo da Silva - 489808
"""

'''Codigo de criacao e encerramento dos sockets extraido dos
slides do capitulo 2 do Kurose'''

#Funcao para verificar se tal comando foi requerido para ser executado no daemon
def verificaComando (pagina, maquina, comando):
    #Verifica se o checkbox do comando foi ativado
    checkbox = maquina + '_' + comando
    if pagina.getvalue(checkbox):
        #Checkbox ativo, hora de ver se foi digitado algum argumento opcional
        parametros = maquina + '-' + comando
        argumentos = pagina.getvalue(parametros)
        #Verifica se foi digitado algum argumento
        if argumentos == None:
            return comando
        else:
            return (comando + ' ' + argumentos)
    else:
        return ''

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

cgitb.enable()

#Pegando os dados da pagina HTML
# a gente vai precisar cortar isso dps
# maquina 1
requisicoes = cgi.FieldStorage()     # checkbox ps
maq1CheckboxPS = requisicoes.getvalue('maq1_ps') 
maq1CommandPS = requisicoes.getvalue('maq1-ps')
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
maq2CheckboxPS = requisicoes.getvalue('maq2_ps')     # checkbox ps
if(maq2CheckboxPS == 'ps'):
    maq2CommandFlagPS = requisicoes.getvalue('maq2-ps') # textbox ps

maq2CheckboxDF = requisicoes.getvalue('maq2_df')       # checkbox df
if(maq2CheckboxDF == 'df'):
    maq2CommandFlagDF = requisicoes.getvalue('maq2-df') # textbox ps

maq2CheckboxF  = requisicoes.getvalue('maq2_finger') # checkbox finger
if(maq2CheckboxF == 'finger'):
    maq2CommandFlagF = requisicoes.getvalue('maq2-finger') # textbox ps

maq2CheckboxUP = requisicoes.getvalue('maq2_up')     # checkbox up
if(maq2CheckboxUP == 'up'):
    maq2CommandFlagUP = requisicoes.getvalue('maq2-up') # textbox ps

# maquina 3
maq3CheckboxPS = requisicoes.getvalue('maq3_ps')     # checkbox ps
if(maq3CheckboxPS == 'ps'):
    maq3CommandFlagPS = requisicoes.getvalue('maq3-ps') # textbox ps

maq3CheckboxDF = requisicoes.getvalue('maq3_df')       # checkbox df
if(maq3CheckboxDF == 'df'):
    maq3CommandFlagDF = requisicoes.getvalue('maq3-df') # textbox ps

maq3CheckboxF  = requisicoes.getvalue('maq3_finger') # checkbox finger
if(maq3CheckboxF == 'finger'):
    maq3CommandFlagF = requisicoes.getvalue('maq3-finger') # textbox ps

maq3CheckboxUP = requisicoes.getvalue('maq3_up')     # checkbox up
if(maq3CheckboxUP == 'up'):
    maq3CommandFlagUP = requisicoes.getvalue('maq3-up') # textbox ps



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

"""for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq1', comando)
    #Verifica se enviado algum comando para aquele daemon:
    if sentence != '':
        daemonCliente1.send(sentence.encode())
        sentence = daemonCliente1.recv(1024)
        modifiedSentence1 += sentence.decode() + '<br><br>' + maq1Command
"""
modifiedSentence2 = 'Maquina 2:<br><br>'
for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq2', comando)
    #Verifica se enviado algum comando para aquele daemon:
    if sentence != '':
        daemonCliente2.send(sentence.encode())
        sentence = daemonCliente2.recv(1024)
        modifiedSentence2 += sentence.decode() + '<br><br>'

modifiedSentence3 = 'Maquina 3:<br><br>'
for comando in comandos:   
    sentence += verificaComando (requisicoes, 'maq3', comando)
    #Verifica se enviado algum comando para aquele daemon:
    if sentence != '':
        daemonCliente3.send(sentence.encode())
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
