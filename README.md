# Django Kid

Um blog simples em Django, feito para aprender a construir sistemas web do jeito
certo: código limpo, testes primeiro, segurança desde o início e deploy sem sofrimento.

[![CI](https://github.com/vlamirc/django-kid/actions/workflows/ci.yml/badge.svg)](https://github.com/vlamirc/django-kid/actions/workflows/ci.yml)

## O que tem aqui

- **Blog**: posts com rascunho e publicação, página de leitura, "meus posts", edição e exclusão.
- **Contas**: cadastro com e-mail verificado, senhas fortes (mínimo de 12 caracteres, hash Argon2)
  e **autenticação em dois fatores** (app autenticador, códigos de recuperação e chaves de segurança).
- **Autorização** pronta para o sistema inteiro: papéis (Autores, Editores) e regras por objeto
  ("só o autor ou um editor pode editar este post"), usadas em views, templates e admin.
- **2FA obrigatório** para quem tem poder extra (staff e editores).
- **Interface** com o tema [Clean Blog](https://startbootstrap.com/theme/clean-blog) (Bootstrap 5).
- **Testes** com pytest, 100% de cobertura exigida no CI.
- **Ambiente Docker** com PostgreSQL e Mailpit (caixa de e-mails de teste).
- **Pronto para IA**: instruções para agentes (`AGENTS.md`, `CLAUDE.md`) e as skills de Django da Vinta Software.
- **Deploy** preparado para o Render (ou qualquer plataforma que rode Docker).

## Começando

Você só precisa do [Docker](https://docs.docker.com/get-docker/) e do `make`.

```bash
git clone https://github.com/vlamirc/django-kid.git
cd django-kid
make setup   # cria o .env, monta as imagens, cria o banco e dados de exemplo
make up      # sobe em http://localhost:8000
```

Entre com `autor@example.com`, `editora@example.com` ou `leitora@example.com`,
senha `senha-de-demonstracao-123`. A editora vai ser convidada a ativar o 2FA
antes de continuar: use um app como Google Authenticator, Authy ou 1Password.

Os e-mails enviados (verificação de cadastro, troca de senha) aparecem em
http://localhost:8025.

Rode `make` para ver todos os atalhos. Os mais usados:

| Comando | O que faz |
| --- | --- |
| `make up` | Sobe o sistema |
| `make test` | Roda os testes com cobertura |
| `make format` | Formata o código |
| `make check` | Tudo o que o CI verifica |

## Documentação

| Documento | Assunto |
| --- | --- |
| [Arquitetura](docs/arquitetura.md) | Como o código está organizado e por quê |
| [Desenvolvimento](docs/desenvolvimento.md) | Ambiente, comandos e fluxo de trabalho em equipe |
| [Testes e TDD](docs/testes.md) | Como escrever testes neste projeto |
| [Contas e segurança](docs/seguranca.md) | Login, senhas, 2FA e configurações de produção |
| [Autorização](docs/autorizacao.md) | Papéis e regras de permissão |
| [Deploy](docs/deploy.md) | Como colocar no ar |
| [Desenvolvendo com IA](docs/ia.md) | Como o projeto está preparado para assistentes de IA |
| [Decisões (ADRs)](docs/adr/) | Registro das decisões de arquitetura |
| [Como contribuir](CONTRIBUTING.md) | Branches, commits e pull requests |

## Tecnologias

Python 3.13 · Django 5.2 LTS · PostgreSQL 17 · django-allauth · django-rules ·
WhiteNoise · Gunicorn · pytest · ruff · uv · Docker

## Créditos

- Tema [Start Bootstrap Clean Blog](https://github.com/StartBootstrap/startbootstrap-clean-blog), licença MIT
  (veja `static/theme/LICENSE`).
- Templates Bootstrap das telas de conta adaptados do projeto de exemplo do
  [django-allauth](https://docs.allauth.org/), licença MIT.
- Skills de IA: [Django AI Skills](https://github.com/vintasoftware/django-ai-plugins), da Vinta Software, licença MIT.
