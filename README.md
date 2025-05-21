# Formativa

Esse é o back-end de um projeto que consiste no gerenciamento de um sistema escolar, ele também contará com um front-end para uma visualização mais amigável e dinâmica, é possível gerenciar usuários, disciplinas, salas e realizar reservas.

### O que foi utilizado?
* Django Restframework
* Autenticação com simple JWT

### O que é preciso para vizualizar o projeto:

#### Antes de qualquer passo é necessário ter:
* python instalado na máquina
* configuração para usar pip
* workbench instalado na máquina

1. Clonar o repositório
```
git clone https://github.com/leticiaa-santos/formativa_back.git
```

2. Acessar o projeto e criar um ambiente virtual
```
cd formativa_back
py -m venv .env
.env\Scripts\activate
```

3. Instalar as dependências do projeto
```
pip install -r requirements.txt
```

4. Banco de dados
O banco que está configurado é mysql, com o nome cadastro e para que funcione precisa ser criado no workbench
Para rodar o projeto e ser possível salvar as alterações é preciso realizar as migrações depois do arquivo do banco criado
```
py manage.py makemigrations
py manage.py migrate
```

5. Agora o projeto está pronto para ser iniciado
```
py manage.py runserver
```

Agora já é possível visulizar o back-end do projeto

É possível consultar a documentação feita no Postman através desse link:
https://documenter.getpostman.com/view/43171594/2sB2qZEN5D
