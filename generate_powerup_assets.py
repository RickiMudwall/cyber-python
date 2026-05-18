# generate_powerup_assets.py

import math
import os
import pygame


IMAGES_DIR = os.path.join("assets", "images")
BANNERS_DIR = os.path.join(IMAGES_DIR, "powerup_banners")

ICON_SIZE = 48
BANNER_SIZE = (620, 210)

NEGRO_PANEL = (6, 10, 24)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 120)
AZUL = (0, 180, 255)
AMARILLO = (255, 220, 80)
MORADO = (180, 80, 255)
ROJO = (255, 60, 60)


POWERUPS = {
    "scanner": {
        "icon_file": "powerup_scanner.png",
        "banner_file": "powerup_banner_scanner.png",
        "accent": VERDE,
        "title": "ESCANER ACTIVADO",
        "detail": "Pulso de rastreo listo para detectar amenazas",
    },
    "weapon": {
        "icon_file": "powerup_weapon.png",
        "banner_file": "powerup_banner_weapon.png",
        "accent": AMARILLO,
        "title": "ARMA POTENCIADA",
        "detail": "Municion de alto impacto disponible",
    },
    "allies": {
        "icon_file": "powerup_allies.png",
        "banner_file": "powerup_banner_allies.png",
        "accent": AZUL,
        "title": "ALIADOS ACTIVADOS",
        "detail": "Escuadron de apoyo entrando en combate",
    },
}


def asegurar_directorios():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(BANNERS_DIR, exist_ok=True)


def dibujar_marco_icono(superficie, accent):
    pygame.draw.circle(superficie, (8, 14, 30, 230), (24, 24), 22)
    pygame.draw.circle(superficie, (*accent, 180), (24, 24), 21, 2)
    pygame.draw.circle(superficie, (*AZUL, 90), (24, 24), 16, 1)

    for angulo in (45, 135, 225, 315):
        radianes = math.radians(angulo)
        x = 24 + int(math.cos(radianes) * 21)
        y = 24 + int(math.sin(radianes) * 21)
        pygame.draw.circle(superficie, accent, (x, y), 2)


def crear_icono_scanner():
    superficie = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    dibujar_marco_icono(superficie, VERDE)

    pygame.draw.circle(superficie, (*VERDE, 220), (24, 24), 11, 2)
    pygame.draw.circle(superficie, (*VERDE, 150), (24, 24), 5, 1)
    pygame.draw.line(superficie, BLANCO, (24, 24), (36, 16), 3)
    pygame.draw.circle(superficie, BLANCO, (24, 24), 2)

    return superficie


def crear_icono_weapon():
    superficie = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    dibujar_marco_icono(superficie, AMARILLO)

    pygame.draw.polygon(superficie, AMARILLO, [(24, 7), (16, 22), (22, 22), (18, 39), (34, 18), (27, 19)])
    pygame.draw.line(superficie, BLANCO, (24, 10), (21, 25), 2)
    pygame.draw.circle(superficie, ROJO, (31, 16), 3)

    return superficie


def crear_icono_allies():
    superficie = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    dibujar_marco_icono(superficie, AZUL)

    pygame.draw.polygon(superficie, VERDE, [(24, 9), (15, 28), (24, 22), (33, 28)])
    pygame.draw.polygon(superficie, MORADO, [(13, 20), (5, 37), (13, 32), (21, 37)])
    pygame.draw.polygon(superficie, MORADO, [(35, 20), (27, 37), (35, 32), (43, 37)])
    pygame.draw.circle(superficie, BLANCO, (24, 19), 2)
    pygame.draw.circle(superficie, BLANCO, (13, 31), 2)
    pygame.draw.circle(superficie, BLANCO, (35, 31), 2)

    return superficie


def dibujar_lineas_tecnicas(superficie, accent):
    ancho, alto = superficie.get_size()

    for x in range(-120, ancho, 44):
        pygame.draw.line(superficie, (*AZUL, 22), (x, 18), (x + 135, alto - 18), 1)

    pygame.draw.rect(superficie, (*accent, 210), (14, 14, ancho - 28, alto - 28), 3, border_radius=18)
    pygame.draw.rect(superficie, (*AZUL, 80), (28, 30, ancho - 56, alto - 60), 1, border_radius=12)

    pygame.draw.line(superficie, accent, (50, alto - 48), (ancho - 50, alto - 48), 3)
    pygame.draw.circle(superficie, (*accent, 150), (68, 62), 18, 2)
    pygame.draw.circle(superficie, (*accent, 100), (ancho - 72, alto - 64), 22, 2)


def crear_banner(tipo, config):
    ancho, alto = BANNER_SIZE
    accent = config["accent"]
    superficie = pygame.Surface(BANNER_SIZE, pygame.SRCALPHA)

    for y in range(alto):
        mezcla = y / alto
        color = (
            int(NEGRO_PANEL[0] + 8 * mezcla),
            int(NEGRO_PANEL[1] + 14 * mezcla),
            int(NEGRO_PANEL[2] + 26 * mezcla),
            238,
        )
        pygame.draw.line(superficie, color, (0, y), (ancho, y))

    pygame.draw.rect(superficie, (3, 6, 16, 210), (22, 28, ancho - 44, alto - 56), border_radius=14)
    dibujar_lineas_tecnicas(superficie, accent)

    iconos = {
        "scanner": crear_icono_scanner,
        "weapon": crear_icono_weapon,
        "allies": crear_icono_allies,
    }
    icono = pygame.transform.smoothscale(iconos[tipo](), (76, 76))
    superficie.blit(icono, icono.get_rect(center=(96, 96)))

    fuente_titulo = pygame.font.SysFont(None, 46)
    fuente_detalle = pygame.font.SysFont(None, 28)
    fuente_codigo = pygame.font.SysFont(None, 20)

    titulo = fuente_titulo.render(config["title"], True, accent)
    detalle = fuente_detalle.render(config["detail"], True, BLANCO)
    codigo = fuente_codigo.render(f"POWER UP // {tipo.upper()}", True, VERDE)

    superficie.blit(titulo, (152, 64))
    superficie.blit(detalle, (154, 112))
    superficie.blit(codigo, (46, alto - 34))

    return superficie


def guardar_assets():
    asegurar_directorios()

    iconos = {
        "scanner": crear_icono_scanner(),
        "weapon": crear_icono_weapon(),
        "allies": crear_icono_allies(),
    }

    for tipo, config in POWERUPS.items():
        pygame.image.save(iconos[tipo], os.path.join(IMAGES_DIR, config["icon_file"]))
        pygame.image.save(
            crear_banner(tipo, config),
            os.path.join(BANNERS_DIR, config["banner_file"])
        )


def main():
    pygame.init()
    guardar_assets()
    pygame.quit()


if __name__ == "__main__":
    main()
