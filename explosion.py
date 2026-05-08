# explosion.py

import random
import pygame

from settings import (
    AMARILLO,
    ROJO_ALERTA,
    BLANCO,
)


class Explosion:
    def __init__(self, x, y, cantidad_particulas=18):
        self.particulas = []
        self.tiempo_vida = 25

        for _ in range(cantidad_particulas):
            particula = {
                "x": x,
                "y": y,
                "vel_x": random.uniform(-4, 4),
                "vel_y": random.uniform(-4, 4),
                "radio": random.randint(2, 5),
                "color": random.choice([AMARILLO, ROJO_ALERTA, BLANCO]),
            }

            self.particulas.append(particula)

    def actualizar(self):
        self.tiempo_vida -= 1

        for particula in self.particulas:
            particula["x"] += particula["vel_x"]
            particula["y"] += particula["vel_y"]

            # Reducir tamaño poco a poco
            if particula["radio"] > 0:
                particula["radio"] -= 0.12

    def dibujar(self, pantalla):
        for particula in self.particulas:
            if particula["radio"] > 0:
                pygame.draw.circle(
                    pantalla,
                    particula["color"],
                    (int(particula["x"]), int(particula["y"])),
                    int(particula["radio"])
                )

    def finalizada(self):
        return self.tiempo_vida <= 0