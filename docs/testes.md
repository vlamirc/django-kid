# Testes e TDD

## O ciclo

1. **Vermelho**: escreva um teste para o comportamento que você quer. Rode e veja falhar.
2. **Verde**: escreva o mínimo de código para o teste passar.
3. **Refatore**: melhore o código com a segurança de que os testes continuam verdes.

Ver o teste falhar é importante: prova que ele realmente testa o que você acha que testa.

## Rodando

```bash
make test                                   # tudo, com cobertura
docker compose run --rm web pytest -k slug  # só testes com "slug" no nome
docker compose run --rm web pytest apps/blog/tests/test_views.py -x  # para no primeiro erro
```

A cobertura mínima é **100%** (linhas e desvios). Se algo não merece teste, marque
com `# pragma: no cover` e explique o motivo no comentário. Cobertura alta não garante
bons testes, mas cobertura baixa garante que tem código sem teste.

## Onde fica cada teste

Cada app tem uma pasta `tests/`:

| Arquivo | Testa |
| --- | --- |
| `factories.py` | Não é teste: cria objetos válidos com factory_boy |
| `test_models.py` | Regras do modelo e do QuerySet |
| `test_rules.py` | Permissões, em formato de tabela |
| `test_views.py` | Comportamento HTTP: status, redirecionamento, conteúdo |
| `test_forms.py` | Formulários |

Fixtures compartilhadas (`reader`, `author`, `other_author`, `editor`, `superuser`)
ficam no `conftest.py` da raiz.

## Boas práticas usadas aqui

- **Teste comportamento, não implementação.** "Leitor não vê rascunho" é melhor que
  "a view chama `has_perm`".
- **Nomes que contam a história**: `test_other_author_is_forbidden`.
- **Factories em vez de fixtures JSON.** `PostFactory(status=Post.Status.DRAFT)` deixa
  claro o que importa no teste.
- **Tabela de permissões** com `pytest.mark.parametrize`: cada papel, cada ação, um resultado.
- **Contagem de queries** nas listas (`django_assert_num_queries`) para pegar problemas de N+1.
- **Banco de verdade**: os testes rodam no PostgreSQL, como a produção.
- Os testes usam um hash de senha rápido (veja `conftest.py`); a produção usa Argon2.
