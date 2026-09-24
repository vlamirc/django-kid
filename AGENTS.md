# Instruções para agentes de IA

Este arquivo vale para qualquer assistente (Claude Code, Codex, Cursor, Copilot...).
O `CLAUDE.md` apenas importa este arquivo.

## O projeto

Blog em Django feito para aprender boas práticas. Leia `docs/arquitetura.md`
para o mapa do código e `docs/adr/` para as decisões já tomadas (e por quê).

- Django 5.2 LTS, Python 3.13, PostgreSQL 17, dependências com `uv`.
- Login, cadastro e 2FA: django-allauth (`allauth.account` e `allauth.mfa`).
- Autorização: django-rules. Papéis em `apps/accounts/roles.py`, regras em `apps/<app>/rules.py`.
- Interface: templates do Django + tema Start Bootstrap Clean Blog (Bootstrap 5), em `templates/`.

## Idioma

- Código (nomes de variáveis, funções, classes, testes): **inglês**.
- Textos da interface, `verbose_name`, mensagens, docs e comentários: **português do Brasil**.

## Comandos

Rode tudo pelo Docker (`make help` lista os atalhos):

- `make test`: testes com cobertura (a cobertura mínima é 100%).
- `make lint` / `make format`: ruff.
- `make migrations` / `make migrate`.
- `make check`: o mesmo que o CI roda.

Fora do Docker (Postgres local e `.env` com `DATABASE_URL` apontando para `localhost`):
`uv run pytest --cov`, `uv run ruff check .`, `uv run python manage.py ...`.

## Como trabalhar

1. **TDD sempre.** Escreva o teste que falha, rode e veja falhar, escreva o mínimo
   de código para passar, depois refatore. Veja `docs/testes.md`.
2. **Autorização só por regras.** Nunca verifique `user.groups` ou `is_staff` direto
   numa view ou template. Crie ou reutilize um predicado em `rules.py`, declare em
   `Meta.rules_permissions` e use `PermissionRequiredMixin` / `{% has_perm %}`.
   Toda regra nova entra na tabela de testes (`apps/blog/tests/test_rules.py` é o modelo).
3. **Views finas.** Regra de negócio fica no modelo, no QuerySet ou em uma função
   de serviço; a view só orquestra.
4. **Mudanças pequenas.** Um assunto por PR. Nada de refatorações não pedidas.
5. **Sem dependências novas** sem justificar: precisa ser popular, mantida e
   resolver algo que o Django não resolve. Registre a decisão em `docs/adr/`.
6. **Migrações:** gere com `makemigrations`, revise o arquivo e nunca edite uma
   migração que já foi para a `main`.
7. **Segurança:** nunca leia nem escreva o `.env`; nunca coloque segredos no código.
   Conteúdo de usuário é sempre escapado (nada de `|safe` em texto de usuário).

## Antes de dizer que terminou

- `make check` passa (lint, testes com 100% de cobertura, migrações em dia).
- Documentação em `docs/` atualizada se algo mudou para quem desenvolve.
