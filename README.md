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
MVP 0.4
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

> Los enemigos disparan automáticamente amenazas digitales que reducen la energía del jugador.


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

Agregar meteoritos.
Agregar enemigos medianos.
Agregar disparos enemigos.
Agregar efectos de explosión.
Agregar sonidos y música.
Agregar menú inicial.
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