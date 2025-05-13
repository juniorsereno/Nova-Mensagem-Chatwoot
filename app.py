import os
      from flask import Flask, jsonify, request
      from flask_cors import CORS # Adicionado CORS
      import requests
      from dotenv import load_dotenv
      load_dotenv()
      app = Flask(__name__)
      CORS(app) # Habilita CORS para todas as rotas e origens por padrão
      CHATWOOT_API_KEY = os.getenv(\"CHATWOOT_API_KEY\")
      CHATWOOT_ACCOUNT_ID = os.getenv(\"CHATWOOT_ACCOUNT_ID\")
      CHATWOOT_BASE_URL = os.getenv(\"CHATWOOT_BASE_URL\", \"https://chat.unifyerp.com.br\")
      @app.route('/')
      def index():
          # Futuramente, pode servir o index.html daqui
          return \"Backend do Aplicativo de Mensagens Chatwoot está rodando!\"
      # Endpoint para listar caixas de entrada
      @app.route('/api/inboxes', methods=['GET'])
      def get_inboxes():
          if not CHATWOOT_API_KEY or not CHATWOOT_ACCOUNT_ID:
              return jsonify({\"error\": \"Variáveis de ambiente do Chatwoot não configuradas no servidor.\"}), 500
          headers = {
              \"api_access_token\": CHATWOOT_API_KEY
          }
          try:
              response = requests.get(
                  f\"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/inboxes\",
                  headers=headers
              )
              response.raise_for_status()  # Lança exceção para respostas de erro HTTP (4xx ou 5xx)
              
              raw_response_data = response.json()
              print(f\"Resposta crua da API Chatwoot para /inboxes: {raw_response_data}\") # Log para depuração
              print(f\"Tipo da resposta crua: {type(raw_response_data)}\")
              if isinstance(raw_response_data, list):
                  inboxes_data = raw_response_data
              elif isinstance(raw_response_data, dict) and 'payload' in raw_response_data and isinstance(raw_response_data['payload'], list):
                  inboxes_data = raw_response_data['payload']
              elif isinstance(raw_response_data, dict) and 'data' in raw_response_data and isinstance(raw_response_data['data'], list):
                  inboxes_data = raw_response_data['data']
              else:
                  print(f\"Formato inesperado da resposta da API Chatwoot para /inboxes: {raw_response_data}\")
                  return jsonify({\"error\": \"Formato inesperado da resposta da API do Chatwoot ao listar caixas de entrada.\"}), 502
              simplified_inboxes = []
              for inbox in inboxes_data:
                  if isinstance(inbox, dict):
                      simplified_inboxes.append({\"id\": inbox.get(\"id\"), \"name\": inbox.get(\"name\")})
                  else:
                      print(f\"Item inesperado na lista de inboxes (não é um dicionário): {inbox}\")
              
              return jsonify(simplified_inboxes)
          except requests.exceptions.HTTPError as e:
              print(f\"Erro HTTP ao buscar inboxes do Chatwoot: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}\")
              error_message = f\"Erro na API do Chatwoot ({e.response.status_code}): \"
              try:
                  error_details = e.response.json()
                  error_message += error_details.get(\"message\", e.response.text)
              except ValueError:
                  error_message += e.response.text
              return jsonify({\"error\": error_message}), e.response.status_code if e.response else 503
              
          except requests.exceptions.RequestException as e:
              print(f\"Erro de requisição ao buscar inboxes do Chatwoot: {e}\")
              return jsonify({\"error\": f\"Erro de comunicação ao tentar buscar caixas de entrada: {str(e)}\"}), 503
              
          except Exception as e:
              print(f\"Erro inesperado ao processar inboxes: {e}\")
              return jsonify({\"error\": \"Erro interno no servidor ao processar caixas de entrada.\"}), 500
      # Endpoint para enviar mensagem (criar contato, criar conversa, enviar mensagem)
      @app.route('/api/send-message', methods=['POST'])
      def send_message():
          if not CHATWOOT_API_KEY or not CHATWOOT_ACCOUNT_ID:
              return jsonify({\"error\": \"Variáveis de ambiente do Chatwoot não configuradas no servidor.\"}), 500
          data = request.json
          if not data:
              return jsonify({\"error\": \"Payload da requisição ausente.\"}), 400
          nome_completo = data.get('nomeCompleto')
          telefone = data.get('telefone')
          inbox_id = data.get('inboxId')
          mensagem_content = data.get('mensagem')
          if not all([nome_completo, telefone, inbox_id, mensagem_content]):
              return jsonify({\"error\": \"Dados incompletos no payload: nomeCompleto, telefone, inboxId e mensagem são obrigatórios.\"}), 400
          headers = {
              \"api_access_token\": CHATWOOT_API_KEY,
              \"Content-Type\": \"application/json\"
          }
          contact_id = None
          
          try:
              search_url = f\"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts/search\"
              search_params = {'q': telefone}
              search_response = requests.get(search_url, headers=headers, params=search_params)
              search_response.raise_for_status()
              search_results = search_response.json()
              
              existing_contacts = search_results.get('payload', [])
              
              if existing_contacts:
                  contact_id = existing_contacts[0].get('id')
                  print(f\"Contato encontrado: ID {contact_id}\")
              else:
                  create_contact_url = f\"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts\"
                  contact_payload = {
                      \"inbox_id\": int(inbox_id),
                      \"name\": nome_completo,
                      \"phone_number\": f\"+55{telefone}\",
                  }
                  print(f\"Criando contato com payload: {contact_payload}\")
                  response_contact = requests.post(create_contact_url, headers=headers, json=contact_payload)
                  response_contact.raise_for_status()
                  contact_data = response_contact.json()
                  contact_id = contact_data.get('id')
                  if not contact_id and 'payload' in contact_data and 'contact' in contact_data['payload']:
                       contact_id = contact_data['payload']['contact'].get('id')
                  if not contact_id and 'payload' in contact_data:
                       contact_id = contact_data['payload'].get('id')
                  if not contact_id:
                      print(f\"Erro: ID do contato não encontrado na resposta da criação: {contact_data}\")
                      return jsonify({\"error\": \"Falha ao obter ID do contato criado.\"}), 500
                  print(f\"Contato criado: ID {contact_id}\")
          except requests.exceptions.RequestException as e:
              print(f\"Erro ao criar/buscar contato: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}\")
              return jsonify({\"error\": f\"Erro na API do Chatwoot (contato): {str(e)}\"}), 503
          except Exception as e:
              print(f\"Erro inesperado (contato): {e}\")
              return jsonify({\"error\": \"Erro interno no servidor (contato).\"}), 500
          if not contact_id:
              return jsonify({\"error\": \"Não foi possível criar ou identificar o contato.\"}), 500
          try:
              create_conversation_url = f\"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations\"
              conversation_payload = {
                  \"inbox_id\": int(inbox_id),
                  \"contact_id\": contact_id,
                  \"message\": {
                      \"content\": mensagem_content,
                      \"message_type\": \"outgoing\"
                  },
                  \"status\": \"open\"
              }
              print(f\"Criando conversa com payload: {conversation_payload}\")
              response_conversation = requests.post(create_conversation_url, headers=headers, json=conversation_payload)
              response_conversation.raise_for_status()
              conversation_data = response_conversation.json()
              print(f\"Conversa criada: {conversation_data}\")
              
              return jsonify({
                  \"success\": True, 
                  \"message\": \"Mensagem enviada e conversa iniciada com sucesso!\",
                  \"contact_id\": contact_id,
                  \"conversation_id\": conversation_data.get(\"id\")
              }), 200
          except requests.exceptions.RequestException as e:
              print(f\"Erro ao criar conversa: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}\")
              return jsonify({\"error\": f\"Erro na API do Chatwoot (conversa): {str(e)}\"}), 503
          except Exception as e:
              print(f\"Erro inesperado (conversa): {e}\")
              return jsonify({\"error\": \"Erro interno no servidor (conversa).\"}), 500
      if __name__ == '__main__':
          app.run(debug=True, port=5001)
      
