from django.contrib import admin

from .models import Componente, HistorialDecision, TiempoReaccion

admin.site.register(Componente)
admin.site.register(HistorialDecision)
admin.site.register(TiempoReaccion)
