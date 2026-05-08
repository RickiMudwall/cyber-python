# generate_sounds.py

import os
import wave
import math
import struct
import random

SOUNDS_DIR = "assets/sounds"
os.makedirs(SOUNDS_DIR, exist_ok=True)

SAMPLE_RATE = 44100


def guardar_wav(nombre_archivo, muestras):
    ruta = os.path.join(SOUNDS_DIR, nombre_archivo)

    with wave.open(ruta, "w") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(SAMPLE_RATE)

        for muestra in muestras:
            valor = max(-1.0, min(1.0, muestra))
            archivo.writeframes(struct.pack("<h", int(valor * 32767)))

    print(f"Sonido generado: {ruta}")


def tono(frecuencia, duracion, volumen=0.4):
    total_muestras = int(SAMPLE_RATE * duracion)
    muestras = []

    for i in range(total_muestras):
        t = i / SAMPLE_RATE
        onda = math.sin(2 * math.pi * frecuencia * t)
        envolvente = 1 - (i / total_muestras)
        muestras.append(onda * volumen * envolvente)

    return muestras


def sonido_disparo():
    muestras = []
    duracion = 0.12
    total_muestras = int(SAMPLE_RATE * duracion)

    for i in range(total_muestras):
        t = i / SAMPLE_RATE
        frecuencia = 900 - (500 * (i / total_muestras))
        onda = math.sin(2 * math.pi * frecuencia * t)
        envolvente = 1 - (i / total_muestras)
        muestras.append(onda * 0.35 * envolvente)

    guardar_wav("player_shoot.wav", muestras)


def sonido_impacto_bala():
    muestras = []
    duracion = 0.08
    total_muestras = int(SAMPLE_RATE * duracion)

    for i in range(total_muestras):
        t = i / SAMPLE_RATE

        # Golpe corto tipo "clic metálico"
        frecuencia_1 = 1400
        frecuencia_2 = 900

        onda_1 = math.sin(2 * math.pi * frecuencia_1 * t)
        onda_2 = math.sin(2 * math.pi * frecuencia_2 * t)
        ruido = random.uniform(-0.4, 0.4)

        envolvente = 1 - (i / total_muestras)
        muestra = ((onda_1 * 0.5) + (onda_2 * 0.3) + ruido) * 0.35 * envolvente

        muestras.append(muestra)

    guardar_wav("bullet_impact.wav", muestras)


def sonido_explosion():
    muestras = []
    duracion = 0.35
    total_muestras = int(SAMPLE_RATE * duracion)

    for i in range(total_muestras):
        ruido = random.uniform(-1, 1)
        envolvente = 1 - (i / total_muestras)
        muestras.append(ruido * 0.45 * envolvente)

    guardar_wav("explosion.wav", muestras)


def sonido_danio():
    muestras = tono(220, 0.18, 0.45)
    guardar_wav("player_damage.wav", muestras)


def sonido_game_over():
    muestras = []
    muestras += tono(330, 0.25, 0.45)
    muestras += tono(220, 0.25, 0.45)
    muestras += tono(110, 0.45, 0.45)

    guardar_wav("game_over.wav", muestras)


def main():
    sonido_disparo()
    sonido_impacto_bala()
    sonido_explosion()
    sonido_danio()
    sonido_game_over()


if __name__ == "__main__":
    main()