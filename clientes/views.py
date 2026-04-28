from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ClienteForm, PolizaForm
from .models import Cliente, Poliza
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import timedelta



# Página PRINCIPAL
def home(request):
    return render(request, 'home.html')


# Página SIGNUP
# REVISAR QUÉ CAMBIÓ
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        # 1. Pasamos los datos del POST al formulario de Django
        form = UserCreationForm(request.POST)
        
        # 2. .is_valid() ejecuta TODAS las validaciones (longitud, claves comunes, etc.)
        if form.is_valid():
            user = form.save() # Guarda al usuario automáticamente con seguridad
            login(request, user)
            return redirect('clientes')
        else:
            # 3. Si no es válido, regresamos el formulario con los errores específicos
            return render(request, 'signup.html', {'form': form})


# Página SIGNOUT
@login_required
def signout(request):
    logout(request)
    return redirect('home')


# Página SIGNIN
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm}) # Manda la página
    else:
        # Toma username y password para verificar si coinciden con un usuario válido en la base de datos
        # Si las credenciales son correctas -> Devuelve el usuario, sino -> None
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecto'})
        else:
            login(request, user) # Inicia sesión
            return redirect('clientes') # Redirige


# Página ASEGURADOS
@login_required
def clientes(request):
    # Guarda todos los asegurados de la cuenta en una QuerySet
    clientes = Cliente.objects.filter(user=request.user)
    hoy = date.today()

    for cliente in clientes:
        cliente.es_cumple = (
            cliente.fecha_nacimiento.day == hoy.day and
            cliente.fecha_nacimiento.month == hoy.month
        )
    return render(request, 'clientes.html', {'clientes': clientes})


# Página de EDITAR CLIENTE
@login_required
def editar_cliente(request, cliente_id):
    # Si el asegurado pertenece al agente, guarda el cliente, si no redirigirlo a la página clientes
    try:
        cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    except:
        return redirect('clientes')
    # Mostrar el formulario del cliente
    if request.method == 'GET':
        form = ClienteForm(instance=cliente)
        return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form})
    # POST - Actualiza datos del asegurado mientras los datos sean validos
    else:
        try:
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('cliente_details', cliente.id)
        except ValueError:
            return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form, 'error': "Error actualizando asegurado"})


# Página EDITAR POLIZA
@login_required
def editar_poliza(request, cliente_id, poliza_id):
    # Si la poliza pertenece al cliente que pertenece al agente, guarda la poliza, si no redirigirlo a la página clientes
    try:
        poliza = get_object_or_404(Poliza, pk=poliza_id, cliente_id=cliente_id, cliente__user=request.user)
    except:
        return redirect('clientes')
    cliente = poliza.cliente
    # Mostrar el formulario de la poliza
    if request.method == 'GET':
        form = PolizaForm(instance=poliza)
        return render(request, 'editar_poliza.html', {'poliza': poliza, 'cliente': cliente, 'form': form})
    # POST - Actualiza datos de la poliza mientras los datos sean validos
    else:
        form = PolizaForm(request.POST, instance=poliza)
        if form.is_valid():
            form.save()
            return redirect('cliente_details', cliente_id=cliente.id)
        else:
            return render(request, 'editar_poliza.html', {'poliza': poliza, 'cliente': cliente, 'form': form, 'error': "Error actualizando la póliza"})
        

# Página DETALLES DEL CLIENTE
@login_required
def cliente_details(request, cliente_id,):
    # Si el cliente pertenece al agente, guarda el cliente, si no redirigirlo a la página clientes
    try:
        cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    except:
        return redirect('clientes')
    # Guarda las polizas del cliente
    polizas = Poliza.objects.filter(cliente=cliente)
    return render(request, 'cliente_details.html', {'cliente': cliente, 'polizas': polizas})


# ELIMINAR ASEGURADO
@login_required
def delete_cliente(request, cliente_id):
    # Si el cliente pertenece al agente, guarda el cliente, si no redirigirlo a la página clientes
    try:
        cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    except:
        return redirect('clientes')
    if request.method == 'POST': # Elimina cliente
        cliente.delete()
        return redirect('clientes')
    

# ELIMINAR POLIZA
@login_required
def delete_poliza(request, cliente_id, poliza_id):
    # Si la poliza pertenece al cliente que pertenece al agente, guarda la poliza, si no redirigirlo a la página clientes
    try:
        poliza = get_object_or_404(Poliza, pk=poliza_id, cliente_id=cliente_id, cliente__user=request.user)
    except:
        return redirect('clientes')
    if request.method == 'POST': # Elimina poliza
        poliza.delete()
        return redirect('cliente_details', cliente_id=cliente_id)


# AGREGAR ASEGURADO
@login_required
def agregar_cliente(request):
    if request.method == 'GET': # Mostrar página
        return render(request, 'agregar_cliente.html', {'form': ClienteForm})
    else:
        try:
            # Crea y guarda un objeto Cliente, si no ingresa datos validos, muestra un error
            form = ClienteForm(request.POST) # Recibe los datos del formulario
            new_cliente = form.save(commit=False) # Crea un objeto Cliente sin guardarlo (solo en memoria)
            new_cliente.user = request.user # Le asigna el usuario actual
            new_cliente.save() # Lo guarda en la base de datos
            return redirect('clientes')
        except ValueError:
            return render(request, 'agregar_cliente.html', {'form': ClienteForm, 'error': 'Ingrese datos validos'})
        

# AGREGAR POLIZA
@login_required
def agregar_poliza(request, cliente_id):
    # Si el asegurado pertenece al agente, manda el formulario, si no redirigirlo a la página clientes
    try:
        client = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    except:
        return redirect('clientes')
    if request.method == 'GET':
        return render(request, 'agregar_poliza.html', {'form': PolizaForm(), 'cliente': client})
    else:
        try:
            # Crea y guarda un objeto Poliza, si no ingresa datos validos, muestra un error
            form = PolizaForm(request.POST) # Recibe los datos del formulario
            new_poliza = form.save(commit=False) # Crea un objeto Poliza sin guardarlo (solo en memoria)
            new_poliza.cliente = client # Le asigna el cliente actual
            new_poliza.save() # Lo guarda en la base de datos
            return redirect('cliente_details', client.id)
        except ValueError:
            return render(request, 'agregar_poliza.html', {'form': PolizaForm, 'cliente': client, 'error': 'Ingrese datos validos'})


# Página DASHBOARD
@login_required
def dashboard(request):
    hoy = date.today() # Guarda la fecha de hoy
    fin_40_dias = hoy + timedelta(days=40) # Calcula qué día será en 40 días y lo guarda
    inicio_mes = hoy.replace(day=1) # Inicio del mes actual
    if hoy.month == 12: # Inicio del mes siguiente
        inicio_siguiente_mes = hoy.replace(year=hoy.year + 1, month=1, day=1)
    else:
        inicio_siguiente_mes = hoy.replace(month=hoy.month + 1, day=1)

    # Pólizas activas del usuario
    polizas = (
        Poliza.objects
        .filter(cliente__user=request.user, estatus__in=['Activa', 'Pendiente']) # Trae las pólizas del cliente del usuario actual atravesando relaciones con doble "_"
        .select_related('cliente') # Optimiza base de datos para traer datos del cliente
    )

    # Guarda polizas que se pagan este mes, en los proximos 40 días y separar los que se pagan hoy en listas separadas
    pagan_este_mes = []
    pagan_proximos_40_dias = []
    pagan_hoy = []

    for p in polizas:
        renovacion = p.proxima_renovacion # Calcula la proxima renovación de la poliza y guarda la fecha
        if renovacion is None:
            continue # Si no hay fecha de renovación, se ignora esta póliza

        # Caso 1: Se paga exactamente hoy
        if p.proxima_renovacion == hoy:
            pagan_hoy.append(p) # Se agrega a la lista pagan_hoy[]

        # Caso 2: Se paga en el mes actual
        # Se evalúan dos posibilidades: Renovado o por renovar este mes
        elif ((p.ultima_renovacion and inicio_mes <= p.ultima_renovacion < inicio_siguiente_mes) or (inicio_mes <= renovacion < inicio_siguiente_mes)):
            pagan_este_mes.append(p) # Se agrega a la lista pagan_este_mes[]

        # Caso 3: Se paga dentro de los próximos 40 días
        elif hoy <= renovacion <= fin_40_dias:
            pagan_proximos_40_dias.append(p) # Se agrega a la lista pagan_proximos_40_dias[]

    return render(request, 'dashboard.html', {'pagan_este_mes': pagan_este_mes, 'pagan_proximos_40_dias': pagan_proximos_40_dias, 'pagan_hoy': pagan_hoy,})
