from __future__ import annotations
import argparse
import time
from typing import Iterable, List
# --- después de tus imports ---
from visual.puntos import layout_regular_ngon, draw_points, style_axes, auto_radius
import matplotlib.pyplot as plt


# Importa tus generadores (ajusta el import según tu proyecto)
from combinatoria.rgs import (
    rgs_all,
    rgs_exactly,
    rgs_exactly_y,
    rgs_range,
    rgs_to_blocks,
)


def format_rgs(a: List[int]) -> str:
    """RGS bonito: [0,0,1,2]  + info de #bloques."""
    k = 0 if not a else (1 + max(a))
    return f"RGS={a}  (#bloques={k})"


def format_blocks(blocks: List[List[int]]) -> str:
    """Bloques como {1,3} | {2,5} | {4}."""
    parts = ["{" + ",".join(map(str, b)) + "}" for b in blocks]
    return " | ".join(parts)


def stream(
    it: Iterable[List[int] | List[List[int]]],
    *,
    yield_blocks: bool,
    limit: int | None,
    sleep: float,
) -> None:
    """Imprime en vivo (opcionalmente con pausa entre líneas)."""
    count = 0
    for obj in it:
        count += 1
        if yield_blocks:
            print(f"{count:>5}: {format_blocks(obj)}")  # type: ignore[arg-type]
        else:
            print(f"{count:>5}: {format_rgs(obj)}")     # type: ignore[arg-type]
        if limit is not None and count >= limit:
            break
        if sleep > 0:
            time.sleep(sleep)


def main() -> None:
    p = argparse.ArgumentParser(
        description="Explorador de particiones por RGS (imprime en vivo en consola)."
    )
    p.add_argument("--n", type=int, required=True, help="Tamaño del conjunto {1..n}.")
    mode = p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--all", action="store_true", help="Algoritmo V (todas las particiones).")
    mode.add_argument("--exact", type=int, metavar="K", help="Algoritmo X (exactamente K bloques).")
    mode.add_argument("--exact-y", type=int, metavar="K", help="Algoritmo Y (exactamente K bloques).")
    mode.add_argument("--range", nargs=2, type=int, metavar=("KMIN", "KMAX"),
                      help="Algoritmo Z (K en [KMIN,KMAX]).")

    p.add_argument("--blocks", action="store_true",
                   help="Imprimir como bloques en lugar de RGS.")
    p.add_argument("--limit", type=int, default=None,
                   help="Número máximo de líneas a imprimir (para pruebas).")
    p.add_argument("--sleep", type=float, default=0.0,
                   help="Segundos de pausa entre líneas (p. ej. 0.1).")
    mode.add_argument("--points-only", action="store_true",
                  help="Dibuja los puntos en un polígono regular sin particiones.")

    args = p.parse_args()

    # -------------------------------------------------------
    # NUEVO MODO: solo mostrar los puntos (sin particiones)
    # -------------------------------------------------------
    if args.points_only:
        n = args.n
        radius = auto_radius(n)
        positions = layout_regular_ngon(n, radius=radius, rotation_deg=90)

        fig, ax = plt.subplots(figsize=(6, 6))
        draw_points(ax, positions, labels=True)
        style_axes(ax)
        plt.title(f"{n} puntos - Polígono regular", fontsize=12)
        plt.show()
        return


    # Selección del iterador
    if args.all:
        it = rgs_all(args.n, yield_blocks=args.blocks)
    elif args.exact is not None:
        it = rgs_exactly(args.n, args.exact, yield_blocks=args.blocks)
    elif args.exact_y is not None:
        it = rgs_exactly_y(args.n, args.exact_y, yield_blocks=args.blocks)
    elif args.range is not None:
        kmin, kmax = args.range
        it = rgs_range(args.n, kmin, kmax, yield_blocks=args.blocks)
    else:
        p.error("Debes elegir un modo: --all | --exact K | --exact-y K | --range KMIN KMAX")
        return

    # Stream en vivo
    stream(it, yield_blocks=args.blocks, limit=args.limit, sleep=args.sleep)


if __name__ == "__main__":
    main()
