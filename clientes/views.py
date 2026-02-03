from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import ClienteForm, PolizaForm
from .models import Cliente, Poliza
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('clientes')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'El usuario ya existe'})
        else:
            return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Las contraseñas no coinciden'})

@login_required
def clientes(request):
    clientes = Cliente.objects.filter(user=request.user)
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def editar_cliente(request, cliente_id):
    if request.method == 'GET':
        cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
        form = ClienteForm(instance=cliente)
        return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form})
    else:
        try:
            cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
            form = ClienteForm(request.POST, instance=cliente)
            form.save()
            return redirect('cliente_details', cliente.id)
        except ValueError:
            return render(request, 'editar_cliente.html', {'cliente': cliente, 'form': form, 'error': "Error actualizando asegurado"})

@login_required
def editar_poliza(request, cliente_id, poliza_id):
    # Obtenemos la póliza y el cliente
    poliza = get_object_or_404(Poliza, pk=poliza_id, cliente_id=cliente_id)
    cliente = poliza.cliente # Obtenemos el objeto cliente desde la póliza
    
    if request.method == 'GET':
        form = PolizaForm(instance=poliza)
        # IMPORTANTE: Asegúrate de usar 'editar_poliza.html' 
        # Si usas 'editar_cliente.html', fallará si ese template busca un objeto cliente
        return render(request, 'editar_poliza.html', {
            'poliza': poliza, 
            'cliente': cliente, # Agregamos esto para evitar el error de 'Reverse'
            'form': form
        })
    else:
        form = PolizaForm(request.POST, instance=poliza)
        if form.is_valid():
            form.save()
            return redirect('cliente_details', cliente_id=cliente.id)
        else:
            return render(request, 'editar_poliza.html', {
                'poliza': poliza, 
                'cliente': cliente,
                'form': form, 
                'error': "Error actualizando la póliza"
            })
        
@login_required
def cliente_details(request, cliente_id,):
    cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    polizas = Poliza.objects.filter(cliente=cliente)
    return render(request, 'cliente_details.html', {'cliente': cliente, 'polizas': polizas})


@login_required
def delete_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes')
    
@login_required
def delete_poliza(request, cliente_id, poliza_id):
    poliza = get_object_or_404(Poliza, pk=poliza_id, cliente_id=cliente_id, cliente__user=request.user)
    if request.method == 'POST':
        poliza.delete()
        return redirect('cliente_details', cliente_id=cliente_id)

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Usuario o contraseña incorrecto'})
        else:
            login(request, user)
            return redirect('clientes')

@login_required
def agregar_cliente(request):
    if request.method == 'GET':
        return render(request, 'agregar_cliente.html', {'form': ClienteForm})
    else:
        try:
            form = ClienteForm(request.POST)
            new_cliente = form.save(commit=False)
            new_cliente.user = request.user
            new_cliente.save()
            return redirect('clientes')
        except ValueError:
            return render(request, 'agregar_cliente.html', {'form': ClienteForm, 'error': 'Ingrese datos validos'})
        
@login_required
def añadir_poliza(request, cliente_id):
    client = get_object_or_404(Cliente, pk=cliente_id, user=request.user)
    if request.method == 'GET':
        return render(request, 'añadir_poliza.html', {'form': PolizaForm(), 'cliente': client})
    else:
        try:
            form = PolizaForm(request.POST)
            new_poliza = form.save(commit=False)
            new_poliza.cliente = client
            new_poliza.save()
            return redirect('cliente_details', client.id)
        except ValueError:
            return render(request, 'añadir_poliza.html', {'form': PolizaForm(), 'error': 'Ingrese datos validos'})
