# BudgetFlow Backend

## Introdução

O **BudgetFlow Backend** é a parte do servidor da aplicação BudgetFlow, responsável por gerenciar a lógica de negócios, autenticação de usuários, e operações de CRUD (Create, Read, Update, Delete) para receitas e despesas. Este backend foi desenvolvido utilizando Django, um framework web robusto e escalável.

## Funcionalidades Implementadas

### 1. Autenticação de Usuários
- **Verifica Autentificação**: retorna se um usário está autenticado ou não.
- **Registro de Usuários**: Permite que novos usuários se cadastrem no sistema fornecendo um nome de usuário, e-mail e senha.
- **Login**: Autentica usuários registrados, gerando um token de autenticação que é utilizado para acessar áreas protegidas da aplicação.
- **Logout**: Invalida o token de autenticação, deslogando o usuário do sistema.
- **Troca de Senha**: O usuário consegue fazer o pedido de troca de senha.

### 2. Gerenciamento de Receitas
- **Adicionar Receita**: Endpoint para adicionar novas receitas ao sistema. Os dados incluem descrição, valor, data e categoria.
- **Listar Receitas**: Endpoint para listar todas as receitas cadastradas pelo usuário autenticado.
- **Editar Receita**: Permite a edição de receitas existentes.
- **Remover Receita**: Endpoint para excluir receitas do sistema.

### 3. Gerenciamento de Despesas
- **Adicionar Despesa**: Endpoint para adicionar novas despesas ao sistema. Os dados incluem descrição, valor, data e categoria.
- **Listar Despesas**: Endpoint para listar todas as despesas cadastradas pelo usuário autenticado.
- **Editar Despesa**: Permite a edição de despesas existentes.
- **Remover Despesa**: Endpoint para excluir despesas do sistema.

### 4. Segurança e Autorização
- **Proteção de Endpoints**: Utilização de tokens de autenticação para proteger endpoints sensíveis, garantindo que apenas usuários autenticados possam acessar ou modificar dados.
- **Redirecionamento Seguro**: Usuários não autenticados são redirecionados para a página de login ao tentar acessar funcionalidades restritas.

## Tecnologias Utilizadas

- **Django**: Framework web utilizado para construir a aplicação backend.
- **Django REST Framework**: Biblioteca poderosa para a construção de APIs RESTful com Django.
- **SQLite**: Banco de dados utilizado para armazenar as informações de usuários, receitas e despesas.

## Como Executar o Projeto Localmente

1. Clone o repositório:
	```bash
	git clone https://github.com/thiagocamerato757/BudgetFlow_backend.git
	```

2. Navegue até o diretório do projeto:
	```bash
	cd BudgetFlow_backend
	```

3. Crie e ative um ambiente virtual:
	```bash
	python -m venv venv
	source venv/bin/activate
	```

4. Instale as dependências:
	```bash
	pip install -r requirements.txt
	```

5. Execute as migrações:
	```bash
	python manage.py migrate
	```

6. Inicie o servidor local:
	```bash
	python manage.py runserver
	```

7. Acesse o site em seu navegador:
	```bash
	http://127.0.0.1:8000
	```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.