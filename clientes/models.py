from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

# Modelo de Asegurado
class Cliente(models.Model):
    # Solo datos personales y de contacto básicos
    nombre = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Relación con el usuario del sistema (quién es dueño del cliente)
    notas = models.TextField(blank=True) # Campo opcional para notas adicionales

    def __str__(self): # Representación en texto del objeto para admin
        return self.nombre


# Modelo Poliza
class Poliza(models.Model):
    # Tipos de seguro disponibles
    TIPO_SEGURO_CHOICES = [
        ('Vida', 'Vida'),
        ('Auto', 'Auto'),
        ('Gastos médicos', 'Gastos médicos'),
    ]

    # Formas de pago disponibles
    FORMA_PAGO_CHOICES = [
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
    ]

    # Estados posibles de la póliza
    ESTATUS_CHOICES = [
        ('Activa', 'Activa'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    # Relación: una póliza pertenece a un cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='polizas')
    
    # Datos principales de la póliza
    numero_poliza = models.CharField(max_length=50, unique=True)
    tipo_seguro = models.CharField(max_length=50, choices=TIPO_SEGURO_CHOICES) # Ej: Vida, Auto, Gastos Médicos
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField()
    prima_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=30, choices=FORMA_PAGO_CHOICES)
    fecha_ultimo_pago = models.DateField(null=True, blank=True) # Fecha del último pago realizado (puede ser nulo)
    estatus = models.CharField(max_length=20, default='Activa', choices=ESTATUS_CHOICES) # Estado actual de la póliza

    def __str__(self):  # Representación en texto del objeto para admin
        return f"{self.tipo_seguro} - {self.numero_poliza}"
    

    # Calcula la próxima fecha en la que se debe pagar/renovar
    @property
    def proxima_renovacion(self):
        # Si la póliza está cancelada, no hay renovaciones
        if self.estatus == 'Cancelada':
            return None

        hoy = date.today()
        inicio = self.fecha_inicio

        # Si la póliza aún no inicia, la próxima renovación es su inicio
        if inicio > hoy:
            return inicio

        # Define el intervalo según la forma de pago
        if self.forma_pago == 'Anual':
            intervalo = relativedelta(years=1)
        else:  # Semestral
            intervalo = relativedelta(months=6)

        # Se parte desde la fecha de inicio
        proxima = inicio
        # Avanza en intervalos hasta encontrar la fecha más cercana >= hoy
        # Usamos '<=' por '<'
        # Así, si 'proxima' es igual a 'hoy', el bucle se detiene y devuelve la fecha de hoy como día de renovación.
        while proxima < hoy:
            proxima += intervalo
            
        return proxima


    # Calcula la última fecha en la que debió pagar
    @property
    def ultima_renovacion(self):
        proxima = self.proxima_renovacion
        hoy = date.today()
        inicio = self.fecha_inicio

        # Si aún no inicia, no hay pagos anteriores
        if inicio >= hoy:
            return inicio
        
        # Resta un intervalo a la próxima renovación
        if self.forma_pago == 'Anual':
            return proxima - relativedelta(years=1)
        else:  # Semestral
            return proxima - relativedelta(months=6)
    

    # Indica si la póliza está al corriente en pagos
    # Ejemplo de uso
    # {% if poliza.esta_al_dia %}
    #     ✅ Al corriente
    # {% else %}
    #     ⚠️ Pendiente
    # {% endif %}
    # if not poliza.esta_al_dia:
    #   enviar_recordatorio(poliza)
    @property
    def esta_al_dia(self):
        # Si nunca ha pagado, no está al día
        if not self.fecha_ultimo_pago:
            return False
        
        proxima = self.proxima_renovacion

        # Calcula desde cuándo debería estar pagado el periodo actual
        if self.forma_pago == 'Anual':
            estado = proxima - relativedelta(years=1)
        else:
            estado = proxima - relativedelta(months=6)

        # Está al día si el último pago cubre el periodo actual
        return self.fecha_ultimo_pago >= estado
