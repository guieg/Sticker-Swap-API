# Usando a imagem oficial do Python como base
FROM python:3.12-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Instalando dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiando o arquivo de dependências (requirements.txt) para o container
COPY requirements.txt /app/

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiando todo o código da aplicação para o container
COPY . /app/

# Expondo a porta 8000 (porta padrão do Django)
EXPOSE 8000

# Definindo o comando de inicialização (serve a aplicação com o Django)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
