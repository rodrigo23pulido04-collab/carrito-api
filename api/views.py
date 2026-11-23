from rest_framework import viewsets

from .models import Componente, HistorialDecision, TiempoReaccion
from .serializers import (
    ComponenteSerializer,
    HistorialDecisionSerializer,
    TiempoReaccionSerializer,
)


# ReadOnlyModelViewSet: solo GET (listar y detalle). POST/PUT/PATCH/DELETE devuelven 405.
class ComponenteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Componente.objects.all().order_by("nombre")
    serializer_class = ComponenteSerializer
    lookup_value_regex = "[^/]+"  # permite nombres con espacios, puntos, etc.


class HistorialDecisionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistorialDecision.objects.all().order_by("-id")
    serializer_class = HistorialDecisionSerializer


class TiempoReaccionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TiempoReaccion.objects.all().order_by("-id")
    serializer_class = TiempoReaccionSerializer
