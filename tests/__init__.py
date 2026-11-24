import logging
from celery import current_app

# Los tests ejecutan las tareas .delay() al instante, sin Redis
current_app.conf.task_always_eager = True

# Silencia el warning de xhtml2pdf
logging.getLogger("xhtml2pdf").setLevel(logging.ERROR)