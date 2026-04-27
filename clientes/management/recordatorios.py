from django.core.management.base import BaseCommand
from clientes.models import Poliza
from datetime import date, timedelta
import pywhatkit as kit

class Command(BaseCommand):
    help = 'Envía recordatorios por WhatsApp usando pywhatkit'

    def handle(self, *args, **kwargs):
        hoy = date.today()
        objetivo = hoy + timedelta(days=30)
        #polizas que vencen en 30 días
        polizas = Poliza.objects.filter(estatus='Activa')
        for p in polizas:
            if p.proxima_renovacion == objetivo:
                try:
                    #mensaje de whasapp
                    mensaje = f"Estimado {p.cliente.nombre}, te recordamos que tu póliza de seguro de {p.tipo_seguro} vencerá en 30 días. ¡Evita quedarte sin cobertura!"
                    
                    #envia el mensaje, incluor lada del telefono y codigo de pais
                    kit.sendwhatmsg_instantly(
                        phone_no=p.cliente.telefono,
                        message=mensaje,
                        wait_time=15,
                        tab_close=True,
                        close_time=3
                    )
                    self.stdout.write(self.style.SUCCESS(f'WhatsApp enviado a {p.cliente.nombre}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error con {p.cliente.nombre}: {e}'))