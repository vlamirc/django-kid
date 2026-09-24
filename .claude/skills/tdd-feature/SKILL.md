---
name: tdd-feature
description: Implementar uma funcionalidade nova neste projeto Django com TDD, incluindo modelo, regras de autorização, views, templates e testes. Use quando pedirem uma funcionalidade, tela ou regra nova no blog.
---

# Funcionalidade nova com TDD

Siga os passos em ordem. Não pule o passo 2: ver o teste falhar prova que ele testa algo.

1. **Entenda o pedido** em uma frase do ponto de vista do usuário
   ("Como autor, quero X para Y"). Se algo for ambíguo, escolha o mais simples e diga qual.
2. **Escreva os testes primeiro**, no `tests/` da app:
   - `test_models.py` para regras do modelo e do QuerySet;
   - `test_rules.py` para cada permissão nova, em tabela (parametrize) cobrindo
     anônimo, leitor, autor dono, outro autor, editor e superusuário;
   - `test_views.py` para o comportamento HTTP (status, redirecionamento, conteúdo).
   Use as factories (`apps/*/tests/factories.py`) e as fixtures do `conftest.py`.
   Rode `make test` e confirme que os testes novos **falham pelo motivo certo**.
3. **Implemente o mínimo** para os testes passarem:
   - modelo e migração (`make migrations`, revise o arquivo gerado);
   - predicados em `rules.py` e `Meta.rules_permissions`;
   - view com `PermissionRequiredMixin` (de `rules.contrib.views`);
   - template estendendo `base.html`, formulário com `BootstrapFormMixin`;
   - URL com nome, em português (`posts/novo/`).
4. **Refatore** com os testes verdes: nomes claros, sem duplicação, views finas.
5. **Verifique**: `make check` (lint, 100% de cobertura, migrações em dia).
6. **Documente** em `docs/` se mudou algo para quem desenvolve, e registre uma
   decisão de arquitetura nova em `docs/adr/`.
