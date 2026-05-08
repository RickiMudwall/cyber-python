# enemy.py

import os
import random
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    ANCHO_ENEMIGO,
    ALTO_ENEMIGO,
    VELOCIDAD_ENEMIGO,
)


class Enemy:
    def __init__(self):
        self.ancho = ANCHO_ENEMIGO
        self.alto = ALTO_ENEMIGO
        self.velocidad = VELOCIDAD_ENEMIGO

        # Aparece en una posición aleatoria arriba de la pantalla
        self.x = random.randint(self.ancho, ANCHO_PANTALLA - self.ancho)
        self.y = -self.alto

        # Cargar sprite enemigo
        ruta_imagen = os.path.join("assets", "images", "enemy_ship.png")
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        # El enemigo baja hacia el jugador
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.alto