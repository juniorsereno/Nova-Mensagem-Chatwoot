import os
from flask import Flask, jsonify, request, render_template # Adicionado render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

# Configurar pastas de templates e estáticos. Flask procura por 'templates' e 'static' por padrão.
# Se os nomes das pastas fossem diferentes, você especificaria aqui:
# app = Flask(__name__, template_folder='meus_templates', static_folder='meus_estaticos')
app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas e origens por padrão

CHATWOOT_API_KEY = os.getenv("CHATWOOT_API_KEY")
CHATWOOT_ACCOUNT_ID = os.getenv("CHATWOOT_ACCOUNT_ID")
CHATWOOT_BASE_URL = os.getenv("CHATWOOT_BASE_URL", "https://chat.unifyerp.com.br")

# A rota raiz '/' não é mais necessária aqui, será servida pelo Nginx (frontend)
# @app.route('/')
# def index():
#     return render_template('index.html')

# Endpoint para listar caixas de entrada
@app.route('/api/inboxes', methods=['GET'])
def get_inboxes():
    if not CHATWOOT_API_KEY or not CHATWOOT_ACCOUNT_ID:
        return jsonify({"error": "Variáveis de ambiente do Chatwoot não configuradas no servidor."}), 500

    headers = {
        "api_access_token": CHATWOOT_API_KEY
    }
    try:
        response = requests.get(
            f"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/inboxes",
            headers=headers
        )
        response.raise_for_status()  # Lança exceção para respostas de erro HTTP (4xx ou 5xx)
        
        raw_response_data = response.json()
        print(f"Resposta crua da API Chatwoot para /inboxes: {raw_response_data}") # Log para depuração
        print(f"Tipo da resposta crua: {type(raw_response_data)}")

        # A documentação da API sugere que a resposta é um array direto de inboxes.
        # Algumas APIs aninham a lista sob uma chave 'data' ou 'payload'.
        # Vamos verificar se é uma lista diretamente, ou se está aninhada.
        if isinstance(raw_response_data, list):
            inboxes_data = raw_response_data
        elif isinstance(raw_response_data, dict) and 'payload' in raw_response_data and isinstance(raw_response_data['payload'], list):
            inboxes_data = raw_response_data['payload']
        elif isinstance(raw_response_data, dict) and 'data' in raw_response_data and isinstance(raw_response_data['data'], list):
            inboxes_data = raw_response_data['data']
        else:
            # Se não for uma lista nem um dict com 'payload' ou 'data' contendo uma lista, algo está errado.
            print(f"Formato inesperado da resposta da API Chatwoot para /inboxes: {raw_response_data}")
            return jsonify({"error": "Formato inesperado da resposta da API do Chatwoot ao listar caixas de entrada."}), 502

        simplified_inboxes = []
        for inbox in inboxes_data:
            if isinstance(inbox, dict): # Garante que cada item é um dicionário
                simplified_inboxes.append({"id": inbox.get("id"), "name": inbox.get("name")})
            else:
                print(f"Item inesperado na lista de inboxes (não é um dicionário): {inbox}")
                # Pode optar por pular este item ou retornar um erro
        
        return jsonify(simplified_inboxes)

    except requests.exceptions.HTTPError as e:
        # Erros HTTP específicos (4xx, 5xx da API do Chatwoot)
        print(f"Erro HTTP ao buscar inboxes do Chatwoot: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}")
        error_message = f"Erro na API do Chatwoot ({e.response.status_code}): "
        try:
            error_details = e.response.json()
            error_message += error_details.get("message", e.response.text)
        except ValueError: # Em caso de resposta não-JSON
            error_message += e.response.text
        return jsonify({"error": error_message}), e.response.status_code if e.response else 503
        
    except requests.exceptions.RequestException as e:
        # Outros erros de requisição (conexão, timeout, etc.)
        print(f"Erro de requisição ao buscar inboxes do Chatwoot: {e}")
        return jsonify({"error": f"Erro de comunicação ao tentar buscar caixas de entrada: {str(e)}"}), 503
        
    except Exception as e:
        # Outros erros inesperados (ex: erro de parsing do JSON se a resposta não for JSON válido)
        print(f"Erro inesperado ao processar inboxes: {e}")
        return jsonify({"error": "Erro interno no servidor ao processar caixas de entrada."}), 500

# Endpoint para enviar mensagem (criar contato, criar conversa, enviar mensagem)
@app.route('/api/send-message', methods=['POST'])
def send_message():
    if not CHATWOOT_API_KEY or not CHATWOOT_ACCOUNT_ID:
        return jsonify({"error": "Variáveis de ambiente do Chatwoot não configuradas no servidor."}), 500

    data = request.json
    if not data:
        return jsonify({"error": "Payload da requisição ausente."}), 400

    nome_completo = data.get('nomeCompleto')
    telefone = data.get('telefone') # Frontend deve enviar sem o +55, backend pode adicionar se necessário pela API
    inbox_id = data.get('inboxId')
    mensagem_content = data.get('mensagem')

    if not all([nome_completo, telefone, inbox_id, mensagem_content]):
        return jsonify({"error": "Dados incompletos no payload: nomeCompleto, telefone, inboxId e mensagem são obrigatórios."}), 400

    headers = {
        "api_access_token": CHATWOOT_API_KEY,
        "Content-Type": "application/json"
    }

    contact_id = None

    # Passo 1: Criar/Identificar Contato
    # Usaremos o telefone como identificador único para buscar ou criar o contato.
    # A API de busca de contatos é GET /api/v1/accounts/{account_id}/contacts/search?q={telefone}
    # Se não encontrado, criar com POST /api/v1/accounts/{account_id}/contacts
    
    try:
        # Tentar buscar contato existente pelo telefone
        search_url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts/search"
        search_params = {'q': telefone}
        search_response = requests.get(search_url, headers=headers, params=search_params)
        search_response.raise_for_status()
        search_results = search_response.json()
        
        # A API de search retorna um objeto com uma chave 'payload' que é uma lista de contatos
        existing_contacts = search_results.get('payload', [])
        
        if existing_contacts:
            # Usar o primeiro contato encontrado com o telefone
            # Idealmente, a API deveria permitir uma busca mais precisa ou ter um campo 'identifier' mais robusto
            contact_id = existing_contacts[0].get('id')
            # Poderíamos atualizar o contato se o nome for diferente, mas vamos manter simples por ora.
            print(f"Contato encontrado: ID {contact_id}")
        else:
            # Contato não encontrado, criar um novo
            create_contact_url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/contacts"
            contact_payload = {
                "inbox_id": int(inbox_id), # API espera inbox_id para associar o contato
                "name": nome_completo,
                "phone_number": f"+55{telefone}", # Adicionando DDI para o Chatwoot
                # "identifier": telefone # Pode ser útil para buscas futuras
            }
            print(f"Criando contato com payload: {contact_payload}")
            response_contact = requests.post(create_contact_url, headers=headers, json=contact_payload)
            response_contact.raise_for_status()
            contact_data = response_contact.json()
            # A resposta de criação de contato pode estar aninhada, ex: contact_data.get('payload', {}).get('contact', {}).get('id')
            # Ou diretamente contact_data.get('id') ou contact_data.get('payload', {}).get('id')
            # Verificando a estrutura de 'extended_contact' e 'contact_create' response
            # A resposta de POST /contacts parece ser um objeto 'extended_contact' que tem 'id' no nível raiz do 'payload.contact' ou similar.
            # Vamos assumir que 'payload' contém o contato e o contato tem 'id'.
            # Exemplo de estrutura de resposta para POST /contacts: { "payload": { "contact": { "id": 123, ... } } }
            # Ou, conforme a definição de extended_contact, pode ser { "id": ..., "payload": { "contact": { ... } } }
            # A definição de `contactCreate` operationId diz que retorna `extended_contact`.
            # `extended_contact` tem `id` no nível superior.
            contact_id = contact_data.get('id')
            if not contact_id and 'payload' in contact_data and 'contact' in contact_data['payload']: # Fallback para estrutura aninhada
                 contact_id = contact_data['payload']['contact'].get('id')
            if not contact_id and 'payload' in contact_data: # Outro fallback
                 contact_id = contact_data['payload'].get('id')

            if not contact_id:
                print(f"Erro: ID do contato não encontrado na resposta da criação: {contact_data}")
                return jsonify({"error": "Falha ao obter ID do contato criado."}), 500
            print(f"Contato criado: ID {contact_id}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar/buscar contato: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}")
        return jsonify({"error": f"Erro na API do Chatwoot (contato): {str(e)}"}), 503
    except Exception as e:
        print(f"Erro inesperado (contato): {e}")
        return jsonify({"error": "Erro interno no servidor (contato)."}), 500

    if not contact_id:
        return jsonify({"error": "Não foi possível criar ou identificar o contato."}), 500

    # Passo 2: Criar Conversa com Mensagem Inicial
    try:
        create_conversation_url = f"{CHATWOOT_BASE_URL}/api/v1/accounts/{CHATWOOT_ACCOUNT_ID}/conversations"
        conversation_payload = {
            "inbox_id": int(inbox_id),
            "contact_id": contact_id,
            # "source_id": f"+55{telefone}", # Usar contact_id é mais robusto
            "message": {
                "content": mensagem_content,
                "message_type": "outgoing" # Mensagem enviada do "app" para o contato
            },
            "status": "open"
        }
        print(f"Criando conversa com payload: {conversation_payload}")
        response_conversation = requests.post(create_conversation_url, headers=headers, json=conversation_payload)
        response_conversation.raise_for_status()
        conversation_data = response_conversation.json()
        print(f"Conversa criada: {conversation_data}")
        
        # A resposta de 'newConversation' é um objeto com id, account_id, inbox_id
        return jsonify({
            "success": True, 
            "message": "Mensagem enviada e conversa iniciada com sucesso!",
            "contact_id": contact_id,
            "conversation_id": conversation_data.get("id")
        }), 200

    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar conversa: {e}. Resposta: {e.response.text if e.response else 'Sem resposta'}")
        return jsonify({"error": f"Erro na API do Chatwoot (conversa): {str(e)}"}), 503
    except Exception as e:
        print(f"Erro inesperado (conversa): {e}")
        return jsonify({"error": "Erro interno no servidor (conversa)."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Rodar em uma porta diferente da padrão para evitar conflitos
