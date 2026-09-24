# Como contribuir

## Fluxo

1. Atualize a `main` e crie uma branch: `git switch -c feature/agendar-posts`.
2. Trabalhe em ciclos de TDD (veja [docs/testes.md](docs/testes.md)).
3. Rode `make check` antes de subir.
4. Abra um Pull Request pequeno, preenchendo o modelo.
5. O CI precisa ficar verde e alguém do time precisa revisar.
6. Junte com **Squash and merge**, para a `main` ter um commit por mudança.

## Nomes de branch

`feature/...`, `fix/...`, `docs/...`, `chore/...` (manutenção, dependências).

## Mensagens de commit

Curtas, no imperativo, dizendo o que muda: `Adiciona agendamento de posts`.
Se precisar explicar o porquê, use o corpo da mensagem.

## Revisão de código

Quem revisa olha, nesta ordem: o comportamento está certo e testado? A autorização está
em `rules.py`? O código está simples? A documentação foi atualizada?

Pedir ajuda da IA para revisar é bem-vindo (veja [docs/ia.md](docs/ia.md)), mas a
aprovação é de uma pessoa.

## Regras da main

Recomendamos proteger a `main` no GitHub (Settings > Branches): exigir PR, CI verde
(jobs Lint, Testes e Ambiente Docker) e uma aprovação.
