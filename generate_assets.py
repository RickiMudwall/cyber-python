# generate_assets.py

import os
import pygame

pygame.init()

IMAGES_DIR = "assets/images"
os.makedirs(IMAGES_DIR, exist_ok=True)


def guardar_superficie(nombre_archivo, superficie):
    ruta = os.path.join(IMAGES_DIR, nombre_archivo)
    pygame.image.save(superficie, ruta)
    print(f"Sprite generado: {ruta}")


def crear_nave_jugador():
    superficie = pygame.Surface((64, 64), pygame.SRCALPHA)

    verde = (0, 255, 120)
    azul = (0, 180, 255)
    blanco = (255, 255, 255)

    pygame.draw.polygon(
        superficie,
        verde,
        [(32, 4), (8, 58), (32, 46), (56, 58)]
    )

    pygame.draw.circle(superficie, azul, (32, 34), 8)
    pygame.draw.line(superficie, blanco, (32, 14), (32, 48), 3)

    guardar_superficie("player_ship.png", superficie)


def crear_nave_enemiga():
    superficie = pygame.Surface((56, 56), pygame.SRCALPHA)

    rojo = (255, 60, 60)
    blanco = (255, 255, 255)

    pygame.draw.polygon(
        superficie,
        rojo,
        [(28, 52), (4, 8), (28, 20), (52, 8)]
    )

    pygame.draw.circle(superficie, blanco, (28, 28), 6)

    guardar_superficie("enemy_ship.png", superficie)


def crear_bala_jugador():
    superficie = pygame.Surface((12, 24), pygame.SRCALPHA)

    amarillo = (255, 220, 80)
    blanco = (255, 255, 255)

    pygame.draw.rect(superficie, amarillo, (3, 2, 6, 20), border_radius=4)
    pygame.draw.rect(superficie, blanco, (5, 4, 2, 14), border_radius=2)

    guardar_superficie("player_bullet.png", superficie)


def crear_bala_enemiga(nombre, color):
    superficie = pygame.Surface((22, 30), pygame.SRCALPHA)

    pygame.draw.rect(superficie, color, (6, 5, 10, 20), border_radius=5)
    pygame.draw.circle(superficie, (255, 255, 255), (11, 10), 3)

    guardar_superficie(nombre, superficie)


def crear_meteorito():
    superficie = pygame.Surface((70, 70), pygame.SRCALPHA)

    gris = (120, 120, 120)
    borde = (210, 210, 210)
    crater = (80, 80, 80)

    pygame.draw.circle(superficie, gris, (35, 35), 30)
    pygame.draw.circle(superficie, borde, (35, 35), 30, 3)

    pygame.draw.circle(superficie, crater, (24, 24), 7)
    pygame.draw.circle(superficie, crater, (45, 42), 6)
    pygame.draw.circle(superficie, (95, 95, 95), (38, 22), 4)

    guardar_superficie("meteor.png", superficie)


def main():
    crear_nave_jugador()
    crear_nave_enemiga()
    crear_bala_jugador()

    crear_bala_enemiga("malware_bullet.png", (255, 60, 60))
    crear_bala_enemiga("bug_bullet.png", (255, 220, 80))
    crear_bala_enemiga("alert_bullet.png", (180, 80, 255))

    crear_meteorito()

    pygame.quit()


if __name__ == "__main__":
    main()