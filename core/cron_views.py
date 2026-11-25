# core/cron_views.py
import hmac

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def enviar_reporte_diario(request):
    """Genera y envía el reporte diario. Protegida con un token secreto."""
    esperado = settings.CRON_TOKEN.encode()
    recibido = request.GET.get('token', '').encode()

    # Sin token configurado o token incorrecto -> no hace nada
    if not esperado or not hmac.compare_digest(recibido, esperado):
        return JsonResponse({'error': 'no autorizado'}, status=403)

    from ventas.tasks import reporte_ventas_diario
    resultado = reporte_ventas_diario.apply().get()   # sin Celery ni Redis
    return JsonResponse({'ok': True, 'resultado': resultado})