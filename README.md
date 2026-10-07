<h1><div align=center>SISTEMA WMS</div></h1>


# Sobre o Projeto

Esse projeto consiste em um sistema back-end **FastAPI** de um software de gerenciamento de estoque baseado em um contexto especialmente proximo de mercados de bairro e mercearias.

---

# Stack Tecnologica

![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white) ![Pydantic](https://img.shields.io/badge/pydantic-%23E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white) ![JWT](https://img.shields.io/badge/json%20web%20tokens-%23000000.svg?style=for-the-badge&logo=jsonwebtokens&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)


# Funcionalidades

## Estoque

O sistema contem todas as funcionalidades **CRUD** para gerenciamento de estoque e itens, sendo possivel:
* **cadastrar** itens e corredores do estoque
* **ver** informações sobre determinado item ou corredor
* **atualizar** informações dos corredores e itens
* **deletar** registros de corredores e itens
* **adcionar** registro de itens em um corredor

## Autenticação e Autorização

O sistema utiliza-se de autenticação por token **JWT** (JSON Web Token) para autenticação e um modelo **RBAC** (Roled-Base Acess Control) para autorização

o fluxo de autenticação ocorre da seguinte forma:

1. O usuario é cadastrado através do endpoint `/auth/signup`
2. O usuario realiza login através de `/auth/signin`
3. Após a autenticação a API gera um acess token JWT
4. O token deve ser enviado nas requisições que exigem autenticação através do header `Authorization` 

esse header deve ser enviado seguindo a seguinte estrutura:
```http
"Authorization": "Bearer {access_token}"
```

Certos endpoints requerem permissões associadas a cargos (`role`) especificos.

Por padrão o cargo de usuarios cadastrados por meio do endpoint `/auth/signup` é o de `user`.

O cadastro de usuarios com outros cargos é feito através do endpoint `/auth/admin/signup`, que requer permissões de administrador (`admin`)

## Administração de Usuarios

Usuarios podem ser **gerenciados** por administradores e outros usuarios autorizados apartir dos endpoints disponiveis em `/users/`

Sendo possivel:
* **visualizar** informações não sensiveis de usuarios apartir do **id de usuario**, mediante a permissão necessaria
* **editar** informações como nome e email
* **editar** cargo/atividade, mediante a permissão necessaria

Usuarios Comuns podem somente visualizar e alterar suas proprias informações, não podendo alterar seu cargo ou atividade da conta.

# Instalação e Configuração
## Pré Requisitos:
* **Python 3.x**
* **GIT**
## Clonando o repositorio
O primeiro passo para fazer a instalação é clonar o repositorio do Github apartir do comando a seguir:
```bash
git clone https://github.com/Gfgreghi/sistema_de_estoque/

```

## Criando um ambiente virtual
O passo seguinte é criar um ambiente virtual python, para isso é necessario executar o seguinte comando na pasta raiz do projeto:
```bash
python -m venv .venv
```
Logo após, para ativar o ambiente virtual deve rodar um dos comandos a seguir de acordo com o sistema operacional utilizado:

### Linux/MacOS
```bash
source .venv/bin/activate
```
### Windows
```bash
.\.venv\Scripts\activate
```
## Instalação das dependências
Com o ambiente virtual ativado, é necessario instalar as dependências do projeto apartir do arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```
## Configuração do Ambiente
O sistema utiliza variáveis de ambiente para configurar parâmetros relacionados à autenticação e ao banco de dados.

Crie um arquivo `.env` na raiz do projeto

Nele deve conter as seguintes variáveis:

```env
SECRET_KEY=sua_chave_secreta 
ALGORITHM=HS256 
ACCESS_TOKEN_EXPIRE_MINUTES=30 
DATABASE_URL=sqlite:///./banco.db
```

## Configuração do Banco de Dados
Agora é necessario executar a migração do banco de dados com:
```bash
alembic upgrade head
```
## Executando a aplicação
Por fim, execute a API usando o comando:
```bash
uvicorn app.main:app --reload
```
com isso, sera possível utilizar a API, apartir do caminho descrito na saida do terminal.

# Documentação da API

A API possui documentação interativa baseada em OpenAPI, disponibilizada pelo FastAPI.

A documentação pode ser acessada através de:

http://127.0.0.1:8000/docs

# Estrutura do projeto

```
app/
├── api/
│   ├── dependencies.py -> Funções de dependencia 
│   └── routes/ -> rotas de requisição da API
├── core/
│   ├── db.py -> configuração e criação da engine do banco de dados
│   ├── config.py -> configuração das variaveis de ambiente
│   └── security.py -> funções de segurança como JWT ou Hash de senha
├── crud/ -> operações de criação, consulta, atualização e remoção de dados
├── models/ -> modelos ORM utilizados pela aplicação
├── schemas/ -> schemas de entrada e saida
└── main.py -> inicialização da aplicação
```

# Proximos Passos

- [ ] Refactor com o objetivo de padronizar nomenclaturas de funções e variaveis.
- [ ] aplicar Containers no projeto utilizando Docker
- [ ] Tornar o projeto completamente assincrono