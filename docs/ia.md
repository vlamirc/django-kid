# Desenvolvendo com IA

O projeto está preparado para que assistentes de IA (Claude Code, Codex, Cursor,
Copilot) entendam as regras da casa e trabalhem com autonomia e segurança.

## O que já vem configurado

| Arquivo | Para quê |
| --- | --- |
| `AGENTS.md` | Instruções do projeto para qualquer agente: idioma, comandos, TDD, regras de autorização |
| `CLAUDE.md` | Importa o `AGENTS.md` e adiciona o que é específico do Claude Code |
| `.claude/settings.json` | Instala as skills de Django, libera comandos seguros (testes, lint, make) e bloqueia a leitura do `.env` |
| `.claude/skills/tdd-feature/` | Skill do projeto: passo a passo para criar uma funcionalidade com TDD |

## Skills de Django (Vinta Software)

O pacote que você tinha ouvido falar é o **Django AI Skills**, repositório
[vintasoftware/django-ai-plugins](https://github.com/vintasoftware/django-ai-plugins),
mantido pela Vinta Software (empresa brasileira, referência na comunidade Django), licença MIT.
Ele segue o padrão aberto [Agent Skills](https://agentskills.io/) e funciona no Claude Code,
Codex, Cursor e OpenCode.

Habilitamos três das cinco skills:

| Skill | Para quê |
| --- | --- |
| `django-expert` | Boas práticas de modelos, ORM, views, segurança, testes e performance |
| `django-safe-migration` | Migrações seguras no PostgreSQL, sem travar a produção |
| `django-reviewer` | Revisão de código Django antes do PR |

As outras duas (`django-celery-expert` e `cdrf-expert`) são para Celery e Django REST
Framework, que o projeto ainda não usa. Se um dia usar, habilite em `.claude/settings.json`.

### Claude Code

Ao abrir o projeto e confiar na pasta, o Claude Code oferece instalar o marketplace e as
skills declaradas em `.claude/settings.json`. Para instalar manualmente:

```text
/plugin marketplace add vintasoftware/django-ai-plugins
/plugin install django-expert@django-ai-plugins
```

### Codex, Cursor e outros

Veja as [instruções de instalação da Vinta](https://github.com/vintasoftware/django-ai-plugins/blob/main/docs/installation.md).
O `AGENTS.md` é lido automaticamente pela maioria das ferramentas.

## Como tirar o máximo

- **Peça em termos de comportamento**: "autores devem poder agendar a publicação de um post".
  O agente segue o `AGENTS.md`: escreve o teste, implementa, roda `make check`.
- **Peça revisão**: "revise minhas mudanças com o django-reviewer".
- **Deixe o CI ser o juiz**: nenhum PR entra sem lint, testes e 100% de cobertura.
- **Mantenha o `AGENTS.md` vivo**: quando o time combinar uma regra nova, escreva lá.
  Instrução que não está escrita é instrução que a IA não segue.

## Próximo passo opcional

A Vinta também mantém o [django-ai-boost](https://github.com/vintasoftware/django-ai-boost), um
servidor MCP que deixa o assistente consultar modelos, URLs e configurações do projeto rodando.
Não foi incluído para manter o ambiente simples; vale experimentar quando o projeto crescer.
