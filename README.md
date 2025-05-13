# Sticker Swap API

Este é um projeto backend utilizando Django REST Framework (DRF), totalmente containerizado com Docker e Docker Compose. As variáveis de ambiente são gerenciadas através de um arquivo `.env`.

## 🚀 Tecnologias

- Python 3.10+
- Django REST Framework
- PostgreSQL
- Docker
- Docker Compose
- .env (gerenciamento de ambiente)


---

## ⚙️ Configuração

### 1. Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DEBUG=1
SECRET_KEY=sua-secret-key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
POSTGRES_DB=meubanco
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Execução

```
docker-compose up --build
```




