from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def generar_reporte(request):
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        # Aquí puedes manejar los datos, por ejemplo, generar el reporte con las fechas recibidas
        return render(request, 'reporte_generado.html', {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
    return render(request, 'generar_reporte.html')

def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        contraseña = request.POST.get('contraseña')
        # Aquí puedes manejar los datos, por ejemplo, crear un usuario con los datos recibidos
        return render(request, 'usuario_creado.html', {'nombre': nombre})
    return render(request, 'crear_usuario.html')
