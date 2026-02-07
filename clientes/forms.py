from django.forms import ModelForm
from.models import Cliente, Poliza
from django import forms

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'fecha_nacimiento', 'telefono', 'correo', 'notas']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

class PolizaForm(ModelForm):
    class Meta:
        model = Poliza
        fields = ['numero_poliza', 'tipo_seguro', 'fecha_inicio', 'fecha_vencimiento', 'prima_total', 'forma_pago', 'fecha_ultimo_pago', 'estatus']

        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_ultimo_pago': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
