# enemy_bullet.py

import os
import pygame

from settings import ALTO_PANTALLA


class EnemyBullet:
    def __init__(self, x, y, tipo="malware"):
        self.x = x
        self.y = y
        self.tipo = tipo

        self.ancho = 22
        self.alto = 30
        self.velocidad = 4

        # Seleccionar sprite según tipo de amenaza
        if self.tipo == "malware":
            nombre_imagen = "malware_bullet.png"
        elif self.tipo == "bug":
            nombre_imagen = "bug_bullet.png"
        else:
            nombre_imagen = "alert_bullet.png"

        ruta_imagen = os.path.join("assets", "images", nombre_imagen)
        imagen_original = pygame.image.load(ruta_imagen).convert_alpha()

        self.imagen = pygame.transform.scale(
            imagen_original,
            (self.ancho, self.alto)
        )

        # Rectángulo de colisión
        self.rect = self.imagen.get_rect()
        self.rect.center = (self.x, self.y)

    def actualizar(self):
        # El disparo enemigo baja hacia el jugador
        self.y += self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.alto