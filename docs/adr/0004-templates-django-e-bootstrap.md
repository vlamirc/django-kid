# 0004. Templates do Django com Bootstrap, sem SPA

- Situação: aceita
- Data: 2026-09-24

## Contexto

O foco é aprender Django e ter uma interface boa sem manter dois projetos (back e front).

## Decisão

Páginas renderizadas pelo Django com o tema **Start Bootstrap Clean Blog** (Bootstrap 5,
MIT), copiado para `static/theme/` sem etapa de build de front-end.

## Alternativas consideradas

- React/Vue com API: dois projetos, duas pilhas, muito mais para aprender e manter.
- Tailwind: exige etapa de build; o Bootstrap tem mais temas prontos e documentação em português.

## Consequências

Simples de entender e de publicar. Se surgir necessidade de interatividade, o próximo
passo natural é o [htmx](https://htmx.org), que continua usando templates do Django.
