# 0001. Django LTS e poucas dependências

- Situação: aceita
- Data: 2026-09-24

## Contexto

O projeto precisa ser mantido por mais de quinze anos, por equipes que vão mudar.

## Decisão

- Usar sempre uma versão **LTS** do Django (hoje a 5.2, com suporte até abril de 2028) e
  migrar para a LTS seguinte (6.2, prevista para 2027) dentro da janela de suporte.
- Só adicionar pacotes **populares, ativamente mantidos**, que resolvem algo que o Django
  não resolve. Hoje: django-allauth, django-rules, django-environ, WhiteNoise, Gunicorn e psycopg.
- Configuração por variáveis de ambiente em um único `settings.py`.
- Dependências gerenciadas com `uv` e travadas no `uv.lock`.

## Alternativas consideradas

- Acompanhar sempre a última versão do Django: mais novidades, mas atualizações a cada 8 meses.
- Settings separados por ambiente (`base.py`, `dev.py`, `prod.py`): mais arquivos para
  manter; as diferenças entre ambientes já cabem em variáveis de ambiente.
- pip + requirements.txt: funciona, mas sem lock completo nem gestão da versão do Python.

## Consequências

Menos coisa para atualizar e menos risco de um pacote abandonado. Às vezes será preciso
escrever um pouco mais de código em vez de instalar um pacote.
