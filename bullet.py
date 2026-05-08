# bullet.py

import os
import pygame

from settings import (
    VELOCIDAD_BALA,
    ANCHO_BALA,
    ALTO_BALA,
)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.ancho = ANCHO_BALA
        self.alto = ALTO_BALA
        self.velocidad = VELOCIDAD_BALA

        # Cargar sprite de la bala del jugador
        ruta_imagen = os.path.join("assets", "images", "player_bullet.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        # La bala avanza hacia arriba
        self.y -= self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return self.y < -self.alto