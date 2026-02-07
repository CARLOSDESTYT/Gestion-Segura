from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    # Solo datos personales y de contacto
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notas = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
    
class Poliza(models.Model):
    TIPO_SEGURO_CHOICES = [
        ('Vida', 'Vida'),
        ('Auto', 'Auto'),
        ('Gastos médicos', 'Gastos médicos'),
    ]

    FORMA_PAGO_CHOICES = [
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    ]

    ESTATUS_CHOICES = [
        ('Activa', 'Activa'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='polizas')
    
    numero_poliza = models.CharField(max_length=50, unique=True)
    tipo_seguro = models.CharField(max_length=50, choices=TIPO_SEGURO_CHOICES) # Ej: Vida, Auto, Gastos Médicos
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    prima_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=30, choices=FORMA_PAGO_CHOICES)
    fecha_ultimo_pago = models.DateField(null=True, blank=True)
    estatus = models.CharField(max_length=20, default='Activa', choices=ESTATUS_CHOICES)

    def __str__(self):
        return f"{self.tipo_seguro} - {self.numero_poliza}"
    
    @property
    def proxima_renovacion(self):
        hoy = date.today()
        inicio = self.fecha_inicio

        if inicio > hoy:
            return inicio

        if self.forma_pago == 'Anual':
            intervalo = relativedelta(years=1)
        else:  # Semestral
            intervalo = relativedelta(months=6)

        proxima = inicio
        # Cambiamos '<=' por '<'
        # Así, si 'proxima' es igual a 'hoy', el bucle se detiene 
        # y devuelve la fecha de hoy como día de renovación.
        while proxima < hoy:
            proxima += intervalo
            
        return proxima

    @property
    def ultima_renovacion(self):
        proxima = self.proxima_renovacion
        hoy = date.today()
        inicio = self.fecha_inicio

        if inicio >= hoy:
            return inicio
        
        if self.forma_pago == 'Anual':
            return proxima - relativedelta(years=1)
        else:  # Semestral
            return proxima - relativedelta(months=6)
    
    @property
    def esta_al_dia(self):
        if not self.fecha_ultimo_pago:
            return False
        
        proxima = self.proxima_renovacion
        if self.forma_pago == 'Anual':
            estado = proxima - relativedelta(years=1)
        else:
            estado = proxima - relativedelta(months=6)

        return self.fecha_ultimo_pago >= estado
