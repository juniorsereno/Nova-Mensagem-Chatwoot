# Contexto do Produto: Aplicativo de Envio de Mensagens para Chatwoot

## Problema a Ser Resolvido
Facilitar e agilizar o processo de iniciar novas conversas no Chatwoot a partir de um sistema ou formulário externo, sem a necessidade de acessar diretamente a interface do Chatwoot para cada novo contato ou mensagem inicial. Isso é particularmente útil para cenários onde a captura de leads ou o primeiro contato ocorre fora do Chatwoot, mas a gestão da conversa subsequente deve ser centralizada nele.

## Objetivos do Produto
- Permitir que usuários (agentes ou sistemas automatizados) enviem mensagens para contatos (que podem ainda não existir no Chatwoot) através de uma interface simples.
- Garantir que as mensagens sejam corretamente direcionadas para a caixa de entrada (inbox) apropriada dentro do Chatwoot.
- Automatizar o processo de criação de contatos e conversas no Chatwoot com base nos dados fornecidos.
- Oferecer uma solução empacotável (Docker) para fácil implantação.

## Experiência do Usuário (Frontend)
- O usuário preenche um formulário web com:
    - Nome Completo.
    - Telefone (com DDI +55 pré-configurado).
    - Seleciona uma Caixa de Entrada de uma lista carregada do Chatwoot.
    - Escreve a mensagem.
- Ao submeter, o usuário recebe um feedback visual sobre o sucesso ou falha da operação.
