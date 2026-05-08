# meteor.py

import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
)


class Meteor:
    def __init__(self):
        self.radio = random.randint(18, 32)
        self.x = random.randint(self.radio, ANCHO_PANTALLA - self.radio)
        self.y = -self.radio

        self.velocidad = random.randint(2, 4)
        self.vida = 3

        self.color_base = (120, 120, 120)
        self.color_borde = (210, 210, 210)

        self.rect = pygame.Rect(
            self.x - self.radio,
            self.y - self.radio,
            self.radio * 2,
            self.radio * 2
        )

    def actualizar(self):
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        # Cuerpo del meteorito
        pygame.draw.circle(
            pantalla,
            self.color_base,
            (self.x, self.y),
            self.radio
        )

        # Borde irregular simple
        pygame.draw.circle(
            pantalla,
            self.color_borde,
            (self.x, self.y),
            self.radio,
            2
        )

        # Detalles visuales tipo cráter
        pygame.draw.circle(
            pantalla,
            (80, 80, 80),
            (self.x - self.radio // 3, self.y - self.radio // 4),
            max(3, self.radio // 5)
        )

        pygame.draw.circle(
            pantalla,
            (90, 90, 90),
            (self.x + self.radio // 4, self.y + self.radio // 5),
            max(2, self.radio // 6)
        )

    def recibir_impacto(self):
        self.vida -= 1
        return self.vida <= 0

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.radio