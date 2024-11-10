# Guia de Deployment

## Requisitos
- Docker 20.10+
- Docker Compose 2.0+
- AWS CLI configurado
- Kubectl (para K8s)
- Python 3.9+

## Ambientes

### Desenvolvimento
```bash
# Iniciar ambiente de desenvolvimento
make dev

# Rodar testes
make test

# Lint e formatação
make lint
```

### Staging
```bash
# Deploy para staging
make deploy-staging
```

### Produção
```bash
# Deploy para produção
make deploy-prod
```

## Configuração do Ambiente

### Variáveis de Ambiente
Copie `.env.example` para `.env` e configure:

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379

# Segurança
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=https://yourdomain.com

# AWS
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

### Banco de Dados
1. Criar banco de dados
```bash
createdb spinmaster
```

2. Rodar migrations
```bash
alembic upgrade head
```

## Docker

### Build
```bash
# Desenvolvimento
docker-compose build

# Produção
docker-compose -f docker-compose.prod.yml build
```

### Deploy com Docker
```bash
# Iniciar serviços
docker-compose -f docker-compose.prod.yml up -d

# Verificar logs
docker-compose -f docker-compose.prod.yml logs -f
```

## CI/CD Pipeline

### GitHub Actions
- CI pipeline: `.github/workflows/ci.yml`
- CD pipeline: `.github/workflows/cd.yml`

### Processo
1. Push para `main` ou `develop`
2. Testes automatizados
3. Build de imagens Docker
4. Push para registry
5. Deploy automático

## Monitoramento

### Setup Grafana
1. Acessar dashboard Grafana
2. Importar dashboards predefinidos
3. Configurar alertas

### Logs
- Logs centralizados no CloudWatch
- Retention policy: 30 dias
- Alertas configurados

## Backup

### Database
- Backups automáticos diários
- Retenção: 30 dias
- Teste de restore mensal

### Restore
```bash
# Restore do último backup
make db-restore

# Restore de data específica
make db-restore DATE=2024-01-01
```

## Troubleshooting

### Problemas Comuns
1. Database connection fails
```bash
# Verificar conectividade
make db-check
```

2. Redis connection fails
```bash
# Verificar Redis
make redis-check
```

### Health Check
```bash
# Verificar status dos serviços
make health-check
```

## Rollback

### Procedimento
1. Identificar versão para rollback
2. Executar rollback
```bash
make rollback VERSION=v1.2.3
```

### Verificação
```bash
# Verificar status após rollback
make verify-deployment
```
