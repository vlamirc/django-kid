# 0002. django-allauth para contas e 2FA

- Situação: aceita
- Data: 2026-09-24

## Contexto

O sistema precisa de cadastro, login, verificação de e-mail, recuperação de senha e
autenticação em dois fatores, com boas práticas de segurança.

## Decisão

Usar o **django-allauth** (módulos `account` e `mfa`): TOTP, códigos de recuperação e
WebAuthn. O login do admin passa pelo allauth (`secure_admin_login`). Staff e editores são
obrigados a ativar o 2FA por um middleware do projeto.

## Alternativas consideradas

- Views de autenticação do próprio Django: sem cadastro, verificação de e-mail ou 2FA.
- django-two-factor-auth / django-otp: bons, mas cobrem só o 2FA; seria preciso juntar
  vários pacotes para ter o que o allauth entrega sozinho.

## Consequências

Um pacote grande, mas muito usado e mantido há mais de dez anos. As telas foram adaptadas
ao layout do site em `templates/allauth/`.
