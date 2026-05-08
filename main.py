# main.py

import pygame
import sys

from settings import (
    ANCHO_PANTALLA,
    ALTO_PANTALLA,
    FPS,
    TITULO_JUEGO,
    NEGRO,
    VERDE_CYBER,
    BLANCO,
    ROJO_ALERTA,
    PUNTOS_ENEMIGO_PEQUENO,
    VIDAS_INICIALES,
    ENERGIA_INICIAL,
)

from player import Player
from bullet import Bullet
from enemy import Enemy
from starfield import StarField


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption(TITULO_JUEGO)

    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont(None, 32)
    fuente_grande = pygame.font.SysFont(None, 72)

    jugador = Player()
    fondo_estrellas = StarField()

    balas = []
    enemigos = []

    puntaje = 0
    vidas = VIDAS_INICIALES
    energia = ENERGIA_INICIAL
    game_over = False

    EVENTO_CREAR_ENEMIGO = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_CREAR_ENEMIGO, 1200)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_over:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        jugador = Player()
                        balas = []
                        enemigos = []
                        puntaje = 0
                        vidas = VIDAS_INICIALES
                        energia = ENERGIA_INICIAL
                        game_over = False

                    if evento.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                continue

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    nueva_bala = Bullet(jugador.x, jugador.y - jugador.alto // 2)
                    balas.append(nueva_bala)

            if evento.type == EVENTO_CREAR_ENEMIGO:
                nuevo_enemigo = Enemy()
                enemigos.append(nuevo_enemigo)

        if not game_over:
            teclas = pygame.key.get_pressed()

            jugador.mover(teclas)

            for bala in balas[:]:
                bala.actualizar()

                if bala.esta_fuera_de_pantalla():
                    balas.remove(bala)

            for enemigo in enemigos[:]:
                enemigo.actualizar()

                if enemigo.esta_fuera_de_pantalla():
                    enemigos.remove(enemigo)

            # Colisión bala contra enemigo
            for bala in balas[:]:
                for enemigo in enemigos[:]:
                    if bala.rect.colliderect(enemigo.rect):
                        if bala in balas:
                            balas.remove(bala)

                        if enemigo in enemigos:
                            enemigos.remove(enemigo)

                        puntaje += PUNTOS_ENEMIGO_PEQUENO
                        break

            # Colisión enemigo contra jugador
            for enemigo in enemigos[:]:
                if enemigo.rect.colliderect(jugador.rect):
                    enemigos.remove(enemigo)
                    energia -= 20

                    if energia <= 0:
                        vidas -= 1
                        energia = ENERGIA_INICIAL

                        if vidas <= 0:
                            vidas = 0
                            energia = 0
                            game_over = True

        pantalla.fill(NEGRO)

        fondo_estrellas.actualizar()
        fondo_estrellas.dibujar(pantalla)

        texto_titulo = fuente.render("Cyber Python - MVP 0.3", True, VERDE_CYBER)
        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        texto_energia = fuente.render(f"Energia: {energia}", True, BLANCO)

        pantalla.blit(texto_titulo, (20, 20))
        pantalla.blit(texto_puntaje, (20, 50))
        pantalla.blit(texto_vidas, (20, 80))
        pantalla.blit(texto_energia, (20, 110))

        for bala in balas:
            bala.dibujar(pantalla)

        for enemigo in enemigos:
            enemigo.dibujar(pantalla)

        jugador.dibujar(pantalla)

        if game_over:
            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO_ALERTA)
            texto_reinicio = fuente.render("Presiona R para reiniciar o ESC para salir", True, BLANCO)

            pantalla.blit(texto_game_over, (230, 250))
            pantalla.blit(texto_reinicio, (190, 330))

        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()