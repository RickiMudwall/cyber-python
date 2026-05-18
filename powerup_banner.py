# powerup_banner.py

import os
import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    POWERUP_BANNER_RUTA_BASE,
    POWERUP_BANNER_ANCHO,
    POWERUP_BANNER_ALTO,
    POWERUP_BANNER_SLIDE_MS,
    POWERUP_BANNER_HOLD_MS,
    AZUL_CYBER,
    VERDE_CYBER,
    BLANCO,
)


class PowerUpBanner:
    def __init__(self, tipo):
        self.tipo = tipo
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion_total = (
            POWERUP_BANNER_SLIDE_MS
            + POWERUP_BANNER_HOLD_MS
            + POWERUP_BANNER_SLIDE_MS
        )
        self.imagen = self.cargar_imagen()

    def obtener_nombre_imagen(self):
        return f"powerup_banner_{self.tipo}.png"

    def cargar_imagen(self):
        ruta = os.path.join(
            POWERUP_BANNER_RUTA_BASE,
            self.obtener_nombre_imagen()
        )

        if os.path.exists(ruta):
            imagen = pygame.image.load(ruta).convert_alpha()
            return pygame.transform.smoothscale(
                imagen,
                (POWERUP_BANNER_ANCHO, POWERUP_BANNER_ALTO)
            )

        return self.crear_imagen_temporal()

    def obtener_textos(self):
        if self.tipo == "scanner":
            return ("ESCANER ACTIVADO", "Pulso de rastreo listo para detectar amenazas")

        if self.tipo == "weapon":
            return ("ARMA POTENCIADA", "Municion de alto impacto disponible")

        if self.tipo == "allies":
            return ("ALIADOS ACTIVADOS", "Escuadron de apoyo entrando en combate")

        return ("POWER UP ACTIVADO", "Sistema potenciado")

    def crear_imagen_temporal(self):
        superficie = pygame.Surface(
            (POWERUP_BANNER_ANCHO, POWERUP_BANNER_ALTO),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            superficie,
            (8, 12, 28, 235),
            (0, 0, POWERUP_BANNER_ANCHO, POWERUP_BANNER_ALTO),
            border_radius=18
        )
        pygame.draw.rect(
            superficie,
            AZUL_CYBER,
            (0, 0, POWERUP_BANNER_ANCHO, POWERUP_BANNER_ALTO),
            3,
            border_radius=18
        )
        pygame.draw.line(
            superficie,
            VERDE_CYBER,
            (34, POWERUP_BANNER_ALTO - 44),
            (POWERUP_BANNER_ANCHO - 34, POWERUP_BANNER_ALTO - 44),
            3
        )

        titulo, detalle = self.obtener_textos()
        fuente_titulo = pygame.font.SysFont(None, 44)
        fuente_detalle = pygame.font.SysFont(None, 27)

        texto_titulo = fuente_titulo.render(titulo, True, VERDE_CYBER)
        texto_detalle = fuente_detalle.render(detalle, True, BLANCO)

        superficie.blit(
            texto_titulo,
            texto_titulo.get_rect(center=(POWERUP_BANNER_ANCHO // 2, 78))
        )
        superficie.blit(
            texto_detalle,
            texto_detalle.get_rect(center=(POWERUP_BANNER_ANCHO // 2, 126))
        )

        return superficie

    def suavizar_movimiento(self, progreso):
        return progreso * progreso * (3 - 2 * progreso)

    def obtener_alpha_y_escala(self, tiempo_local):
        if tiempo_local <= POWERUP_BANNER_SLIDE_MS:
            progreso = tiempo_local / POWERUP_BANNER_SLIDE_MS
            progreso = self.suavizar_movimiento(progreso)
            return int(255 * progreso), 0.88 + 0.12 * progreso

        if tiempo_local <= POWERUP_BANNER_SLIDE_MS + POWERUP_BANNER_HOLD_MS:
            return 255, 1.0

        tiempo_salida = (
            tiempo_local
            - POWERUP_BANNER_SLIDE_MS
            - POWERUP_BANNER_HOLD_MS
        )
        progreso = tiempo_salida / POWERUP_BANNER_SLIDE_MS
        progreso = self.suavizar_movimiento(progreso)

        return int(255 * (1 - progreso)), 1.0 - 0.08 * progreso

    def finalizado(self):
        tiempo_local = pygame.time.get_ticks() - self.tiempo_inicio
        return tiempo_local > self.duracion_total

    def dibujar(self, pantalla):
        tiempo_local = pygame.time.get_ticks() - self.tiempo_inicio
        alpha, escala = self.obtener_alpha_y_escala(tiempo_local)

        ancho = max(1, int(POWERUP_BANNER_ANCHO * escala))
        alto = max(1, int(POWERUP_BANNER_ALTO * escala))
        imagen = pygame.transform.smoothscale(self.imagen, (ancho, alto))
        imagen.set_alpha(alpha)

        rect = imagen.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2))
        pantalla.blit(imagen, rect)
