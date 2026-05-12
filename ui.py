# ui.py

import pygame

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    NEGRO,
    BLANCO,
    VERDE_CYBER,
    AZUL_CYBER,
    GRIS_CLARO,
    MORADO_CYBER,
)


def dibujar_texto_centrado(pantalla, texto, fuente, color, y):
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(ANCHO_PANTALLA // 2, y))
    pantalla.blit(superficie_texto, rect_texto)


def dibujar_opcion(pantalla, texto, fuente, y, seleccionada=False):
    if seleccionada:
        color = VERDE_CYBER
        prefijo = "> "
        sufijo = " <"
    else:
        color = GRIS_CLARO
        prefijo = "  "
        sufijo = "  "

    superficie_texto = fuente.render(f"{prefijo}{texto}{sufijo}", True, color)
    rect_texto = superficie_texto.get_rect(center=(ANCHO_PANTALLA // 2, y))
    pantalla.blit(superficie_texto, rect_texto)


def dibujar_menu_inicio(pantalla, opcion_seleccionada):
    pantalla.fill(NEGRO)

    fuente_titulo = pygame.font.SysFont(None, 78)
    fuente_subtitulo = pygame.font.SysFont(None, 32)
    fuente_menu = pygame.font.SysFont(None, 44)
    fuente_info = pygame.font.SysFont(None, 24)

    dibujar_texto_centrado(
        pantalla,
        "CYBER PYTHON",
        fuente_titulo,
        VERDE_CYBER,
        140
    )

    dibujar_texto_centrado(
        pantalla,
        "Arcade retro",
        fuente_subtitulo,
        AZUL_CYBER,
        200
    )

    opciones = ["Start", "Salir"]

    for indice, opcion in enumerate(opciones):
        y = 310 + indice * 60
        dibujar_opcion(
            pantalla,
            opcion,
            fuente_menu,
            y,
            seleccionada=(indice == opcion_seleccionada)
        )

    dibujar_texto_centrado(
        pantalla,
        "Usa ↑ / ↓ para moverte y Enter para seleccionar",
        fuente_info,
        BLANCO,
        500
    )

    dibujar_texto_centrado(
        pantalla,
        "Proyecto Python + Pygame + GitHub",
        fuente_info,
        MORADO_CYBER,
        530
    )


def dibujar_menu_pausa(pantalla, opcion_seleccionada):
    # Capa oscura sobre el juego
    capa = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    capa.set_alpha(210)
    capa.fill(NEGRO)
    pantalla.blit(capa, (0, 0))

    fuente_titulo = pygame.font.SysFont(None, 72)
    fuente_menu = pygame.font.SysFont(None, 42)
    fuente_info = pygame.font.SysFont(None, 24)

    dibujar_texto_centrado(
        pantalla,
        "PAUSA",
        fuente_titulo,
        VERDE_CYBER,
        150
    )

    opciones = ["Continuar", "Reiniciar", "Salir"]

    for indice, opcion in enumerate(opciones):
        y = 270 + indice * 55
        dibujar_opcion(
            pantalla,
            opcion,
            fuente_menu,
            y,
            seleccionada=(indice == opcion_seleccionada)
        )

    dibujar_texto_centrado(
        pantalla,
        "↑ / ↓ para moverte | Enter para seleccionar | P para continuar",
        fuente_info,
        BLANCO,
        500
    )