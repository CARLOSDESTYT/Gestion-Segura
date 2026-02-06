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
    estatus = models.CharField(max_length=20, default='Activa', choices=ESTATUS_CHOICES)

    def __str__(self):
        return f"{self.tipo_seguro} - {self.numero_poliza}"
    
    @property
    def proxima_renovacion(self):
        hoy = date.today()
        inicio = self.fecha_inicio

        # Si la fecha de inicio es en el futuro, esa es la próxima renovación
        if inicio > hoy:
            return inicio

        # Calculamos la diferencia en años y meses
        diff = relativedelta(hoy, inicio)
        
        if self.forma_pago == 'Anual':
            # Sumamos los años transcurridos + 1 para llegar al siguiente aniversario
            aniversario = inicio + relativedelta(years=diff.years)
            if aniversario < hoy:
                aniversario += relativedelta(years=1)
            return aniversario

        else: # Semestral
            # Calculamos total de meses transcurridos
            total_meses = (diff.years * 12) + diff.months
            # Calculamos cuántos semestres han pasado (división entera) + 1
            cantidad_semestres = (total_meses // 6) + 1
            return inicio + relativedelta(months=cantidad_semestres * 6)
        
    @property
    def esta_al_dia(self):
        if not self.fecha_ultimo_pago_realizado:
            return False
        
        return self.fecha_ultimo_pago_realizado <= self.proxima_renovacion