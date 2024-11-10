# SpinMaster API 🏓

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![FastAPI Version](https://img.shields.io/badge/fastapi-0.109.0-green.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-87%25-green.svg)

API backend do sistema SpinMaster para gerenciamento de rankings e estatísticas de tênis de mesa.

## 🏗️ Arquitetura

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0
- **Banco de Dados**: PostgreSQL 14
- **Cache**: Redis 6
- **Documentação**: OpenAPI (Swagger) + ReDoc
- **Containerização**: Docker
- **CI/CD**: GitHub Actions

## 🔧 Requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Docker e Docker Compose
- Make (opcional, para comandos helper)

## 🚀 Quick Start

1. **Clone o repositório**
```bash
git clone https://github.com/your-org/spinmaster-api.git
cd spinmaster-api
```

2. **Crie e ative o ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para ambiente de desenvolvimento
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicie os serviços com Docker**
```bash
docker-compose up -d
```

6. **Execute as migrações**
```bash
alembic upgrade head
```

7. **Inicie o servidor de desenvolvimento**
```bash
uvicorn app.main:app --reload --port 8000
```

A API estará disponível em `http://localhost:8000`
Documentação Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

## 📁 Estrutura do Projeto

```
app/
├── api/                  # Endpoints da API
│   ├── v1/              # Versão 1 da API
│   │   ├── players/     # Endpoints de jogadores
│   │   ├── matches/     # Endpoints de partidas
│   │   └── tournaments/ # Endpoints de torneios
│   └── dependencies/    # Dependências compartilhadas
├── core/                # Lógica de negócio
│   ├── models/         # Modelos SQLAlchemy
│   ├── schemas/        # Schemas Pydantic
│   └── services/       # Serviços de negócio
├── db/                  # Configuração do banco
│   ├── migrations/     # Migrações Alembic
│   └── repositories/   # Repositórios
└── utils/              # Utilitários
```

## 🔑 Variáveis de Ambiente

```env
# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost:5432/spinmaster

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_V1_PREFIX=/api/v1
PROJECT_NAME=SpinMaster API
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## 📚 Comandos Úteis

```bash
# Desenvolvimento
make run         # Inicia servidor de desenvolvimento
make test        # Executa testes
make lint        # Executa linters (flake8, mypy)
make format      # Formata código (black, isort)

# Banco de Dados
make migrations  # Gera novas migrações
make migrate     # Aplica migrações
make downgrade  # Reverte última migração

# Docker
make build      # Constrói imagem Docker
make up         # Inicia containers
make down       # Para containers
```

## 🧪 Testes

```bash
# Executa todos os testes
pytest

# Com cobertura
pytest --cov=app

# Testes específicos
pytest tests/api/v1/test_players.py

# Relatório de cobertura HTML
pytest --cov=app --cov-report=html
```

## 📡 API Endpoints

### Players
- `GET /api/v1/players/` - Lista jogadores
- `POST /api/v1/players/` - Cria jogador
- `GET /api/v1/players/{id}` - Detalhes do jogador
- `PUT /api/v1/players/{id}` - Atualiza jogador
- `DELETE /api/v1/players/{id}` - Remove jogador

### Matches
- `GET /api/v1/matches/` - Lista partidas
- `POST /api/v1/matches/` - Registra partida
- `GET /api/v1/matches/{id}` - Detalhes da partida

### Rankings
- `GET /api/v1/rankings/` - Ranking geral
- `GET /api/v1/rankings/category/{category}` - Ranking por categoria

## 🔐 Autenticação

A API utiliza JWT para autenticação. Tokens devem ser enviados no header:
```
Authorization: Bearer <token>
```

## 📈 Monitoramento

- Health Check: `/health`
- Métricas: `/metrics`
- Status: `/status`

## 🚀 Deploy

### Produção
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Staging
```bash
docker-compose -f docker-compose.staging.yml up -d
```

## 🔄 CI/CD Pipeline

1. **Testes**
   - Lint check
   - Type check
   - Unit tests
   - Integration tests

2. **Build**
   - Docker image build
   - Push to registry

3. **Deploy**
   - Staging deployment
   - Production deployment

## 📝 Convenções de Código

- **Estilo**: [Black](https://github.com/psf/black)
- **Imports**: [isort](https://pycqa.github.io/isort/)
- **Linting**: flake8
- **Type Checking**: mypy
- **Docstrings**: Google style

## 🐛 Debug

1. Configure PyCharm/VSCode para debugging
2. Use `ipdb` para debugging interativo
3. Logs disponíveis em `logs/app.log`

## 🤝 Contribuição

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/amazing`)
3. Commit suas alterações (`git commit -m 'Add: amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

### Processo de Review
- Dois aprovadores necessários
- Todos os testes passando
- Cobertura mínima de 80%
- Sem débitos técnicos

## 📚 Documentação Adicional

- [Guia de Arquitetura](./docs/ARCHITECTURE.md)
- [Guia de Deploy](./docs/DEPLOYMENT.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)

## 📞 Suporte

- GitHub Issues
- Email: dev@spinmaster.com
- Slack: #spinmaster-dev

---
Desenvolvido com ❤️ pelo time SpinMaster
