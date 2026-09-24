# Desenvolvimento

## Ambiente com Docker (recomendado)

Pré-requisitos: Docker (com Docker Compose) e `make`.

```bash
make setup   # só na primeira vez
make up      # http://localhost:8000
```

O `compose.yaml` sobe três serviços:

| Serviço | Endereço | Para quê |
| --- | --- | --- |
| `web` | http://localhost:8000 | Django com recarga automática ao salvar arquivos |
| `db` | `localhost:5432` (usuário/senha/banco: `blog`) | PostgreSQL 17 |
| `mailpit` | http://localhost:8025 | Captura os e-mails enviados |

O código é montado como volume, então editar um arquivo no seu editor já reflete
no container. Dependências Python ficam dentro da imagem: depois de mudar o
`pyproject.toml`, rode `docker compose build`.

### Administrador

```bash
make superuser
```

Staff precisa ativar o 2FA antes de acessar o admin. Em desenvolvimento dá para
desligar essa exigência com `MFA_REQUIRED_FOR_PRIVILEGED_USERS=False` no `.env`.

## Ambiente sem Docker (opcional)

Útil para o editor achar as dependências (autocompletar) ou rodar testes mais rápido.

```bash
# instale o uv: https://docs.astral.sh/uv/
uv sync                       # cria .venv com Python 3.13 e as dependências
cp .env.example .env          # e troque "db" por "localhost" no DATABASE_URL
docker compose up -d db       # só o banco
uv run pytest --cov
uv run python manage.py runserver
```

## Dependências

Declaradas no `pyproject.toml` e travadas no `uv.lock` (sempre faça commit dos dois).

```bash
uv add nome-do-pacote          # dependência da aplicação
uv add --dev nome-do-pacote    # só para desenvolvimento
uv lock --upgrade              # atualiza tudo dentro das faixas permitidas
```

O Dependabot abre PRs semanais de atualização; o CI diz se é seguro aceitar.

## Qualidade de código

- **ruff** faz lint e formatação (substitui flake8, isort, black e outros). Regras no `pyproject.toml`.
- **pre-commit** roda o ruff antes de cada commit: `uv run pre-commit install` (uma vez).
- **EditorConfig** padroniza indentação em qualquer editor.

## Fluxo de trabalho em equipe

Veja o [CONTRIBUTING.md](../CONTRIBUTING.md). Resumo: uma branch por mudança,
PR pequeno com testes, CI verde e revisão antes de juntar na `main`.

## Variáveis de ambiente

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `DEBUG` | `False` | Modo de desenvolvimento. Nunca `True` em produção |
| `SECRET_KEY` | (obrigatória) | Chave secreta do Django |
| `DATABASE_URL` | (obrigatória) | `postgres://usuario:senha@host:5432/banco` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Domínios aceitos, separados por vírgula |
| `CSRF_TRUSTED_ORIGINS` | vazio | Origens HTTPS confiáveis (ex.: `https://meusite.com`) |
| `EMAIL_URL` | console | SMTP: `smtp+tls://usuario:senha@host:587` |
| `DEFAULT_FROM_EMAIL` | `Django Kid <nao-responda@localhost>` | Remetente dos e-mails |
| `MFA_REQUIRED_FOR_PRIVILEGED_USERS` | `True` | Exige 2FA de staff e editores |
| `SECURE_SSL_REDIRECT` | `True` sem DEBUG | Redireciona HTTP para HTTPS |
| `SECURE_HSTS_SECONDS` | 30 dias sem DEBUG | Tempo do cabeçalho HSTS |
| `CONN_MAX_AGE` | `60` | Segundos que uma conexão com o banco é reaproveitada |
| `LOG_LEVEL` | `INFO` | Nível de log |
