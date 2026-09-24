from allauth.mfa.utils import is_mfa_enabled
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from apps.accounts.roles import is_privileged

# Caminhos liberados mesmo sem 2FA: as próprias telas de conta (onde o 2FA é
# ativado e onde se faz logout) e a verificação de saúde.
EXEMPT_PATH_PREFIXES = ("/contas/", "/healthz/")


class RequireMFAForPrivilegedUsersMiddleware:
    """Obriga staff e editores a ativarem o 2FA antes de usar o sistema."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self._must_enable_mfa(request):
            messages.warning(
                request,
                "Sua conta tem permissões especiais. Ative a autenticação em "
                "dois fatores para continuar.",
            )
            return redirect("mfa_index")
        return self.get_response(request)

    @staticmethod
    def _must_enable_mfa(request) -> bool:
        user = request.user
        return (
            settings.MFA_REQUIRED_FOR_PRIVILEGED_USERS
            and user.is_authenticated
            and not request.path.startswith((*EXEMPT_PATH_PREFIXES, settings.STATIC_URL))
            and is_privileged(user)
            and not is_mfa_enabled(user)
        )
