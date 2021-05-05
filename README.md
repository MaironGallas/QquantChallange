# Qquant Desafio

###### Desafio da empresa Qquant!

Siga estas etapas para instalar e executá-lo:
Clone o repositório

Mude para o diretório do aplicativo

Crie um .env e project.env com os exemplos em / contrib. Esse projeto utilizou o pipenv
para criar o ambiente e instalar as bibliotecas necessárias, assim basta seguir a seguinte etapa:

pip install pipenv

pipenv -sync

Execute a pilha de testes

Teste o aplicativo enviando a ele uma solicitação GET ou POST nas respectivas endpoints
http://127.0.0.1:8000/artigos/ e para realizar o CRUD http://127.0.0.1:8000/artigos/id

Seguem exemplo de uma entrada válida:

https://github.com/MrTango/rispy/blob/master/tests/data/example_full.ris