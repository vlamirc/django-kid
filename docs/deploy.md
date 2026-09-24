# Deploy

> Nada foi publicado ainda. Este documento é o plano; o deploy acontece quando você decidir.

## A recomendação: Render

O [Render](https://render.com) é o caminho mais simples para este projeto:

- lê o `render.yaml` do repositório e cria **a aplicação e o PostgreSQL de uma vez**;
- faz deploy automático a cada push na `main`;
- HTTPS e domínio `*.onrender.com` incluídos;
- tem plano gratuito para experimentar.

Limitações do plano gratuito: a aplicação "dorme" depois de 15 minutos sem acesso (o
primeiro acesso seguinte demora uns segundos) e o banco gratuito expira depois de 30 dias.
Para algo real, use os planos pagos mais baratos da aplicação e do banco.

### Passo a passo

1. Crie uma conta no Render entrando com o GitHub.
2. **New > Blueprint** e escolha o repositório `django-kid`.
3. O Render mostra o que vai criar (serviço `django-kid` e banco `django-kid-db`). Confirme.
4. Preencha as variáveis marcadas como manuais:
   - `EMAIL_URL`: SMTP de um provedor de e-mail transacional (Brevo, Resend, Amazon SES,
     Mailgun...), no formato `smtp+tls://usuario:senha@host:587`. Sem isso os e-mails
     de verificação não saem e ninguém consegue terminar o cadastro.
   - `DEFAULT_FROM_EMAIL`: por exemplo `Django Kid <nao-responda@seudominio.com>`.
5. Espere o primeiro deploy. As migrações rodam sozinhas a cada deploy (`scripts/start-prod.sh`).
6. Crie o administrador. O plano gratuito não tem **Shell**, então use variáveis de ambiente:
   1. Em **Environment** do serviço, adicione `DJANGO_SUPERUSER_EMAIL`,
      `DJANGO_SUPERUSER_PASSWORD` (12 caracteres ou mais) e, se quiser,
      `DJANGO_SUPERUSER_USERNAME` (o padrão é a parte do e-mail antes do `@`).
   2. Salve. O Render reinicia o serviço e o `scripts/start-prod.sh` roda
      `python manage.py ensure_superuser`, que cria o administrador com o e-mail já
      verificado (não precisa de SMTP para esse primeiro login). Veja nos **Logs** a linha
      `ensure_superuser: administrador ... criado.`
   3. Entre no site e ative o 2FA; o `/admin/` pede isso antes de abrir.
   4. Apague `DJANGO_SUPERUSER_PASSWORD` do painel. O comando nunca altera um usuário que
      já existe, então deixar as variáveis não troca a senha, mas não há por que guardar a senha ali.

   Nos planos pagos, o **Shell** também serve: `python manage.py createsuperuser`.

### Domínio próprio

Em **Settings > Custom Domains** do serviço, adicione o domínio e ajuste as variáveis:
`ALLOWED_HOSTS=meusite.com.br` e `CSRF_TRUSTED_ORIGINS=https://meusite.com.br`.

## Como a aplicação está preparada

Nada disso é específico do Render; vale para qualquer plataforma:

- **Uma imagem Docker** (`Dockerfile`, estágio `prod`): roda com usuário sem privilégios,
  já com os arquivos estáticos coletados.
- **Configuração só por variáveis de ambiente** (veja `docs/desenvolvimento.md`).
- **Arquivos estáticos pelo WhiteNoise**, com compressão e cache longo; não precisa de Nginx nem de CDN.
- **Gunicorn** como servidor, na porta da variável `PORT`.
- **Health check** em `/healthz/` (verifica também o banco).
- **Logs no stdout**, que a plataforma coleta.
- **Migrações automáticas** ao iniciar, e administrador criado por variáveis de ambiente (`ensure_superuser`).

## Alternativas

| Plataforma | Quando considerar |
| --- | --- |
| [Railway](https://railway.com) | Parecido com o Render, cobra por uso. Usa o mesmo Dockerfile |
| [Fly.io](https://fly.io) | Servidores perto do Brasil (região `gru`). Precisa de um `fly.toml` |
| VPS (DigitalOcean, Hetzner, Magalu Cloud) com [Coolify](https://coolify.io) ou [Kamal](https://kamal-deploy.org) | Mais controle e custo menor, mais trabalho de manutenção |
| AWS / Google Cloud / Azure | Quando a empresa já usa; mais complexo |

## Checklist antes de abrir para o público

- [ ] `DEBUG` não está definido (ou está `False`)
- [ ] `SECRET_KEY` gerada pela plataforma, nunca a do `.env.example`
- [ ] E-mail transacional configurado e testado (cadastro e "esqueci minha senha")
- [ ] Administrador criado e com 2FA ativo
- [ ] Backups automáticos do banco ligados (planos pagos do Render fazem isso)
