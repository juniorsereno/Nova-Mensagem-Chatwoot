# Nova-Mensagem-Chatwoot

Aplicativo para enviar mensagens para contatos via Chatwoot.

## Visão Geral

Este projeto consiste em:
- Um **frontend** (HTML, CSS, JavaScript) que apresenta um formulário para o usuário inserir nome, telefone, selecionar uma caixa de entrada do Chatwoot e digitar uma mensagem.
- Um **backend** (Python/Flask) que recebe os dados do formulário, interage com a API do Chatwoot para:
    - Listar caixas de entrada.
    - Criar/identificar contatos.
    - Criar conversas.
    - Enviar a mensagem inicial.
- Um **Dockerfile** para empacotar a aplicação para deploy.

## Tecnologias
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask, Requests, python-dotenv, Flask-CORS
- API: Chatwoot
- Deploy: Docker

## Configuração Local
1.  Clone o repositório (após ser criado e os arquivos enviados).
2.  Crie e ative um ambiente virtual Python:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Crie um arquivo `.env` na raiz do projeto com suas credenciais do Chatwoot:
    ```env
    CHATWOOT_API_KEY="SUA_API_KEY_AQUI"
    CHATWOOT_ACCOUNT_ID="SEU_ACCOUNT_ID_AQUI"
    CHATWOOT_BASE_URL="URL_BASE_DA_SUA_INSTANCIA_CHATWOOT" # ex: https://chat.unifyerp.com.br
    ```
5.  Rode o servidor Flask:
    ```bash
    python app.py
    ```
    O backend estará rodando em `http://localhost:5001`.
6.  Abra o arquivo `index.html` no seu navegador.

## Build e Run com Docker
1.  Construa a imagem Docker:
    ```bash
    docker build -t nova-mensagem-chatwoot .
    ```
2.  Rode o container:
    ```bash
    docker run -p 5001:5001 -it --rm --name chatwoot-app nova-mensagem-chatwoot
    ```
    Acesse o `index.html` no navegador (que fará chamadas para `http://localhost:5001`).
