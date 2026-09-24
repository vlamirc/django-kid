from django.db import connection
from django.http import JsonResponse


def healthz(request):
    """Verificação de saúde usada pela plataforma de deploy."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
    return JsonResponse({"status": "ok"})
