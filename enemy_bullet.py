# enemy_bullet.py

import pygame

from settings import (
    ALTO_PANTALLA,
    ROJO_ALERTA,
    AMARILLO,
)


class EnemyBullet:
    def __init__(self, x, y, tipo="malware"):
        self.x = x
        self.y = y
        self.tipo = tipo

        self.ancho = 10
        self.alto = 18
        self.velocidad = 4

        self.rect = pygame.Rect(
            self.x - self.ancho // 2,
            self.y,
            self.ancho,
            self.alto
        )

    def actualizar(self):
        # El disparo enemigo baja hacia el jugador
        self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self, pantalla):
        if self.tipo == "malware":
            color = ROJO_ALERTA
        elif self.tipo == "bug":
            color = AMARILLO
        else:
            color = (180, 80, 255)

        # Proyectil enemigo simple
        pygame.draw.rect(
            pantalla,
            color,
            self.rect,
            border_radius=4
        )

        # Texto pequeño para reforzar la temática
        fuente = pygame.font.SysFont(None, 14)
        texto = fuente.render(self.tipo, True, (255, 255, 255))
        pantalla.blit(texto, (self.rect.x - 8, self.rect.y - 10))

    def esta_fuera_de_pantalla(self):
        return self.y > ALTO_PANTALLA + self.alto