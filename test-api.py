"""
Script para poblar la base de datos con datos de prueba.
Uso:
    python seed.py
    python seed.py --flush   # borra los datos existentes antes de insertar
"""

import os
import sys
import django
import argparse
import random

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <-- CAMBIA "tu_proyecto"
django.setup()

from django.db import transaction
from api.models import Componente, HistorialDecision, TiempoReaccion  # <-- CAMBIA "core" por tu app


# ---------------------------------------------------------------------------
# Datos de prueba
# ---------------------------------------------------------------------------

COMPONENTES = [
    {"nombre": "Arduino Uno R3",     "tipo": "Microcontrolador", "voltaje": 5.0,  "cantidad": 10, "descripcion": "Placa basada en ATmega328P, 14 pines digitales, 6 analógicos."},
    {"nombre": "Sensor HC-SR04",     "tipo": "Ultrasónico",      "voltaje": 5.0,  "cantidad": 25, "descripcion": "Sensor de distancia por ultrasonido, rango 2cm–400cm."},
    {"nombre": "L298N",              "tipo": "Puente H",         "voltaje": 12.0, "cantidad": 8,  "descripcion": "Driver para motores DC de doble canal."},
    {"nombre": "ESP32-WROOM-32",     "tipo": "Microcontrolador", "voltaje": 3.3,  "cantidad": 5,  "descripcion": "WiFi + Bluetooth integrado, 240 MHz."},
    {"nombre": "Batería LiPo 3S",    "tipo": "Alimentación",     "voltaje": 11.1, "cantidad": 4,  "descripcion": "2200 mAh, 3 celdas en serie."},
    {"nombre": "Motor DC 12V",       "tipo": "Actuador",         "voltaje": 12.0, "cantidad": 6,  "descripcion": "Motor con caja reductora, 200 RPM."},
    {"nombre": "Resistencia 220Ω",   "tipo": "Pasivo",           "voltaje": None, "cantidad": 200, "descripcion": "Resistencia de carbón 1/4W."},
    {"nombre": "LED Rojo 5mm",       "tipo": "Óptico",           "voltaje": 2.0,  "cantidad": 150, "descripcion": "LED difuso, 20 mA."},
    {"nombre": "Módulo Relé 5V",     "tipo": "Actuador",         "voltaje": 5.0,  "cantidad": 12, "descripcion": "Relé de 1 canal, optoacoplado."},
    {"nombre": "Sensor IR TCRT5000", "tipo": "Óptico",           "voltaje": 5.0,  "cantidad": 30, "descripcion": "Sensor infrarrojo reflectivo para línea."},
    {"nombre": "Servo SG90",         "tipo": "Actuador",         "voltaje": 5.0,  "cantidad": 15, "descripcion": "Servomotor 9g, 180°."},
    {"nombre": "Cámara PiCam v2",    "tipo": "Óptico",           "voltaje": 3.3,  "cantidad": 3,  "descripcion": "Cámara 8MP para Raspberry Pi."},
    {"nombre": "Raspberry Pi 4B",    "tipo": "Microcontrolador", "voltaje": 5.0,  "cantidad": 2,  "descripcion": "4GB RAM, quad-core 1.5 GHz."},
    {"nombre": "Cable Dupont M-M",   "tipo": "Conexión",         "voltaje": None, "cantidad": 300, "descripcion": "Pack de 40 cables, 20cm."},
    {"nombre": "Protoboard 830",     "tipo": "Conexión",         "voltaje": None, "cantidad": 20, "descripcion": "Protoboard de 830 puntos."},
]

SENALETICAS = [
    "flecha_derecha.png",
    "flecha_izquierda.jpg",
    "stop.png",
    "semaforo_verde.png",
    "flecha_recto.png",
    "curva_peligrosa.png",
    "ceda_el_paso.png",
    "zona_escolar.jpg",
    "flecha_derecha.png,flecha_recto.png",
    "stop.png,semaforo_rojo.png",
]


def generar_historial(n=50):
    """Genera n registros aleatorios de historial de decisiones."""
    tipos = [t[0] for t in HistorialDecision.Tipo.choices]
    registros = []
    for _ in range(n):
        registros.append(
            HistorialDecision(
                tipo=random.choice(tipos),
                senaleticas=random.choice(SENALETICAS),
                indice_confianza=round(random.uniform(0.55, 0.999), 3),
            )
        )
    return registros


def generar_tiempos(n=20):
    """Genera n registros de tiempos de reacción con valores coherentes."""
    registros = []
    for _ in range(n):
        av_min = round(random.uniform(0.20, 0.60), 2)
        av_max = round(av_min + random.uniform(0.30, 1.00), 2)
        de_min = round(random.uniform(0.10, 0.40), 2)
        de_max = round(de_min + random.uniform(0.20, 0.80), 2)
        latencia = round(random.uniform(10.0, 150.0), 2)
        registros.append(
            TiempoReaccion(
                t_avance_maximo=av_max,
                t_avance_minimo=av_min,
                t_detenerse_maximo=de_max,
                t_detenerse_minimo=de_min,
                latencia_ms=latencia,
            )
        )
    return registros


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Poblar la BD con datos de prueba.")
    parser.add_argument("--flush", action="store_true", help="Borrar datos existentes antes de insertar.")
    args = parser.parse_args()

    with transaction.atomic():
        if args.flush:
            print("🧹 Borrando datos existentes...")
            TiempoReaccion.objects.all().delete()
            HistorialDecision.objects.all().delete()
            Componente.objects.all().delete()

        # --- Componentes ---
        print(f"📦 Insertando {len(COMPONENTES)} componentes...")
        creados, actualizados = 0, 0
        for data in COMPONENTES:
            obj, created = Componente.objects.update_or_create(
                nombre=data["nombre"],
                defaults={k: v for k, v in data.items() if k != "nombre"},
            )
            if created:
                creados += 1
            else:
                actualizados += 1
        print(f"   ✓ {creados} creados, {actualizados} actualizados")

        # --- Historial de decisiones ---
        print("🧭 Generando 50 historiales de decisión...")
        historial = generar_historial(50)
        HistorialDecision.objects.bulk_create(historial)
        print(f"   ✓ {len(historial)} registros insertados")

        # --- Tiempos de reacción ---
        print("⏱️  Generando 20 tiempos de reacción...")
        tiempos = generar_tiempos(20)
        TiempoReaccion.objects.bulk_create(tiempos)
        print(f"   ✓ {len(tiempos)} registros insertados")

    # Resumen final
    print("\n📊 Estado final de la base de datos:")
    print(f"   Componente:        {Componente.objects.count()}")
    print(f"   HistorialDecision: {HistorialDecision.objects.count()}")
    print(f"   TiempoReaccion:    {TiempoReaccion.objects.count()}")
    print("\n✅ Listo.")


if __name__ == "__main__":
    main()