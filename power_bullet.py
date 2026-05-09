# power_bullet.py

import os
import pygame

from settings import (
    ANCHO_BALA_PODEROSA,
    ALTO_BALA_PODEROSA,
    VELOCIDAD_BALA_PODEROSA,
    DANIO_BALA_PODEROSA,
)


class PowerBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ancho = ANCHO_BALA_PODEROSA
        self.alto = ALTO_BALA_PODEROSA
        self.velocidad = VELOCIDAD_BALA_PODEROSA
        self.danio = DANIO_BALA_PODEROSA

        # Usaremos el mismo sprite base de la bala, pero escalado más grande
        ruta_imagen = os.path.join("assets", "images", "player_bullet.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        self.y -= self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return self.y < -self.alto