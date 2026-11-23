from rest_framework import serializers

from .models import Componente, HistorialDecision, TiempoReaccion


class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = "__all__"


class HistorialDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialDecision
        fields = "__all__"


class TiempoReaccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TiempoReaccion
        fields = "__all__"
