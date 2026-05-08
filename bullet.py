# bullet.py

import pygame

from settings import (
    VELOCIDAD_BALA,
    ANCHO_BALA,
    ALTO_BALA,
    AMARILLO,
)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ancho = ANCHO_BALA
        self.alto = ALTO_BALA
        self.velocidad = VELOCIDAD_BALA

        self.rect = pygame.Rect(
            self.x - self.ancho // 2,
            self.y,
            self.ancho,
            self.alto
        )

    def actualizar(self):
        # La bala avanza hacia arriba
        self.y -= self.velocidad
        self.rect.y = self.y

    def dibujar(self, pantalla):
        pygame.draw.rect(
            pantalla,
            AMARILLO,
            self.rect,
            border_radius=3
        )

    def esta_fuera_de_pantalla(self):
        return self.y < -self.alto