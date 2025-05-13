document.addEventListener('DOMContentLoaded', function() {
          const inboxSelect = document.getElementById('inbox_id_select');
          const defaultOption = document.createElement('option');
          defaultOption.value = \"\";
          defaultOption.textContent = \"Carregando caixas de entrada...\";
          defaultOption.disabled = true;
          defaultOption.selected = true;
          inboxSelect.appendChild(defaultOption);
          const backendUrl = 'http://127.0.0.1:5001';
          fetch(`${backendUrl}/api/inboxes`)
              .then(response => {
                  if (!response.ok) {
                      throw new Error(`Erro HTTP ${response.status} ao buscar caixas de entrada.`);
                  }
                  return response.json();
              })
              .then(inboxes => {
                  inboxSelect.innerHTML = ''; 
                  
                  if (inboxes && inboxes.length > 0) {
                      const placeholderOption = document.createElement('option');
                      placeholderOption.value = \"\";
                      placeholderOption.textContent = \"Selecione uma caixa de entrada\";
                      placeholderOption.disabled = true;
                      placeholderOption.selected = true;
                      inboxSelect.appendChild(placeholderOption);
                      inboxes.forEach(inbox => {
                          if (inbox.id && inbox.name) {
                              const option = document.createElement('option');
                              option.value = inbox.id;
                              option.textContent = inbox.name;
                              inboxSelect.appendChild(option);
                          }
                      });
                  } else {
                      defaultOption.textContent = \"Nenhuma caixa de entrada encontrada.\";
                      inboxSelect.appendChild(defaultOption);
                  }
              })
              .catch(error => {
                  console.error('Erro ao buscar caixas de entrada:', error);
                  inboxSelect.innerHTML = '';
                  defaultOption.textContent = \"Erro ao carregar caixas\";
                  defaultOption.selected = true;
                  defaultOption.disabled = true;
                  inboxSelect.appendChild(defaultOption);
              });
          const form = document.querySelector('.form');
          form.addEventListener('submit', function(event) {
              event.preventDefault();
              const nomeCompletoInput = form.querySelector('label:not(.tel-label) input[type=\"text\"].input');
              const nomeCompleto = nomeCompletoInput ? nomeCompletoInput.value : '';
              
              const telefoneInput = form.querySelector('.tel-label input.input');
              const telefone = telefoneInput ? telefoneInput.value : '';
              const inboxId = inboxSelect.value;
              const mensagemTextarea = form.querySelector('textarea.input');
              const mensagem = mensagemTextarea ? mensagemTextarea.value : '';
              if (!inboxId) {
                  alert(\"Por favor, selecione uma caixa de entrada.\");
                  return;
              }
              const formData = { nomeCompleto, telefone, inboxId, mensagem };
              console.log(\"Enviando dados do formulário:\", formData);
              const submitButton = form.querySelector('button.submit');
              const originalButtonText = submitButton.textContent;
              submitButton.textContent = 'Enviando...';
              submitButton.disabled = true;
              fetch(`${backendUrl}/api/send-message`, {
                  method: 'POST',
                  headers: {
                      'Content-Type': 'application/json',
                  },
                  body: JSON.stringify(formData),
              })
              .then(response => {
                  const contentType = response.headers.get(\"content-type\");
                  if (contentType && contentType.indexOf(\"application/json\") !== -1) {
                      return response.json().then(data => ({ status: response.status, ok: response.ok, body: data }));
                  } else {
                      return response.text().then(text => ({ 
                          status: response.status, 
                          ok: response.ok, 
                          body: { error: `Resposta não JSON: ${text || 'Corpo vazio'}` } 
                      }));
                  }
              })
              .then(result => {
                  submitButton.textContent = originalButtonText;
                  submitButton.disabled = false;
                  if (result.ok) {
                      alert(result.body.message || \"Mensagem enviada com sucesso!\");
                      form.reset();
                      if (inboxSelect.options.length > 0) {
                          inboxSelect.selectedIndex = 0;
                          for(let i=0; i < inboxSelect.options.length; i++) {
                              if(inboxSelect.options[i].disabled && inboxSelect.options[i].value === \"\") {
                                  inboxSelect.selectedIndex = i;
                                  break;
                              }
                          }
                      }
                  } else {
                      console.error(\"Erro ao enviar mensagem:\", result.body);
                      alert(`Erro ao enviar mensagem: ${result.body.error || 'Erro desconhecido.'}`);
                  }
              })
              .catch(error => {
                  submitButton.textContent = originalButtonText;
                  submitButton.disabled = false;
                  console.error('Erro na requisição de envio:', error);
                  alert(`Erro na requisição de envio: ${error.message || 'Verifique a conexão ou o console para mais detalhes.'}`);
              });
          });
      });
      
