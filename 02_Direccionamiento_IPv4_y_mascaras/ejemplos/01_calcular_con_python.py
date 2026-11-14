"""Calcula los datos de una red IPv4 con el módulo ipaddress de Python.

Uso:
    python 02_Direccionamiento_IPv4_y_mascaras/ejemplos/01_calcular_con_python.py 192.168.20.77/26

Sirve para comprobar tus cuentas DESPUÉS de hacerlas en papel. En el examen no vas a tener Python.
Solo usa la biblioteca estándar.
"""

import ipaddress
import sys


def mostrar(texto):
    interfaz = ipaddress.ip_interface(texto)
    red = interfaz.network
    print(f"Dirección:      {interfaz.ip}")
    print(f"Máscara:        {red.netmask}  (/{red.prefixlen})")
    print(f"Wildcard:       {red.hostmask}")
    print(f"Red:            {red.network_address}")
    print(f"Broadcast:      {red.broadcast_address}")
    print(f"Primer host:    {red.network_address + 1}")
    print(f"Último host:    {red.broadcast_address - 1}")
    print(f"Hosts útiles:   {red.num_addresses - 2}")
    print(f"¿Es privada?:   {'sí' if interfaz.ip.is_private else 'no'}")
    print("En binario:")
    for nombre, valor in (("  dirección", interfaz.ip), ("  máscara  ", red.netmask), ("  red      ", red.network_address)):
        octetos = ".".join(f"{int(o):08b}" for o in str(valor).split("."))
        print(f"{nombre} {octetos}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    mostrar(sys.argv[1] if len(sys.argv) > 1 else "192.168.20.77/26")
