# Resumo do Projeto: Aplicativo de Envio de Mensagens para Chatwoot

## Visão Geral
Este projeto visa desenvolver um aplicativo web que se integra à plataforma Chatwoot. O objetivo principal é fornecer uma interface para iniciar conversas com contatos (novos ou existentes) diretamente em caixas de entrada específicas do Chatwoot.

## Requisitos Chave
- Formulário web para coletar dados do remetente (Nome Completo, Telefone) e da mensagem.
- Campo de seleção para escolher a Caixa de Entrada (Inbox) de destino no Chatwoot, populado dinamicamente.
- Integração com a API do Chatwoot para:
    - Listar caixas de entrada.
    - Criar/identificar contatos.
    - Criar conversas.
    - Enviar mensagens.
- Backend desenvolvido em Python com Flask para gerenciar a lógica de negócios e a comunicação segura com a API do Chatwoot.
- Frontend desenvolvido com HTML, CSS e JavaScript.
- Aplicação empacotada em um container Docker para facilitar o deploy (ex: no Easypanel).
- Código versionado no GitHub.

## Entregáveis
- Código fonte do frontend.
- Código fonte do backend.
- Dockerfile.
- Documentação no Memory Bank.
