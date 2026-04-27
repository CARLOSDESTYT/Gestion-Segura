import pywhatkit
from datetime import date, timedelta
from clientes.models import Poliza

def enviar_recordatorios_whatsapp():
    hoy = date.today()#fecha de hoy

    # Calcular la fecha de vencimiento en 30 días
    fecha_vencimiento_limite = hoy + timedelta(days=30)

    # Filtrar las pólizas que vencen exactamente en 30 días
    polizas_a_vencer = Poliza.objects.filter(fecha_vencimiento=fecha_vencimiento_limite)

    if not polizas_a_vencer:
        print("No hay pólizas que venzan en 30 días.")
        return

    for poliza in polizas_a_vencer:
        cliente = poliza.cliente
        if cliente.telefono:
            # Formatear el mensaje
            mensaje = f"Hola {cliente.nombre}, te recordamos que tu póliza de seguro {poliza.tipo_seguro} con número {poliza.numero_poliza} está por vencer en 30 días. ¡No olvides renovarla!"

            try:
                # Enviar el mensaje de WhatsApp
                pywhatkit.sendwhatmsg_instantly(
                    phone_no=f"+52{cliente.telefono}",  # Asegúrate de que el número de teléfono esté en el formato correcto
                    message=mensaje,
                )
                print(f"Mensaje enviado a {cliente.nombre} para la póliza {poliza.numero_poliza}")
            except Exception as e:
                print(f"No se pudo enviar el mensaje a {cliente.nombre}: {e}")
