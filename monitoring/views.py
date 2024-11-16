from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def inicio(request):
    return render(request, 'base.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)

def healthCheck(request):
    return HttpResponse('ok')

def custom_logout(request):
    # Cerrar sesión en Django
    logout(request)
    print("Ejecutando custom_logout...") 
    # Redirigir a Auth0 para cerrar la sesión sin el client_id
    return redirect(f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/v2/logout?returnTo=http%3A%2F%2F34.69.82.113%3A8080")
