# Repositorio de sonidos

Esta carpeta contiene los efectos de sonido usados por el juego.

## Sonidos activos

Estos archivos son cargados directamente por `sound_manager.py`:

```text
player_shoot.wav
bullet_impact.wav
explosion.wav
player_damage.wav
game_over.wav
```

## Organización recomendada

```text
assets/sounds/
  player_shoot.wav
  bullet_impact.wav
  explosion.wav
  player_damage.wav
  game_over.wav

  source/
    README.md
```

Usa `source/` para guardar referencias, versiones editables, pruebas o sonidos alternativos que no estén conectados todavía al juego.

Los `.wav` ubicados directamente en `assets/sounds/` son los sonidos finales que el juego intenta cargar.
