# Contas e segurança

## Login e cadastro

Feitos com o [django-allauth](https://docs.allauth.org/), o pacote de autenticação mais
usado do ecossistema Django. As telas ficam em `/contas/`:

| Endereço | Tela |
| --- | --- |
| `/contas/signup/` | Cadastro |
| `/contas/login/` | Login (por e-mail) |
| `/contas/password/reset/` | Esqueci minha senha |
| `/contas/email/` | Gerenciar e-mails |
| `/contas/password/change/` | Trocar senha |
| `/contas/2fa/` | Autenticação em dois fatores |

- O e-mail precisa ser **verificado** antes do primeiro login.
- O allauth limita tentativas de login e de envio de e-mails (proteção contra força bruta).

## Senhas fortes

- Mínimo de **12 caracteres**, não pode ser só números, nem uma senha comum, nem
  parecida com o nome ou e-mail do usuário (`AUTH_PASSWORD_VALIDATORS`).
- Guardadas com **Argon2**, o algoritmo recomendado pela documentação do Django.

## Autenticação em dois fatores (2FA)

Qualquer usuário pode ativar em "Minha conta > Autenticação em dois fatores":

- **App autenticador (TOTP)**: Google Authenticator, Authy, 1Password etc.
- **Códigos de recuperação**: para quando o celular não estiver à mão.
- **Chaves de segurança (WebAuthn)**: YubiKey, Touch ID, Windows Hello.

**Staff e editores são obrigados a ativar o 2FA.** Enquanto não ativam, qualquer página
os leva para a tela de 2FA (veja `apps/accounts/middleware.py`). Isso vale também para o
admin, cujo login passa pelo allauth.

## Produção

Com `DEBUG=False` o projeto liga automaticamente:

- redirecionamento para HTTPS e HSTS;
- cookies de sessão e CSRF só por HTTPS;
- proteção contra clickjacking, `nosniff` e `Referrer-Policy`.

O CI roda `manage.py check --deploy` para garantir que essas configurações continuam ativas.

## Cuidados no dia a dia

- Segredos só em variáveis de ambiente. O `.env` não vai para o Git.
- Texto digitado por usuários é sempre escapado nos templates. Não use `|safe` nele.
- Dependências são atualizadas pelo Dependabot; leia o changelog de atualizações grandes.
