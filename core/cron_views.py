# core/cron_views.py
import hmac
import os

from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET


@require_GET
def enviar_reporte_diario(request):
    """Genera y envía el reporte diario. Protegida con un token secreto.

    Con ?forzar=1 envía de inmediato. Sin él, solo envía si la hora actual
    cae en la ventana de 10 minutos que empieza en REPORTE_HORA:REPORTE_MINUTO.
    """
    esperado = settings.CRON_TOKEN.encode()
    recibido = request.GET.get('token', '').encode()

    if not esperado or not hmac.compare_digest(recibido, esperado):
        return JsonResponse({'error': 'no autorizado'}, status=403)

    if request.GET.get('forzar') != '1':
        hora_cfg = int(os.environ.get('REPORTE_HORA', '20'))
        minuto_cfg = int(os.environ.get('REPORTE_MINUTO', '0'))
        ahora = timezone.localtime()
        en_ventana = (
            ahora.hour == hora_cfg
            and minuto_cfg <= ahora.minute < minuto_cfg + 10
        )
        if not en_ventana:
            return JsonResponse({'ok': True, 'omitido': 'fuera de horario'})

    from ventas.tasks import reporte_ventas_diario
    resultado = reporte_ventas_diario.apply().get()   # sin Celery ni Redis
    return JsonResponse({'ok': True, 'resultado': resultado})