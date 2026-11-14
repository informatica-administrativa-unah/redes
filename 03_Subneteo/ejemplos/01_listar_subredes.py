"""Lista las subredes de una red con un prefijo nuevo, para comprobar tus tablas de subneteo.

Uso:
    python 03_Subneteo/ejemplos/01_listar_subredes.py 192.168.60.0/24 27
    python 03_Subneteo/ejemplos/01_listar_subredes.py 172.20.0.0/16 23 --hasta 20

Primero hacé la tabla en papel. Esto es para revisar, no para copiar.
Solo usa la biblioteca estándar.
"""

import argparse
import ipaddress
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("red", help="red original, por ejemplo 192.168.60.0/24")
    ap.add_argument("prefijo", type=int, help="prefijo nuevo, por ejemplo 27")
    ap.add_argument("--hasta", type=int, default=16, help="cuántas subredes mostrar (por defecto 16)")
    a = ap.parse_args()

    red = ipaddress.ip_network(a.red)
    if a.prefijo <= red.prefixlen or a.prefijo > 30:
        sys.exit(f"El prefijo nuevo tiene que ser mayor que /{red.prefixlen} y como mucho /30.")
    total = 2 ** (a.prefijo - red.prefixlen)
    print(f"{red} partida en /{a.prefijo}: {total} subredes de {2 ** (32 - a.prefijo) - 2} hosts útiles")
    print(f"{'N.°':>5}  {'Subred':<20} {'Primer host':<16} {'Último host':<16} Broadcast")
    for n, sub in enumerate(red.subnets(new_prefix=a.prefijo), 1):
        if n > a.hasta:
            print(f"  ... y {total - a.hasta} más")
            break
        print(f"{n:>5}  {str(sub):<20} {str(sub.network_address + 1):<16} "
              f"{str(sub.broadcast_address - 1):<16} {sub.broadcast_address}")


if __name__ == "__main__":
    main()
