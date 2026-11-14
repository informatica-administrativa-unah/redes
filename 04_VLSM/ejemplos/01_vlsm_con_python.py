"""Arma una tabla VLSM para comprobar la que hiciste en papel.

Uso:
    python 04_VLSM/ejemplos/01_vlsm_con_python.py 192.168.50.0/24 ventas=40 bodega=20 camaras=12 administracion=10 wan=2

Ordena de más hosts a menos (si empatan, respeta el orden en que los escribiste) y asigna cada red
justo después de la anterior. Avisa si el pedido no cabe.
Solo usa la biblioteca estándar.
"""

import ipaddress
import sys


def prefijo_para(hosts):
    for prefijo in range(30, 0, -1):
        if 2 ** (32 - prefijo) - 2 >= hosts:
            return prefijo
    raise ValueError(hosts)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    base = ipaddress.ip_network(sys.argv[1])
    pedido = [(n, int(h)) for n, h in (x.split("=") for x in sys.argv[2:])]
    pedido.sort(key=lambda p: -p[1])
    total = sum(2 ** (32 - prefijo_para(h)) for _, h in pedido)
    print(f"Espacio: {base.num_addresses} direcciones. Pedido: {total}.")
    if total > base.num_addresses:
        sys.exit("No cabe. Pedí más espacio o revisá el pedido.")
    siguiente = int(base.network_address)
    print(f"{'Red':<16} {'Hosts':>5}  {'Subred':<20} {'Gateway':<16} {'Broadcast':<16}")
    for nombre, hosts in pedido:
        red = ipaddress.ip_network((siguiente, prefijo_para(hosts)))
        print(f"{nombre:<16} {hosts:>5}  {str(red):<20} {str(red.network_address + 1):<16} {red.broadcast_address}")
        siguiente = int(red.broadcast_address) + 1
    print(f"Libre desde {ipaddress.ip_address(siguiente)} hasta {base.broadcast_address}.")


if __name__ == "__main__":
    main()
