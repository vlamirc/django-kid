# 0005. Código em inglês, interface e docs em português

- Situação: aceita
- Data: 2026-09-24

## Contexto

A equipe fala português, mas o ecossistema (Django, pacotes, exemplos, IA) é em inglês.

## Decisão

- Nomes no código (variáveis, funções, classes, testes): inglês.
- Textos visíveis (interface, `verbose_name`, mensagens), comentários e documentação:
  português do Brasil, escritos direto no código, sem arquivos de tradução.

## Alternativas consideradas

- Tudo em português: mistura estranha com a API do Django (`get_queryset` com `titulo`).
- Interface com i18n (`gettext`) desde já: só compensa quando houver um segundo idioma.

## Consequências

Se um dia o sistema precisar de outro idioma, será preciso envolver os textos com
`gettext` e gerar os arquivos de tradução.
