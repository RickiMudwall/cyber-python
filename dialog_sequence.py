# dialog_sequence.py

import os
import pygame

from settings import (
    ANCHO_PANTALLA,
    INTRO_DIALOGO_SLIDE_MS,
    INTRO_DIALOGO_HOLD_MS,
    INTRO_DIALOGO_ANCHO,
    INTRO_DIALOGO_ALTO,
    INTRO_DIALOGO_MARGEN_LATERAL,
    INTRO_DIALOGO_MARGEN_SUPERIOR,
    INTRO_DIALOGO_RUTA_BASE,
    AZUL_CYBER,
    VERDE_CYBER,
    BLANCO,
)


class DialogSequence:
    """
    Controla una secuencia de paneles de diálogo basados en imágenes completas.

    Cada diálogo puede entrar desde la izquierda o desde la derecha.
    La imagen ya puede incluir personaje, escena, frase y diseño completo.
    """

    def __init__(self, dialogos):
        self.dialogos = dialogos
        self.imagenes = {}

        self.duracion_dialogo = (
            INTRO_DIALOGO_SLIDE_MS
            + INTRO_DIALOGO_HOLD_MS
            + INTRO_DIALOGO_SLIDE_MS
        )

        self.cargar_imagenes()

    def cargar_imagenes(self):
        for dialogo in self.dialogos:
            nombre_imagen = dialogo["imagen"]

            if nombre_imagen not in self.imagenes:
                ruta_imagen = os.path.join(
                    INTRO_DIALOGO_RUTA_BASE,
                    nombre_imagen
                )

                if os.path.exists(ruta_imagen):
                    imagen_original = pygame.image.load(ruta_imagen).convert_alpha()
                    imagen_escalada = pygame.transform.smoothscale(
                        imagen_original,
                        (INTRO_DIALOGO_ANCHO, INTRO_DIALOGO_ALTO)
                    )
                    self.imagenes[nombre_imagen] = imagen_escalada
                else:
                    self.imagenes[nombre_imagen] = self.crear_imagen_temporal(
                        nombre_imagen
                    )

    def crear_imagen_temporal(self, nombre_imagen):
        """
        Fallback temporal si todavía no existe el PNG real.
        Esto permite probar la lógica antes de tener el arte final.
        """

        superficie = pygame.Surface(
            (INTRO_DIALOGO_ANCHO, INTRO_DIALOGO_ALTO),
            pygame.SRCALPHA
        )

        pygame.draw.rect(
            superficie,
            (10, 15, 30, 235),
            (0, 0, INTRO_DIALOGO_ANCHO, INTRO_DIALOGO_ALTO),
            border_radius=22
        )

        pygame.draw.rect(
            superficie,
            AZUL_CYBER,
            (0, 0, INTRO_DIALOGO_ANCHO, INTRO_DIALOGO_ALTO),
            3,
            border_radius=22
        )

        pygame.draw.rect(
            superficie,
            (20, 30, 50, 255),
            (24, 24, INTRO_DIALOGO_ANCHO - 48, INTRO_DIALOGO_ALTO - 48),
            border_radius=16
        )

        pygame.draw.line(
            superficie,
            VERDE_CYBER,
            (34, INTRO_DIALOGO_ALTO - 52),
            (INTRO_DIALOGO_ANCHO - 34, INTRO_DIALOGO_ALTO - 52),
            3
        )

        fuente_titulo = pygame.font.SysFont(None, 34)
        fuente_texto = pygame.font.SysFont(None, 24)

        texto_titulo = fuente_titulo.render("DIALOGO TEMPORAL", True, VERDE_CYBER)
        texto_nombre = fuente_texto.render(nombre_imagen, True, BLANCO)
        texto_info = fuente_texto.render("Reemplazar por PNG final", True, BLANCO)

        superficie.blit(texto_titulo, (36, 62))
        superficie.blit(texto_nombre, (36, 110))
        superficie.blit(texto_info, (36, 145))

        return superficie

    def suavizar_movimiento(self, progreso):
        return progreso * progreso * (3 - 2 * progreso)

    def calcular_x(self, lado, tiempo_local):
        ancho = INTRO_DIALOGO_ANCHO

        if lado == "izquierda":
            x_fuera = -ancho - 60
            x_destino = INTRO_DIALOGO_MARGEN_LATERAL
        else:
            x_fuera = ANCHO_PANTALLA + 60
            x_destino = ANCHO_PANTALLA - ancho - INTRO_DIALOGO_MARGEN_LATERAL

        if tiempo_local <= INTRO_DIALOGO_SLIDE_MS:
            progreso = tiempo_local / INTRO_DIALOGO_SLIDE_MS
            progreso = self.suavizar_movimiento(progreso)
            return x_fuera + (x_destino - x_fuera) * progreso

        if tiempo_local <= INTRO_DIALOGO_SLIDE_MS + INTRO_DIALOGO_HOLD_MS:
            return x_destino

        tiempo_salida = (
            tiempo_local
            - INTRO_DIALOGO_SLIDE_MS
            - INTRO_DIALOGO_HOLD_MS
        )

        progreso = tiempo_salida / INTRO_DIALOGO_SLIDE_MS
        progreso = self.suavizar_movimiento(progreso)

        return x_destino + (x_fuera - x_destino) * progreso

    def dibujar(self, pantalla, tiempo_transcurrido):
        for dialogo in self.dialogos:
            inicio = dialogo["inicio_ms"]
            tiempo_local = tiempo_transcurrido - inicio

            if tiempo_local < 0 or tiempo_local > self.duracion_dialogo:
                continue

            lado = dialogo["lado"]
            nombre_imagen = dialogo["imagen"]

            imagen = self.imagenes[nombre_imagen]

            x = int(self.calcular_x(lado, tiempo_local))
            y = INTRO_DIALOGO_MARGEN_SUPERIOR

            pantalla.blit(imagen, (x, y))
