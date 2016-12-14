# redes-Douglas-Marcos
Repositório dos trabalhos da disciplina de Redes 2016/2 da UFSCar

No primeiro trabalho, o nosso objetivo era o seguinte (extraído da descrição do trabalho):
" A aplicação que será desenvolvida pelo grupo, irá permitir a um usuário realizar uma busca de resultados de comandos de linha, a partir de um conjunto de "máquinas" Linux, através de uma interface web. Especificamente, a aplicação começa apresentando ao usuário uma página web. Nessa página, o usuário poderá selecionar K máquinas de uma lista, e para cada máquina, selecionar um ou mais dos seguintes comandos: ps, df, finger e uptime. Uma vez que essa interface web (em python) receber estas instruções do browser do usuário, um aplicativo backend, também em python, irá se conectar (sequencialmente, ou em paralelo) a um conjunto de "daemons" rodando em cada uma das "máquinas" da lista. O programa backend então passará os comandos que precisam ser executados às respectivas máquinas remotas. Os "daemons" receberão o comando do programa backend e executarão localmente o comando correspondente. Eles então redirecionarão a sáıda desses comandos, e o backend juntará todas as respostas para criar uma página web de resultados."
Além disso, para padronizar todos os backends, foi criado um padrão de cabeçalhos parecido com o IPv4.

No código do webserver.py, o primeiro passo foi permitir que fosse criada uma nova página html como resposta e também conseguirmos pegar os dados submetidos da página HTML os estão os comandos, feito tudo isso por meio das funções cgitb.enable() e cgi.FieldStorage().

Após isso, o programa chama a função verifyCheckboxHtml, onde se verifica quais checkboxs da página HTML foram marcados. Ao encontrar uma seleção, é modificado um bit da váriavel command, sendo o bit 1 destinado para o comando ps, o bit 2 destinado para o df, o bit 3 para o finger e o 4º bit é destinado para o uptime.

Passada essa função, é verificado quais checkboxs de determinada máquina foram marcado por meio da variavel commandMaqX (preenchida pelo retorno da função verifyCheckboxHtml), sendo X o número da máquina. Se na máquina avaliada não foi marcado nenhum checkbox é verificado a próxima máquina, caso contrário se inicia a conexão do socket daquela máquina e se busca de qual (ou quais) comandos o checkbox foi marcado, verificando por meio de um comando lógico "and" quais bits estão ativos.

Ao encontrar um comando que deve ser executado, a execução vai para a função send_command, sendo criado o cabeçalho da mensagem e enviando para o daemon, enviando também o comando que deve ser executado. Para aguardar a resposta dele, o webserver vai para a função recv_all, onde espera um certo período de tempo até que ele receba a resposta.

Com o resultado da execução do daemon, é montada a sentença que será impressa na página HTML de resposta, sendo que após percorrer todas as máquinas são fechadas as conexões com os daemons e se imprime na tela a nova página.

No daemon.py, são aguardadas duas mensagens: A primeira contendo o cabeçalho e a segunda contendo o comando que deve ser executado. Após descompactar todo o cabeçalho, é feita a execução do comando por meio da função subprocess.Popen(command, stdout=subprocess.PIPE, shell=True), armazenando o que foi retornado pelo comando e enviando para o webserver esse resultado.
