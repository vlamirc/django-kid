# Arquitetura

O objetivo é que qualquer pessoa que já viu o tutorial oficial do Django se
sinta em casa. Nada de camadas inventadas: usamos o que o Django oferece e só
adicionamos pacotes quando eles resolvem algo que o Django não resolve.

## Mapa do código

```text
config/                 configuração do projeto
  settings.py           um único arquivo, configurado por variáveis de ambiente
  urls.py               rotas principais
apps/
  core/                 peças genéricas sem regra de negócio (health check, mixins de formulário)
  accounts/             usuário, papéis (roles) e o middleware que exige 2FA
  blog/                 posts: modelo, regras de autorização, views, formulários
    models.py           Post e PostQuerySet
    rules.py            quem pode fazer o quê com um post
    views.py            views baseadas em classe, finas
    tests/              testes da app, com factories
templates/              todos os templates (fica fácil de achar)
  base.html             layout do site (tema Clean Blog)
  allauth/              adapta as telas de login/cadastro/2FA ao layout
static/                 CSS/JS/imagens (o tema fica em static/theme/)
conftest.py             fixtures de teste compartilhadas
```

## Como uma requisição flui

```text
URL (apps/blog/urls.py)
  -> View (apps/blog/views.py)
       PermissionRequiredMixin pergunta: user.has_perm("blog.change_post", post)?
         -> django-rules avalia apps/blog/rules.py
       QuerySet (Post.objects.published()) busca os dados
  -> Template (templates/blog/*.html)
```

## Princípios aplicados

- **KISS**: um arquivo de settings; templates no projeto; Bootstrap sem build de front-end;
  texto do post como texto simples (sem editor rico).
- **DRY**: a regra de quem pode editar um post existe em um único lugar (`rules.py`) e é
  usada pela view, pelo template e pelo admin. As classes Bootstrap dos formulários vêm de
  um único mixin (`BootstrapFormMixin`).
- **SOLID** (no que faz sentido em Django):
  - *Responsabilidade única*: modelo cuida dos dados e das regras deles; `rules.py` cuida
    de permissão; a view só liga as peças.
  - *Aberto/fechado*: uma nova permissão é um novo predicado combinado com os existentes,
    sem mexer nas views.
  - *Inversão de dependência*: as views dependem de `has_perm`, não de "é do grupo X".
- **Ágil**: mudanças pequenas, cada uma com testes, integradas pela `main` com CI verde.

## Por que estas escolhas

As decisões maiores estão registradas em [`docs/adr/`](adr/), com contexto e alternativas.
