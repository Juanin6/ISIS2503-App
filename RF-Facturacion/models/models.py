from datetime import datetime

class Factura:
    def __init__(self, id, usuario, total, fecha):
        self.id = id
        self.usuario = usuario
        self.total = total
        self.fecha = fecha or datetime.now()
