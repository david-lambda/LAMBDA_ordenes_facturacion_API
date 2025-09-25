import traceback
from threading import Thread
from django.core.mail.backends.smtp import EmailBackend 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings


def enviar_correo(asunto:str, plantilla:str, contexto:dict, destinatarios:list, adjuntos:list=[]):
    def enviar():
        """
        Envía un correo electrónico utilizando una plantilla HTML.

        :param asunto: Asunto del correo electrónico.
        :param plantilla: Nombre de la plantilla HTML a utilizar.
        :param contexto: Diccionario con el contexto para renderizar la plantilla.
        :param destinatarios: Lista de direcciones de correo electrónico de los destinatarios.
        :param adjuntos: Lista de rutas de archivos a adjuntar al correo electrónico.
        """
        try:
            template = get_template(plantilla)
            msg = template.render(contexto)

            email = EmailMultiAlternatives(
                subject=asunto,
                body=msg,
                from_email=settings.EMAIL_HOST_USER,
                to=destinatarios,
            )

            email.attach_alternative(msg, "text/html")

            for archivo in adjuntos:
                email.attach(archivo["filename"], archivo["bytes"], archivo["mimetype"])

            backend = EmailBackend(
                use_tls=settings.EMAIL_USE_TLS,
                time_out=30
            )

            email.connection = backend
            email.send(fail_silently=False)
        except:
            traceback.print_exc()
    
    hilo = Thread(target=enviar)
    hilo.start()