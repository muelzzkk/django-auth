# Projeto Django - Área Restrita

## 📌 Descrição

Aplicação Django com sistema de autenticação, gerenciamento de funcionários e pedidos. Implementa as melhores práticas de segurança, auditoria e soft delete.

## ✨ Recursos Implementados

### ✅ 1. Configuração Segura com `.env`
- Variáveis de ambiente para credenciais
- Suporte para PostgreSQL e SQLite
- Arquivo `.env` para development

### ✅ 2. Herança de Modelos - BaseModel
- Campo `created_at` - Data de criação
- Campo `updated_at` - Data de atualização automática
- Campo `is_deleted` - Para soft delete

### ✅ 3. Soft Delete
- `SoftDeleteManager` - Retorna apenas registros ativos por padrão
- `objects` - Manager padrão (sem deletados)
- `all_objects` - Manager para incluir todos
- Métodos `soft_delete()` e `restore()`

### ✅ 4. Suporte a Bancos de Dados
- PostgreSQL configurado por padrão
- Fallback para SQLite em desenvolvimento
- Fácil troca via `.env`

### ✅ 5. Configuração de Mídia e Estáticos
- `/media/` - Para uploads de usuários
- `/static/` - Para arquivos estáticos
- `STATICFILES_DIRS` e `STATIC_ROOT` configurados

### ✅ 6. Modelo Order
```python
- numero_pedido (unique)
- funcionario (ForeignKey)
- data_pedido
- valor_total
- status (pending, processing, completed, cancelled)
- prioridade (low, medium, high, urgent)
- descricao
- data_entrega
- Métodos: marcar_como_processando(), marcar_como_concluido(), cancelar()
```

### ✅ 7. Templates Django
- `base.html` - Template base com navegação
- `funcionarios/funcionario_list.html` - Listagem de funcionários
- `funcionarios/funcionario_detail.html` - Detalhes do funcionário
- `orders/order_list.html` - Listagem de pedidos com filtros
- `orders/order_detail.html` - Detalhes do pedido
- `dashboard.html` - Dashboard com estatísticas

## 📁 Estrutura do Projeto

```
project_django/
├── area_restrita/           # Projeto Django
│   ├── settings.py          # Configurações (com .env)
│   ├── urls.py              # URLs principais
│   ├── asgi.py
│   └── wsgi.py
├── funcionarios/            # App Django
│   ├── models.py            # BaseModel, Funcionario, Order
│   ├── views.py             # Views com Class-Based Views
│   ├── urls.py              # URLs da app
│   ├── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── funcionarios/
│   │   ├── orders/
│   │   └── dashboard.html
│   └── migrations/
├── .env                     # Variáveis de ambiente
├── .gitignore              # Git ignore
├── manage.py
├── requirements.txt        # Dependências
└── POSTGRESQL_SETUP.md     # Guia de setup

```

## 🚀 Como Começar

### 1. Clone o repositório
```bash
git clone <url-do-repo>
cd project_django
```

### 2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o PostgreSQL (Ver POSTGRESQL_SETUP.md)
```bash
createdb -U postgres funcionarios_db
```

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superuser
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor
```bash
python manage.py runserver
```

Acesse: http://localhost:8000/

## 🔑 URLs Principais

- `http://localhost:8000/` - Home
- `http://localhost:8000/admin/` - Admin (superuser)
- `http://localhost:8000/login/` - Login
- `http://localhost:8000/painel/` - Painel
- `http://localhost:8000/dashboard/` - Dashboard
- `http://localhost:8000/funcionarios/` - Listagem de Funcionários
- `http://localhost:8000/pedidos/` - Listagem de Pedidos

## 💾 Modelos

### BaseModel (Abstrato)
```python
- created_at: DateTimeField
- updated_at: DateTimeField
- is_deleted: BooleanField
- objects: SoftDeleteManager
- all_objects: Manager
```

### Funcionario
```python
- nome: CharField
- cargo: CharField
- email: EmailField (unique)
- salario: DecimalField (opcional)
- Herda de BaseModel
```

### Order
```python
- numero_pedido: CharField (unique)
- funcionario: ForeignKey(Funcionario)
- data_pedido: DateField
- valor_total: DecimalField
- status: CharField (choices)
- prioridade: CharField (choices)
- descricao: TextField (opcional)
- data_entrega: DateField (opcional)
- Herda de BaseModel
```

## 🔧 Configurações Important

### settings.py
```python
# Variáveis de ambiente
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
DB_ENGINE = os.getenv("DB_ENGINE")
# ...
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
```

## 📊 Funcionalidades Avançadas

### Queries com Soft Delete
```python
# Apenas registros ativos
Funcionario.objects.all()

# Incluindo deletados
Funcionario.all_objects.all()

# Apenas deletados
Funcionario.all_objects.filter(is_deleted=True)

# Soft delete
funcionario.soft_delete()

# Restaurar
funcionario.restore()
```

### Filtros e Búsca
- Listagem de funcionários com busca por nome/email
- Listagem de pedidos com filtros por status e prioridade
- Paginação em todas as listas

### Dashboard
- Total de funcionários
- Total de pedidos
- Pedidos por status
- Pedidos por prioridade
- Valor total e médio de pedidos
- Top 5 últimos pedidos
- Top 5 funcionários com mais pedidos

## 🔐 Segurança

- ✅ Credenciais em `.env` (não no código)
- ✅ SECRET_KEY em variável de ambiente
- ✅ DEBUG controlado por `.env`
- ✅ ALLOWED_HOSTS configurável
- ✅ Soft delete para manter histórico
- ✅ Auditoria com timestamps automáticos

## 📚 Recursos Úteis

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [psycopg2](https://www.psycopg.org/)

## 🤝 Contribuindo

Para contribuir:
1. Crie uma branch para sua feature
2. Faça commit das suas mudanças
3. Envie um Pull Request

## 📄 Licença

Este projeto é um exercício educacional.

---

**Última atualização**: 17 de abril de 2026
