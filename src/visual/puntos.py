from __future__ import annotations
"""
Utilidades para dibujar N puntos como vértices de un polígono regular
(triángulo para n=3, cuadrado para n=4, pentágono para n=5, etc.).

Casos especiales: n=1 y n=2 se ubican de forma razonable.

Funciones principales:
- layout_regular_ngon(n, center=(0,0), radius=1.0, rotation_deg=90.0)
- auto_radius(n, fig_size=(6,6), margin=0.15)
- style_axes(ax, margin=0.15)
- draw_points(ax, positions, labels=True, indices_start=1)

Ejemplo de uso (desde un REPL):

>>> import matplotlib.pyplot as plt
>>> from visual.puntos import layout_regular_ngon, draw_points, style_axes
>>> n = 5
>>> pos = layout_regular_ngon(n, radius=1.0, rotation_deg=90)
>>> fig, ax = plt.subplots(figsize=(5,5))
>>> draw_points(ax, pos, labels=True)
>>> style_axes(ax)
>>> plt.show()
"""

import math
from typing import Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt

__all__ = [
    "layout_regular_ngon",
    "auto_radius",
    "style_axes",
    "draw_points",
]

Point = Tuple[float, float]


def _rotation_rad(deg: float) -> float:
    return deg * math.pi / 180.0


def layout_regular_ngon(
    n: int,
    *,
    center: Point = (0.0, 0.0),
    radius: float = 1.0,
    rotation_deg: float = 90.0,
) -> List[Point]:
    """Devuelve las coordenadas (x,y) de n puntos en un polígono regular.

    Reglas:
    - Para n>=3: vértices de un n-gono regular, orden antihorario, con el
      primer punto orientado por ``rotation_deg`` (90° coloca el 1 arriba).
    - Para n==2: dos puntos sobre el eje X centrados en ``center``.
    - Para n==1: un único punto en ``center``.

    Args:
        n: número de puntos (>=1).
        center: centro geométrico del polígono.
        radius: radio del polígono (distancia de cada punto al centro).
        rotation_deg: rotación inicial en grados (CCW). 90 coloca el 1 arriba.

    Returns:
        Lista de tuplas (x, y) en orden antihorario.
    """
    if n <= 0:
        raise ValueError("n debe ser >= 1")

    cx, cy = center
    if n == 1:
        return [(cx, cy)]
    if n == 2:
        # Dos puntos simétricos en el eje X alrededor del centro
        return [(cx - radius, cy), (cx + radius, cy)]

    rot = _rotation_rad(rotation_deg)
    step = 2.0 * math.pi / n
    pts: List[Point] = []
    for i in range(n):
        ang = rot + i * step
        x = cx + radius * math.cos(ang)
        y = cy + radius * math.sin(ang)
        pts.append((x, y))
    return pts


def auto_radius(
    n: int,
    *,
    fig_size: Tuple[float, float] = (6.0, 6.0),
    margin: float = 0.15,
) -> float:
    """Elige un radio razonable para que los puntos quepan con márgenes.

    Este cálculo es heurístico: asume que el rango útil del eje será [-1,1]
    y deja un margen relativo dado por ``margin``. Para la mayoría de casos
    con ``fig_size`` cuadrado y ``style_axes``, radius≈1.0 funciona bien.

    Args:
        n: número de puntos.
        fig_size: tamaño de figura (inches) para tener una referencia.
        margin: margen relativo en coordenadas de datos (0..0.4 recomendado).

    Returns:
        Radio sugerido (float).
    """
    if n <= 0:
        raise ValueError("n debe ser >= 1")
    # Mantén un radio que deje margen 'margin' a cada lado dentro de [-1,1]
    # Si usamos límites [-1.3, 1.3] luego, radius=1.0 es ideal.
    # Ajuste simple por si el usuario pide márgenes grandes.
    margin = max(0.0, min(0.4, margin))
    return 1.0 - margin * 0.2


def style_axes(ax: plt.Axes, *, margin: float = 0.15) -> None:
    """Aplica estilo estándar: aspecto igual, sin ejes y límites con margen.

    Args:
        ax: ejes de Matplotlib.
        margin: margen relativo para los límites (0..0.4 recomendado).
    """
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([])
    ax.set_yticks([])
    # Límites centrados con margen alrededor de [-1, 1]
    pad = 0.3 + margin
    ax.set_xlim(-1.0 - pad, 1.0 + pad)
    ax.set_ylim(-1.0 - pad, 1.0 + pad)


def draw_points(
    ax: plt.Axes,
    positions: Sequence[Point],
    *,
    labels: bool = True,
    indices_start: int = 1,
    point_size: float = 40.0,
    label_size: float = 10.0,
) -> dict:
    """Dibuja puntos (scatter) y, opcionalmente, etiquetas numéricas.

    Args:
        ax: ejes donde dibujar.
        positions: lista de (x, y).
        labels: si True, imprime etiquetas 1..n (o desplazadas por indices_start).
        indices_start: valor de inicio de las etiquetas (1 por defecto).
        point_size: tamaño del marcador de puntos (pt^2 de Matplotlib).
        label_size: tamaño de fuente de las etiquetas.

    Returns:
        Diccionario con referencias a artists creados: {
            'scatter': PathCollection,
            'texts': List[Text],
        }
    """
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    sc = ax.scatter(xs, ys, s=point_size, zorder=3)

    texts = []
    if labels:
        for i, (x, y) in enumerate(positions, start=indices_start):
            t = ax.text(x, y, str(i), ha="center", va="center", fontsize=label_size, zorder=4)
            texts.append(t)

    return {"scatter": sc, "texts": texts}
