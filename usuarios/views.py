from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UsuarioForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from .forms import UsuarioForm
from .logic.usuario_logic import get_usuarios, create_usuario
from .models import Usuario
from django.http import JsonResponse

# Vista para listar usuarios
def usuario_list(request):

        usuarios = get_usuarios()
        context = {
            'usuario_list': usuarios
        }
        return render(request, 'Usuario/usuarios.html', context)

# Vista para crear usuarios
def usuario_create(request):  
    if request.method == 'POST':
        form = UsuarioForm(request.POST)  
        if form.is_valid():
            create_usuario(form)  
            messages.add_message(request, messages.SUCCESS, 'Successfully created usuario')  
            return HttpResponseRedirect(reverse('usuarioCreate'))  
        else:
            print(form.errors)
    else:
        form = UsuarioForm()  

    context = {
        'form': form,
    }
    return render(request, 'Usuario/usuarioCreate.html', context)  
# Vista de inicio de sesión
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        try:
            # Autenticar al usuario
            user = Usuario.objects.get(correo=correo, contrasena=contrasena)
            request.session['usuario_id'] = user.id
            
            # Redirigir basado en el tipo de usuario
            if user.tipoUsuario == 'admin':
                return redirect('admin_dashboard')  # Redirige al dashboard de administrador
            else:
                return redirect('user_reports')  # Redirige a la página de reportes para usuarios normales
        except Usuario.DoesNotExist:
            # Si el usuario no existe, mostrar error
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'login.html')

# Vista para cerrar sesión
def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('inicio')


# Página de reportes para usuarios normales
def user_reports(request):
    reports = []  # Lógica para obtener reportes (puedes agregar aquí la lógica real)
    return render(request, 'user_reports.html', {'reports': reports})


def check_usuario_exists(request, user_id):
    try:
        # Intentamos obtener el usuario con el id
        usuario = Usuario.objects.get(id=user_id)
        # Si existe, devolvemos sus datos
        usuario_data = {
            "response":'true' 
        }
        return JsonResponse(usuario_data)
    except Usuario.DoesNotExist:
        # Si no existe, devolvemos un error 404
        return JsonResponse({'response':'false'}, status=404)


def verificar_admin(request, contrasena_ingresada):
    # Contraseña almacenada del administrador
    contrasena_admin = "admin_secreta123"  # Reemplaza con una contraseña segura

    # Verificar si la contraseña ingresada coincide con la del administrador
    if contrasena_ingresada == contrasena_admin:
        # Si es correcta, responder con éxito
        return JsonResponse({"response": "true", "message": "Acceso concedido"})
    else:
        # Si es incorrecta, responder con error 403
        return JsonResponse({"response": "false", "message": "Contraseña incorrecta"}, status=403)