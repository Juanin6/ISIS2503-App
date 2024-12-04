from ..models import Usuario

def get_usuarios():
    queryset = Usuario.objects.all()
    return (queryset)

def create_usuario(form):
    measurement = form.save()
    measurement.save()
    return ()
def check_usuario_exists(user_id):
    # Comprobar si existe un usuario con el id proporcionado
    exists = Usuario.objects.filter(id=user_id).exists()
    return exists
