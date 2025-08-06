# Classificador de comentários

Este projeto é uma API REST para processamento e classificação de comentários usando Flask, PostgreSQL e Docker.

## 📋 Pré-requisitos

- Docker
- Docker Compose
- Git

## 🚀 Como subir a aplicação

### Suba os serviços com Docker Compose

```bash
# Subir todos os serviços (API + PostgreSQL)
docker-compose up -d

# Para ver os logs
docker-compose logs -f

# Para verificar se os containers estão rodando
docker-compose ps
```

### Aguarde os serviços iniciarem

A aplicação estará disponível em: `http://localhost:5000`

O banco PostgreSQL estará em: `localhost:5432`

## 📚 Endpoints da API

### Base URL
```
http://localhost:5000
```

### 🔐 Autenticação

#### `POST /login`
Obter token JWT para autenticação.

**Request:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login realizado com sucesso"
}
```

### 📝 Comentários

#### `GET /api/comentarios`
Listar todos os comentários processados (não requer autenticação).

**Request:**
```bash
curl -X GET http://localhost:5000/api/comentarios
```

**Response:**
```json
{
  "comentarios": [
    {
      "id": 1,
      "categoria": "ELOGIO",
      "confianca": 0.95,
      "tags_funcionalidades": ["feat_autotune", "clip_narrativa"],
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

#### `POST /api/comentarios`
Processar e classificar novos comentários (requer autenticação JWT).

**Request:**
```bash
# 1. Primeiro obter o token
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' | \
  jq -r '.access_token')

# 2. Usar o token para enviar comentários
curl -X POST http://localhost:5000/api/comentarios \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "comentarios": [
      "Este app é incrível! Adorei as funcionalidades de autotune.",
      "Não gostei muito da interface, poderia ser melhor."
    ]
  }'
```

**Request Body (um comentário):**
```json
{
  "id": 0, "texto": "Este app é incrível! Adorei as funcionalidades de autotune."
}
```

**Request Body (múltiplos comentários):**
```json
[
    {"id": 1, "texto": "Adorei a nova interface! Muito mais intuitiva"},
    {"id": 2, "texto": "O player trava quando tento mudar de faixa rapidamente."},
    {"id": 3, "texto": "Seria ótimo se tivesse um modo offline para playlists."},
    {"id": 4, "texto": "A qualidade do som está incrível depois da última atualização."}
]
```

**Response:**
```json
{
  "classifications": [
    {
      "id": 1,
      "categoria": "ELOGIO",
      "confianca": 0.95,
      "tags_funcionalidades": ["feat_autotune", "clip_narrativa"]
    },
    {
      "id": 2,
      "categoria": "CRITICA",
      "confianca": 0.87,
      "tags_funcionalidades": ["interface_ui"]
    }
  ],
  "total": 2
}
```

## 🔑 Autenticação JWT

### Credenciais padrão:
- **Usuário:** `admin`
- **Senha:** `admin`

### Como usar o token:

1. **Obter token via login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'
```

2. **Usar token nas requisições:**
```bash
curl -X POST http://localhost:5000/api/comentarios \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"comentario": "Seu comentário aqui"}'
```

3. **Token expira em 30 minutos** - será necessário fazer login novamente.

##  📊 Acesso à Página de Relatórios Semanais

Este projeto disponibiliza uma página de relatórios acessível via navegador.

### Como acessar

1. Certifique-se que o servidor está rodando localmente na porta 5000.

2. Abra seu navegador preferido (Chrome, Firefox, Edge, etc).

3. Digite na barra de endereços o seguinte URL: http://localhost:5000/relatorio/semana


## 🐳 Comandos Docker úteis

### Gerenciar containers
```bash
# Parar todos os serviços
docker-compose down

# Rebuild e restart
docker-compose up --build -d

# Deletar a tabela de classificações no PostgreSQL
docker exec -it postgres-db psql -U admin -d alumusic -c "DROP TABLE IF EXISTS classifications CASCADE;"
```

### Limpar dados
```bash
# Remover volumes (apaga dados do banco)
docker-compose down -v

# Remover tudo e rebuild
docker-compose down -v --rmi all
docker-compose up --build -d
```

## 📊 Estrutura de resposta

### Categorias possíveis:
- `ELOGIO` - Comentários positivos
- `CRITICA` - Comentários negativos  
- `SUGESTAO` - Sugestões de melhorias
- `NEUTRO` - Comentários neutros

### Tags de funcionalidades:
- `feat_autotune` - Funcionalidade de autotune
- `clip_narrativa` - Clipes e narrativas
- `interface_ui` - Interface do usuário
- `performance` - Performance da aplicação
- `audio_quality` - Qualidade do áudio

## 🚨 Resolução de problemas

### Erro de conexão com banco
```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps postgres-db

# Ver logs do PostgreSQL
docker-compose logs -f postgres-db

# Recriar banco
docker-compose down postgres-db
docker-compose up postgres-db -d
```

### Erro 401 Unauthorized
- Verifique se está enviando o token JWT no header
- Verifique se o token não expirou
- Refaça o login para obter novo token

### Erro 500 Internal Server Error
```bash
# Ver logs da API
docker-compose logs -f flask-app

# Restart da API
docker-compose restart flask-app
```

### Portas em uso
```bash
# Verificar portas ocupadas
netstat -tulpn | grep :5000
netstat -tulpn | grep :5432
```

## 📝 Exemplo completo de uso

```bash
# 1. Subir aplicação
docker-compose up -d

# 2. Fazer login e obter token
TOKEN=$(curl -s -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}' | \
  jq -r '.access_token')

# 3. Enviar comentários para processamento
curl -X POST http://localhost:5000/api/comentarios \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "comentarios": [
      "Adorei o app! O autotune funciona perfeitamente.",
      "A interface poderia ser mais intuitiva."
    ]
  }'

# 4. Consultar comentários processados
curl -X GET http://localhost:5000/api/comentarios

# 5. Parar aplicação
docker-compose down
```

## 🛠️ Variáveis de ambiente

Preencha o arquivo `.env` na raiz do projeto:

```env
# Banco de dados
DATABASE_URL=postgresql://admin:admin@localhost:5432/alumusic

# JWT
JWT_USERNAME=admin
JWT_PASSWORD=admin
JWT_SECRET_KEY=chave-super-secreta

# API
MODEL_NAME=gemma3:1b-it-qat
OLLAMA_URL=http://ollama:11434/api/generate

```

---
