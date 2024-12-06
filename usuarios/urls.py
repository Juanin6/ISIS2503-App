from django.urls import path
from . import views

urlpatterns = [
    path('api/usuario/<int:user_id>/', views.check_usuario_exists, name='usuario_exists'),
]
