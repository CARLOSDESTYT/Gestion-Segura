from django.db import models
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
    # Relación: Un cliente puede tener muchas pólizas
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='polizas')
    
    # Datos específicos del contrato
    numero_poliza = models.CharField(max_length=50, unique=True)
    tipo_seguro = models.CharField(max_length=50) # Ej: Vida, Auto, Gastos Médicos
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    prima_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=30)
    estatus = models.CharField(max_length=20, default='Activa')

    def __str__(self):
        return f"{self.tipo_seguro} - {self.numero_poliza}"