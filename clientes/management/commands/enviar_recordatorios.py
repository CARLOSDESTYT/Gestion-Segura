from django.core.management.base import BaseCommand
from recordatorios import enviar_recordatorios_whatsapp

class Command(BaseCommand):
    help = 'Envía recordatorios de WhatsApp para pólizas que vencen en 30 días.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando el envío de recordatorios...'))
        enviar_recordatorios_whatsapp()
        self.stdout.write(self.style.SUCCESS('¡Envío de recordatorios completado!'))
