# starfield.py

import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    BLANCO,
    AZUL_CYBER,
)


class StarField:
    def __init__(self, cantidad_estrellas=80):
        self.estrellas = []

        for _ in range(cantidad_estrellas):
            estrella = {
                "x": random.randint(0, ANCHO_PANTALLA),
                "y": random.randint(0, ALTO_PANTALLA),
                "velocidad": random.randint(1, 3),
                "radio": random.randint(1, 2),
            }
            self.estrellas.append(estrella)

    def actualizar(self):
        for estrella in self.estrellas:
            estrella["y"] += estrella["velocidad"]

            # Si la estrella sale por abajo, vuelve arriba
            if estrella["y"] > ALTO_PANTALLA:
                estrella["x"] = random.randint(0, ANCHO_PANTALLA)
                estrella["y"] = 0
                estrella["velocidad"] = random.randint(1, 3)
                estrella["radio"] = random.randint(1, 2)

    def dibujar(self, pantalla):
        for estrella in self.estrellas:
            color = BLANCO if estrella["velocidad"] == 1 else AZUL_CYBER

            pygame.draw.circle(
                pantalla,
                color,
                (estrella["x"], estrella["y"]),
                estrella["radio"]
            )