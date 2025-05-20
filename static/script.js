document.addEventListener('DOMContentLoaded', function() {
    const inboxSelect = document.getElementById('inbox_id_select');

    // Adiciona uma opção padrão enquanto carrega ou se falhar
    const defaultOption = document.createElement('option');
    defaultOption.value = "";
    defaultOption.textContent = "Carregando caixas de entrada...";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    inboxSelect.appendChild(defaultOption);

    // Use a relative URL to ensure it works both locally and when deployed
    const backendUrl = ''; // Empty string means same domain as the frontend

    fetch(`${backendUrl}/api/inboxes`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP ${response.status} ao buscar caixas de entrada.`);
            }
            return response.json();
        })
        .then(inboxes => {
            // Limpa a opção "Carregando..."
            inboxSelect.innerHTML = '';

            if (inboxes && inboxes.length > 0) {
                const placeholderOption = document.createElement('option');
                placeholderOption.value = "";
                placeholderOption.textContent = "Selecione uma caixa de entrada";
                placeholderOption.disabled = true;
                placeholderOption.selected = true;
                inboxSelect.appendChild(placeholderOption);

                inboxes.forEach(inbox => {
                    if (inbox.id && inbox.name) { // Verifica se os dados esperados existem
                        const option = document.createElement('option');
                        option.value = inbox.id;
                        option.textContent = inbox.name;
                        inboxSelect.appendChild(option);
                    }
                });
            } else {
                defaultOption.textContent = "Nenhuma caixa de entrada encontrada.";
                inboxSelect.appendChild(defaultOption); // Readiciona se estiver vazio
            }
        })
        .catch(error => {
            console.error('Erro ao buscar caixas de entrada:', error);
            // Mantém ou atualiza a opção padrão para indicar o erro
            inboxSelect.innerHTML = ''; // Limpa antes de adicionar a de erro
            defaultOption.textContent = "Erro ao carregar caixas";
            defaultOption.selected = true;
            defaultOption.disabled = true;
            inboxSelect.appendChild(defaultOption);
        });

    // Lógica para submissão do formulário será adicionada aqui futuramente
    const form = document.querySelector('.form');
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário
        // Coletar dados do formulário
        const nomeCompletoInput = document.getElementById('nome_completo');
        const nomeCompleto = nomeCompletoInput ? nomeCompletoInput.value : '';

        const telefoneInput = document.getElementById('telefone');
        const telefone = telefoneInput ? telefoneInput.value : '';

        const inboxId = inboxSelect.value;
        const mensagemTextarea = document.getElementById('mensagem');
        const mensagem = mensagemTextarea ? mensagemTextarea.value : '';

        if (!inboxId) {
            alert("Por favor, selecione uma caixa de entrada.");
            return;
        }

        const formData = { nomeCompleto, telefone, inboxId, mensagem };
        console.log("Enviando dados do formulário:", formData);

        // Mostra um feedback de carregamento
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
            // Independentemente do status, tenta parsear o JSON se o content-type for JSON
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                return response.json().then(data => ({ status: response.status, ok: response.ok, body: data }));
            } else {
                // Se não for JSON, trata como texto e cria um objeto de erro padronizado
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
                alert(result.body.message || "Mensagem enviada com sucesso!");
                form.reset(); // Limpa o formulário
                // Reseta o select para a opção placeholder
                if (inboxSelect.options.length > 0) {
                    inboxSelect.selectedIndex = 0; // Assume que o placeholder é o primeiro
                     // Se o primeiro não for o placeholder, encontre-o
                    for(let i=0; i < inboxSelect.options.length; i++) {
                        if(inboxSelect.options[i].disabled && inboxSelect.options[i].value === "") {
                            inboxSelect.selectedIndex = i;
                            break;
                        }
                    }
                }
            } else {
                console.error("Erro ao enviar mensagem:", result.body);
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
