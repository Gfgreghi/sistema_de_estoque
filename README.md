<h1><div align=center>SISTEMA WMS</div></h1>

---

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

Certos endpoints requerem certas permissões associadas a cargos (`role`) especificos.

Por padrão o cargo de usuarios cadastrados por meio do endpoint `/auth/signup` é o de `user`.

O cadastro de usuarios com outros cargos é feito através do endpoint `/auth/admin/signup`, que requer permissões de administrador (`admin`)

## Administração de Usuarios