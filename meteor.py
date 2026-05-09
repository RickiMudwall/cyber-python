# meteor.py

import os
import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
)


class Meteor:
    def __init__(self):
        self.radio = random.randint(18, 32)
        self.tamano = self.radio * 2

        self.x = random.randint(self.radio, ANCHO_PANTALLA - self.radio)
        self.y = -self.radio

        self.velocidad = random.randint(2, 4)
        self.vida = 3

        # Cargar sprite del meteorito
        ruta_imagen = os.path.join("assets", "images", "meteor.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.tamano, self.tamano)
        )

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def recibir_impacto(self, danio=1):
        self.vida -= danio
        return self.vida <= 0

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.radio