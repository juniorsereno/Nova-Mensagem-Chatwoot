# Usar uma imagem Python oficial como imagem base
FROM python:3.9-slim

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos da aplicação para o diretório de trabalho
# Isso inclui app.py, .env, index.html, style.css, script.js
COPY . .

# Expor a porta em que o aplicativo Flask roda
EXPOSE 5001

# Comando para rodar a aplicação quando o container iniciar
# Usar gunicorn é recomendado para produção, mas para simplicidade, flask run.
# Para 'flask run', FLASK_APP precisa ser definido.
# Alternativamente, executar python app.py diretamente.
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
# O python-dotenv já carrega o .env, então não precisamos explicitamente do --env-file aqui
# se o .env for copiado para a imagem.

# CMD ["flask", "run"]
# Ou, para executar diretamente o script que já tem app.run():
# Usando a forma shell para CMD, que pode ser mais robusta em algumas plataformas
CMD python app.py
