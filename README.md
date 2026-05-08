# Cyber Python

**Cyber Python** es un juego arcade retro desarrollado en Python con Pygame.  
El jugador controla la nave **CyberHack**, encargada de defender la Tierra frente a una invasión de naves alienígenas y amenazas digitales.

El proyecto forma parte de mi portafolio técnico para demostrar habilidades prácticas en Python, organización de código, lógica de videojuegos, Git y GitHub.

---

## Objetivo del juego

Controlar la nave CyberHack, esquivar enemigos, disparar, sumar puntos y sobrevivir el mayor tiempo posible.

En futuras versiones, el jugador deberá recolectar herramientas de ciberseguridad como escáner, arma avanzada y apoyo de naves aliadas para derrotar al Final Boss.

---

## Estado actual del proyecto

Versión actual:

```text
MVP 0.9
```
Funcionalidades implementadas:

Ventana principal del juego.
Nave controlable con teclado.
Movimiento horizontal, vertical y diagonal.
Fondo espacial animado.
Disparo con barra espaciadora.
Enemigos que aparecen desde la parte superior.
- Enemigos que disparan proyectiles hacia el jugador.
- Proyectiles enemigos con temática de amenazas digitales: malware, bug y alert.
- Daño al jugador por impacto de proyectiles enemigos.
Colisiones entre balas y enemigos.
Sistema de puntaje.
Sistema de energía.
Sistema de 3 vidas.
Pantalla de Game Over.
Reinicio de partida con tecla R.
Salida del juego con tecla ESC.
Controles
Acción	Tecla
Mover izquierda	Flecha izquierda
Mover derecha	Flecha derecha
Mover adelante	Flecha arriba
Mover atrás	Flecha abajo
Movimiento diagonal	Combinación de flechas
Disparar	Spacebar
Reiniciar en Game Over	R
Salir en Game Over	ESC

| Acción | Tecla |
|---|---|
| Mover nave con teclado | Flechas direccionales |
| Activar/desactivar control con mouse | M |
| Disparar | Spacebar |
| Pausar / continuar | P |
| Seleccionar opción de menú | Enter |
| Mover selección de menú | Flecha arriba / Flecha abajo |
| Reiniciar en Game Over | R |
| Salir | ESC |

> Los enemigos disparan automáticamente amenazas digitales que reducen la energía del jugador.
- Meteoritos que aparecen desde la parte superior.
- Meteoritos con resistencia de 3 impactos.
- Meteoritos destructibles con disparos del jugador.
- Daño al jugador por colisión con meteoritos.
- Puntaje adicional al destruir meteoritos.

- Explosiones simples por partículas.
- Efectos visuales al destruir enemigos.
- Efectos visuales al destruir meteoritos.
- Explosiones al impactar enemigos o meteoritos contra el jugador.

- Sprites básicos para la nave del jugador.
- Sprites básicos para naves enemigas.
- Sprites básicos para balas del jugador.
- Sprites básicos para proyectiles enemigos.
- Sprites básicos para meteoritos.
- Assets generados localmente en `assets/images/`.
- Feedback visual de daño sobre la nave del jugador.





- Sonidos básicos generados localmente.
- Sonido de disparo del jugador.
- Sonido de impacto de bala.
- Sonido de explosión.
- Sonido de daño recibido por el jugador.
- Sonido de Game Over.
- Administrador de sonidos separado en `sound_manager.py`.


- Menú inicial con opciones Start y Salir.
- Sistema de pausa con la tecla P.
- Menú de pausa con opciones Continuar, Reiniciar y Salir.
- Retorno al menú inicial desde Game Over.
- Control alternativo con mouse.
- Cambio de modo de control con la tecla M.
- Visualización del modo de control actual en pantalla.

Tecnologías utilizadas
Python 3.9
Pygame CE
PyCharm
Git
GitHub
Estructura del proyecto
cyber-runner-pygame/
│
├── main.py          # Motor principal del juego
├── settings.py      # Configuración global
├── player.py        # Clase del jugador
├── bullet.py        # Clase de disparos
├── enemy.py         # Clase de enemigos
├── starfield.py     # Fondo animado de estrellas
├── README.md        # Documentación del proyecto
├── .gitignore       # Archivos excluidos del control de versiones
│
└── assets/
    ├── images/      # Imágenes futuras del juego
    └── sounds/      # Sonidos futuros del juego
Instalación y ejecución local

Clonar el repositorio:

git clone URL_DEL_REPOSITORIO
cd cyber-runner-pygame

Crear entorno virtual:

python3 -m venv .venv
source .venv/bin/activate


Instalar dependencias:


pip install -r requirements.txt

Ejecutar el juego:

python3 main.py
Roadmap

Próximas mejoras planificadas:
- Mejorar explosiones con sprites animados y sonido.
- Mejorar meteoritos con sprites y animaciones.
Agregar enemigos medianos.
Agregar disparos enemigos.
- Agregar música de fondo y mejorar efectos de sonido.
- Mejorar diseño visual del menú inicial.
Agregar pantalla de victoria.
Agregar power-ups:
Escáner
Arma poderosa
Llamada a naves aliadas
Agregar Final Boss.
Empaquetar como ejecutable.
Publicar versión jugable en navegador con GitHub Pages.
Concepto narrativo

La Tierra está siendo invadida por naves alienígenas que atacan usando amenazas digitales como malware, bugs y falsas alertas.

CyberHack, líder de una unidad de defensa tecnológica, debe destruir oleadas enemigas, recolectar herramientas estratégicas y coordinar a su equipo de naves aliadas para vencer al enemigo principal.

Aprendizajes técnicos aplicados

Este proyecto permite practicar:

Programación orientada a objetos.
Separación de responsabilidades por archivos.
Manejo de eventos de teclado.
Renderizado gráfico con Pygame.
Detección de colisiones.
Control de estado del juego.
Uso de Git para control de versiones.
Documentación técnica para portafolio.
Autor

Proyecto desarrollado por Ricardo Nabor Tapia Poblete como parte de su portafolio técnico en Python, automatización, QA, IA y ciberseguridad.