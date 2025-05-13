# Padrões de Sistema

## Arquitetura Geral
- **Cliente-Servidor**: O sistema segue um padrão cliente-servidor.
    - **Cliente (Frontend)**: Interface web (HTML, CSS, JavaScript) rodando no navegador do usuário. Responsável pela coleta de dados e apresentação.
    - **Servidor (Backend)**: Aplicação Python/Flask. Responsável pela lógica de negócios, validações e comunicação segura com serviços externos (API do Chatwoot).

## Fluxo de Dados Principal
1. Usuário interage com o Frontend.
2. Frontend envia requisições HTTP (AJAX/Fetch) para o Backend.
3. Backend processa a requisição:
    - Valida dados.
    - Interage com a API do Chatwoot (autenticado com API Key).
4. API do Chatwoot retorna dados para o Backend.
5. Backend formata e retorna a resposta para o Frontend.
6. Frontend atualiza a interface do usuário.

## Padrões de Comunicação
- **RESTful APIs**: O backend exporá endpoints RESTful para o frontend. A comunicação com a API do Chatwoot também é via REST.

## Segurança
- A API Key do Chatwoot é mantida exclusivamente no backend e não é exposta ao cliente.
- Considerar validação de entrada em ambos frontend e backend.

## Empacotamento e Deploy
- **Docker**: A aplicação completa (frontend e backend) será empacotada em uma imagem Docker.
    - O Dockerfile definirá o ambiente, dependências e como a aplicação é iniciada.
- **Easypanel**: Plataforma de destino para deploy (conforme mencionado pelo usuário).
