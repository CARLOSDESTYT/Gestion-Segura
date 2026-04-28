from django.forms import ModelForm
from.models import Cliente, Poliza
from django import forms

# Formulario para crear y editar cliente con datos del cliente
# Widgets para registrar fechas más fácil
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'fecha_nacimiento', 'telefono', 'correo', 'notas']

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

# Formulario para crear y editar poliza relacionandolo con cliente
# Widgets para registrar fechas más fácil
class PolizaForm(ModelForm):
    class Meta:
        model = Poliza
        fields = ['numero_poliza', 'tipo_seguro', 'fecha_inicio', 'fecha_vencimiento', 'prima_total', 'forma_pago', 'fecha_ultimo_pago', 'estatus']

        widgets = {
            'tipo_seguro': forms.Select(attrs={'class': 'campo_input'}),
            'estatus': forms.Select(attrs={'class': 'campo_input'}),
            'forma_pago': forms.Select(attrs={'class': 'campo_input'}),

            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'fecha_ultimo_pago': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
