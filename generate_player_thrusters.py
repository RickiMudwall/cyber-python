# generate_player_thrusters.py

import os
import pygame


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
pygame.init()

THRUSTERS_DIR = os.path.join("assets", "images", "player", "thrusters")
CANVAS_SIZE = (150, 180)


def guardar_superficie(nombre_archivo, superficie):
    os.makedirs(THRUSTERS_DIR, exist_ok=True)
    ruta = os.path.join(THRUSTERS_DIR, nombre_archivo)
    pygame.image.save(superficie, ruta)
    print(f"Thruster generado: {ruta}")


def dibujar_resplandor(superficie, centro, radio, color):
    for escala in range(3, 0, -1):
        alpha = int(color[3] / (escala * 2.0))
        pygame.draw.circle(
            superficie,
            (*color[:3], alpha),
            centro,
            radio * escala
        )


def dibujar_llama(superficie, puntos, color_exterior, color_interior):
    pygame.draw.polygon(superficie, color_exterior, puntos)

    centro_x = sum(punto[0] for punto in puntos) // len(puntos)
    centro_y = sum(punto[1] for punto in puntos) // len(puntos)

    puntos_internos = []
    for x, y in puntos:
        puntos_internos.append(
            (
                int(centro_x + (x - centro_x) * 0.48),
                int(centro_y + (y - centro_y) * 0.52),
            )
        )

    pygame.draw.polygon(superficie, color_interior, puntos_internos)


def crear_thruster_main(frame):
    superficie = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)

    largo = 16 + frame * 6
    ancho = 3 + frame
    color_exterior = (0, 210, 255, 135)
    color_medio = (0, 255, 180, 175)
    color_interior = (245, 255, 220, 230)

    # Seis motores traseros: tres por lado, alineados con la cola de la nave.
    motores = [
        (49, 148),
        (57, 157),
        (66, 151),
        (84, 151),
        (93, 157),
        (101, 148),
    ]

    for indice, (x, y) in enumerate(motores):
        variacion_largo = (indice % 2) * 4
        largo_motor = largo + variacion_largo

        dibujar_resplandor(
            superficie,
            (x, y + 3),
            2 + frame,
            color_exterior
        )
        dibujar_llama(
            superficie,
            [
                (x - ancho, y),
                (x + ancho, y),
                (x, y + largo_motor),
            ],
            color_exterior,
            color_medio,
        )
        dibujar_llama(
            superficie,
            [
                (x - max(1, ancho - 2), y + 2),
                (x + max(1, ancho - 2), y + 2),
                (x, y + int(largo_motor * 0.62)),
            ],
            color_medio,
            color_interior,
        )

    return superficie


def crear_thruster_reverse(frame):
    superficie = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)

    largo = 18 + frame * 7
    ancho = 6 + frame
    color_exterior = (180, 80, 255, 145)
    color_interior = (230, 250, 255, 210)

    motores = [58, 92]

    for x in motores:
        dibujar_resplandor(superficie, (x, 24), 4 + frame, color_exterior)
        dibujar_llama(
            superficie,
            [
                (x - ancho, 32),
                (x + ancho, 32),
                (x, 32 - largo),
            ],
            color_exterior,
            color_interior,
        )

    return superficie


def crear_thruster_left(frame):
    superficie = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)

    largo = 20 + frame * 8
    alto = 8 + frame
    color_exterior = (0, 255, 150, 140)
    color_interior = (210, 255, 245, 210)

    motores = [78, 118]

    for y in motores:
        dibujar_resplandor(superficie, (122, y), 4 + frame, color_exterior)
        dibujar_llama(
            superficie,
            [
                (118, y - alto),
                (118, y + alto),
                (118 + largo, y),
            ],
            color_exterior,
            color_interior,
        )

    return superficie


def crear_thruster_right(frame):
    superficie = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)

    largo = 20 + frame * 8
    alto = 8 + frame
    color_exterior = (0, 255, 150, 140)
    color_interior = (210, 255, 245, 210)

    motores = [78, 118]

    for y in motores:
        dibujar_resplandor(superficie, (28, y), 4 + frame, color_exterior)
        dibujar_llama(
            superficie,
            [
                (32, y - alto),
                (32, y + alto),
                (32 - largo, y),
            ],
            color_exterior,
            color_interior,
        )

    return superficie


def main():
    generadores = {
        "main": crear_thruster_main,
        "reverse": crear_thruster_reverse,
        "left": crear_thruster_left,
        "right": crear_thruster_right,
    }

    for nombre, generador in generadores.items():
        for frame in range(1, 4):
            superficie = generador(frame)
            guardar_superficie(f"thruster_{nombre}_{frame}.png", superficie)

    pygame.quit()


if __name__ == "__main__":
    main()
