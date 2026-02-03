from django.forms import ModelForm
from.models import Cliente, Poliza

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'fecha_nacimiento', 'telefono', 'correo', 'notas']

class PolizaForm(ModelForm):
    class Meta:
        model = Poliza
        fields = ['numero_poliza', 'tipo_seguro', 'fecha_inicio', 'fecha_vencimiento', 'prima_total', 'forma_pago', 'estatus']
    