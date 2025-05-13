# Contexto Ativo: Preparação para Deploy e Finalização da Documentação

## Foco Atual
- Preparação para deploy da aplicação.
- Finalização da documentação do estado atual do projeto no Memory Bank.

## Mudanças Recentes
- Funcionalidade principal do aplicativo (listar inboxes, criar contato, criar conversa, enviar mensagem) foi implementada.
- Backend Python/Flask e Frontend HTML/CSS/JS desenvolvidos.
- Aplicação testada localmente com sucesso.
- `Dockerfile` criado para empacotamento.
- Código fonte enviado manualmente pelo usuário para o GitHub: `https://github.com/juniorsereno/Nova-Mensagem-Chatwoot`.
- Memory Bank inicializado e atualizado para refletir o progresso.

## Próximos Passos Imediatos
1. Discutir e planejar o processo de deploy no Easypanel (ou plataforma Docker de escolha).
2. Construir a imagem Docker e testá-la em um ambiente isolado, se possível.
3. Realizar o deploy da aplicação.
4. Testar a aplicação no ambiente de deploy.

## Decisões e Considerações Ativas
- A API Key do Chatwoot (`ZZbnpRGZDmwamu9utec9ojDT`) e o Account ID (`1`) são gerenciados via arquivo `.env` localmente e precisarão ser configurados como variáveis de ambiente no ambiente de deploy.
- O campo de telefone no frontend já possui o DDI +55 e validação para números.
- A fonte do formulário foi ajustada para ser mais arredondada.
- O código fonte está versionado em: `https://github.com/juniorsereno/Nova-Mensagem-Chatwoot`.
