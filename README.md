# Cyber Python

**Cyber Python** es un videojuego arcade desarrollado en Python con Pygame. El jugador controla la nave **CyberHack** para defender la Tierra de una invasión de naves enemigas, meteoritos y amenazas digitales.

El proyecto forma parte de mi portafolio técnico y muestra trabajo práctico con Python, Pygame, organización modular, assets locales, lógica de gameplay, Git y GitHub.

## Estado Actual

```text
MVP 1.5 - Intro visual, nave animada y efectos cinemáticos
```

La versión actual incluye una intro cinemática de despegue con sprites por capas, efecto de viaje a velocidad luz, nave del jugador con inclinación lateral y propulsores animados.

## Características

- Ventana principal en pantalla completa escalada.
- Menú inicial, pausa, Game Over y pantalla de victoria.
- Control de nave con mouse o teclado.
- Movimiento horizontal, vertical y diagonal.
- Disparo normal y disparo automático.
- Arma poderosa con munición acumulable.
- Sistema de puntaje, energía y vidas.
- Enemigos en oleadas con trayectorias curvas.
- Enemigos que disparan proyectiles tipo malware, bug y alert.
- Tormentas de meteoritos con meteoritos destructibles.
- Power-ups de scanner, arma poderosa y naves aliadas.
- Final Boss con barra de vida, misiles teledirigidos y secuencia especial de victoria.
- Explosiones por partículas y efectos visuales de impacto.
- Sonidos generados localmente para disparos, daño, impactos, explosiones y Game Over.

## Intro Cinemática

Al iniciar una partida, el juego muestra una escena previa al gameplay:

- Tierra renderizada como sprite al fondo.
- Bahía espacial dividida en capas trasera y frontal.
- Nave ubicada entre las capas de la estación para dar profundidad.
- Despegue con desplazamiento independiente de Tierra y estación.
- La estación sale más rápido y la Tierra más lento antes de pasar al modo jugando.
- Efecto visual de viaje a velocidad luz: estrellas puntuales, estiramiento en líneas y retorno a puntos.
- Diálogos cinemáticos basados en imágenes completas.

Assets principales:

```text
assets/images/intro/intro_earth.png
assets/images/intro/intro_station_back.png
assets/images/intro/intro_station_front.png
assets/images/dialogs/dialog_intro_1.png
assets/images/dialogs/dialog_intro_2.png
assets/images/dialogs/dialog_intro_3.png
```

## Nave del Jugador

La nave del jugador usa sprites dedicados para simular movimiento 3D lateral:

- Sprite idle.
- Dos niveles de inclinación a la izquierda.
- Dos niveles de inclinación a la derecha.
- Propulsores animados según dirección de movimiento.
- Seis propulsores principales alineados con la cola de la nave.
- Retropropulsores y propulsores laterales generados por script.

Assets de nave:

```text
assets/images/player/ship/player_idle.png
assets/images/player/ship/player_left_1.png
assets/images/player/ship/player_left_2.png
assets/images/player/ship/player_right_1.png
assets/images/player/ship/player_right_2.png
```

Assets de propulsores:

```text
assets/images/player/thrusters/thruster_main_1.png
assets/images/player/thrusters/thruster_main_2.png
assets/images/player/thrusters/thruster_main_3.png
assets/images/player/thrusters/thruster_reverse_1.png
assets/images/player/thrusters/thruster_reverse_2.png
assets/images/player/thrusters/thruster_reverse_3.png
assets/images/player/thrusters/thruster_left_1.png
assets/images/player/thrusters/thruster_left_2.png
assets/images/player/thrusters/thruster_left_3.png
assets/images/player/thrusters/thruster_right_1.png
assets/images/player/thrusters/thruster_right_2.png
assets/images/player/thrusters/thruster_right_3.png
```

Los propulsores se pueden regenerar con:

```bash
python generate_player_thrusters.py
```

## Controles

| Acción | Control |
|---|---|
| Iniciar partida | Enter |
| Mover selección de menú | Flecha arriba / Flecha abajo |
| Mover nave con mouse | Mouse |
| Mover nave con teclado | Flechas direccionales |
| Alternar mouse / teclado | M |
| Disparar | Clic izquierdo o Spacebar |
| Activar Scanner | 1 |
| Activar / desactivar arma poderosa | 2 |
| Llamar naves aliadas | 3 |
| Pausar / continuar | P |
| Reiniciar en Game Over | R |
| Salir | ESC |

## Condición del Final Boss

El Final Boss aparece cuando el jugador cumple estas condiciones:

```text
Scanner disponible
Aliados disponibles
Más de 700 municiones de arma poderosa
```

Para derrotarlo se debe ejecutar la secuencia especial:

```text
Scanner -> Arma poderosa activa -> Aliados
```

## Estructura del Proyecto

```text
main.py                     Bucle principal, estados, eventos y colisiones
settings.py                 Constantes de configuración
player.py                   Nave del jugador, sprites e impulsores
enemy.py                    Enemigo individual
enemy_wave.py               Generación de oleadas
final_boss.py               Lógica y dibujo del Final Boss
boss_missile.py             Misiles teledirigidos del Boss
bullet.py                   Bala normal del jugador
power_bullet.py             Bala poderosa
enemy_bullet.py             Proyectiles enemigos
meteor.py                   Meteoritos
powerup.py                  Power-ups
ally_ship.py                Naves aliadas
scanner_effect.py           Efecto visual del scanner
explosion.py                Partículas de explosión
starfield.py                Fondo de estrellas
sound_manager.py            Carga y reproducción de sonidos
dialog_sequence.py          Diálogos cinemáticos de intro
ui.py                       Menús y textos de interfaz
generate_assets.py          Generador de assets base
generate_sounds.py          Generador de sonidos
generate_player_thrusters.py Generador de propulsores del jugador
```

## Instalación

Requiere Python 3.9+.

Crear entorno virtual e instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ejecutar el juego desde la raíz del proyecto:

```bash
python main.py
```

## Dependencias

```text
pygame-ce==2.5.6
```

## Notas de Desarrollo

- Los assets deben ejecutarse desde la raíz del proyecto porque las rutas son relativas.
- Algunos sprites importados fueron exportados como PNG RGB con falso fondo de transparencia; el código limpia fondos claros conectados al borde al cargarlos.
- El árbol visual de la intro está separado en capas para poder seguir mejorando profundidad y animación.
- Las naves enemigas todavía usan sprites base; su actualización visual queda pendiente para una siguiente etapa.
