# 0003. django-rules para autorização

- Situação: aceita
- Data: 2026-09-24

## Contexto

Precisamos de permissões por objeto ("só o autor edita o próprio post") que sirvam para o
sistema inteiro, fáceis de ler e de testar.

## Decisão

Papéis são `Group`s do Django; as regras são predicados do **django-rules** em arquivos
`rules.py`, ligados às permissões padrão (`add`, `view`, `change`, `delete`) via
`Meta.rules_permissions`. Tudo é verificado com `has_perm`.

## Alternativas consideradas

- Permissões de modelo do Django puras: não sabem nada sobre o objeto (quem é o dono).
- django-guardian: guarda permissões por objeto no banco; útil quando cada objeto tem
  uma lista de acesso própria, mas pesado para regras que são sempre as mesmas.

## Consequências

As regras ficam no código, versionadas e testadas em tabela. Se um dia for preciso
permissão por objeto definida pelo usuário (compartilhar um post com alguém), dá para
somar o guardian sem jogar fora o que existe.
