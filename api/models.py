from django.db import models


class Componente(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    tipo = models.CharField(max_length=100)
    voltaje = models.FloatField(null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "componentes"
        verbose_name = "componente"
        verbose_name_plural = "componentes"

    def __str__(self):
        return self.nombre


class HistorialDecision(models.Model):
    class Tipo(models.TextChoices):
        DERECHA = "derecha", "Derecha"
        IZQUIERDA = "izquierda", "Izquierda"
        ALTO = "alto", "Alto"
        AVANZAR = "avanzar", "Avanzar"

    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    senaleticas = models.CharField(
        "señaléticas", max_length=255,
        help_text="Imagen(es) detectada(s): nombre de archivo, ruta o URL.",
    )
    indice_confianza = models.FloatField("índice de confianza")

    class Meta:
        db_table = "historial_decisiones"
        verbose_name = "decisión"
        verbose_name_plural = "historial de decisiones"

    def __str__(self):
        return f"{self.tipo} ({self.indice_confianza})"


class TiempoReaccion(models.Model):
    t_avance_maximo = models.FloatField()
    t_avance_minimo = models.FloatField()
    t_detenerse_maximo = models.FloatField()
    t_detenerse_minimo = models.FloatField()
    latencia_ms = models.FloatField("latencia (ms)")
    # "Velocidad" quedó como pendiente en el pizarrón: se agrega cuando se defina.

    class Meta:
        db_table = "tiempos_reaccion"
        verbose_name = "tiempo de reacción"
        verbose_name_plural = "tiempos de reacción"

    def __str__(self):
        return f"Tiempos #{self.pk}"
