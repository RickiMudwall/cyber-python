# scanner_effect.py

import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    AZUL_CYBER,
    VERDE_CYBER,
    DURACION_SCANNER_MS,
    VELOCIDAD_EXPANSION_SCANNER,
)


class ScannerEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 10
        self.tiempo_inicio = pygame.time.get_ticks()
        self.activo = True

    def actualizar(self):
        self.radio += VELOCIDAD_EXPANSION_SCANNER

        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio

        if tiempo_transcurrido >= DURACION_SCANNER_MS:
            self.activo = False

    def dibujar(self, pantalla):
        if not self.activo:
            return

        # Capa transparente para dibujar ondas
        capa = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.SRCALPHA)

        # Onda principal
        pygame.draw.circle(
            capa,
            (*AZUL_CYBER, 110),
            (int(self.x), int(self.y)),
            int(self.radio),
            4
        )

        # Onda secundaria
        pygame.draw.circle(
            capa,
            (*VERDE_CYBER, 80),
            (int(self.x), int(self.y)),
            max(1, int(self.radio * 0.65)),
            2
        )

        # Línea vertical y horizontal tipo radar
        pygame.draw.line(
            capa,
            (*VERDE_CYBER, 80),
            (self.x, 0),
            (self.x, ALTO_PANTALLA),
            1
        )

        pygame.draw.line(
            capa,
            (*VERDE_CYBER, 80),
            (0, self.y),
            (ANCHO_PANTALLA, self.y),
            1
        )

        pantalla.blit(capa, (0, 0))

    def finalizado(self):
        return not self.activo