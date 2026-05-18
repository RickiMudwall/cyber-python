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


def crear_powerup_scanner():
    superficie = pygame.Surface((48, 48), pygame.SRCALPHA)

    verde = (0, 255, 120)
    azul = (0, 180, 255)
    blanco = (255, 255, 255)

    pygame.draw.circle(superficie, azul, (24, 24), 20, 3)
    pygame.draw.circle(superficie, verde, (24, 24), 9, 2)
    pygame.draw.line(superficie, blanco, (24, 24), (38, 14), 3)

    fuente = pygame.font.SysFont(None, 16)
    texto = fuente.render("SCAN", True, verde)
    superficie.blit(texto, (8, 34))

    guardar_superficie("powerup_scanner.png", superficie)


def crear_powerup_arma():
    superficie = pygame.Surface((48, 48), pygame.SRCALPHA)

    amarillo = (255, 220, 80)
    rojo = (255, 60, 60)
    blanco = (255, 255, 255)

    pygame.draw.rect(superficie, amarillo, (14, 10, 20, 28), border_radius=5)
    pygame.draw.polygon(superficie, rojo, [(24, 2), (17, 14), (31, 14)])
    pygame.draw.line(superficie, blanco, (24, 14), (24, 36), 3)

    fuente = pygame.font.SysFont(None, 16)
    texto = fuente.render("GUN", True, blanco)
    superficie.blit(texto, (11, 34))

    guardar_superficie("powerup_weapon.png", superficie)


def crear_powerup_aliados():
    superficie = pygame.Surface((48, 48), pygame.SRCALPHA)

    morado = (180, 80, 255)
    verde = (0, 255, 120)
    blanco = (255, 255, 255)

    # Tres mini naves aliadas
    pygame.draw.polygon(superficie, verde, [(24, 6), (14, 26), (24, 20), (34, 26)])
    pygame.draw.polygon(superficie, morado, [(12, 18), (4, 36), (12, 31), (20, 36)])
    pygame.draw.polygon(superficie, morado, [(36, 18), (28, 36), (36, 31), (44, 36)])

    pygame.draw.circle(superficie, blanco, (24, 18), 3)
    pygame.draw.circle(superficie, blanco, (12, 30), 2)
    pygame.draw.circle(superficie, blanco, (36, 30), 2)

    fuente = pygame.font.SysFont(None, 15)
    texto = fuente.render("TEAM", True, blanco)
    superficie.blit(texto, (8, 36))

    guardar_superficie("powerup_allies.png", superficie)

def crear_final_boss():
    superficie = pygame.Surface((160, 120), pygame.SRCALPHA)

    rojo = (255, 60, 60)
    morado = (180, 80, 255)
    azul = (0, 180, 255)
    blanco = (255, 255, 255)
    gris = (60, 60, 70)

    # Cuerpo principal
    pygame.draw.polygon(
        superficie,
        morado,
        [
            (80, 8),
            (18, 45),
            (35, 108),
            (80, 88),
            (125, 108),
            (142, 45),
        ]
    )

    # Núcleo central
    pygame.draw.circle(superficie, rojo, (80, 58), 24)
    pygame.draw.circle(superficie, blanco, (80, 58), 10)

    # Alas laterales
    pygame.draw.polygon(superficie, gris, [(18, 45), (0, 75), (35, 108)])
    pygame.draw.polygon(superficie, gris, [(142, 45), (160, 75), (125, 108)])

    # Luces / puntos de energía
    pygame.draw.circle(superficie, azul, (48, 55), 7)
    pygame.draw.circle(superficie, azul, (112, 55), 7)

    # Detalles inferiores
    pygame.draw.rect(superficie, rojo, (55, 90, 12, 22), border_radius=4)
    pygame.draw.rect(superficie, rojo, (93, 90, 12, 22), border_radius=4)

    fuente = pygame.font.SysFont(None, 18)
    texto = fuente.render("BOSS", True, blanco)
    superficie.blit(texto, (63, 12))

    guardar_superficie("final_boss.png", superficie)

def crear_boss_missile():
    superficie = pygame.Surface((28, 48), pygame.SRCALPHA)

    rojo = (255, 60, 60)
    amarillo = (255, 220, 80)
    blanco = (255, 255, 255)
    gris = (80, 80, 90)

    # Cuerpo del misil
    pygame.draw.polygon(
        superficie,
        rojo,
        [(14, 2), (4, 18), (7, 40), (21, 40), (24, 18)]
    )

    # Centro del misil
    pygame.draw.rect(
        superficie,
        gris,
        (9, 16, 10, 20),
        border_radius=4
    )

    # Punta brillante
    pygame.draw.circle(superficie, blanco, (14, 10), 4)

    # Llamas inferiores
    pygame.draw.polygon(
        superficie,
        amarillo,
        [(8, 40), (14, 48), (20, 40)]
    )

    guardar_superficie("boss_missile.png", superficie)

def main():
    crear_nave_jugador()
    crear_nave_enemiga()
    crear_bala_jugador()

    crear_bala_enemiga("malware_bullet.png", (255, 60, 60))
    crear_bala_enemiga("bug_bullet.png", (255, 220, 80))
    crear_bala_enemiga("alert_bullet.png", (180, 80, 255))

    crear_meteorito()

    crear_powerup_scanner()
    crear_powerup_arma()
    crear_powerup_aliados()
    crear_final_boss()
    crear_boss_missile()

    pygame.quit()


if __name__ == "__main__":
    main()
