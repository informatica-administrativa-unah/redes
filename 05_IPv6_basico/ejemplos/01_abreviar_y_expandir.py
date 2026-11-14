"""Abrevia y expande direcciones IPv6, y calcula su red, para comprobar tus respuestas.

Uso:
    python 05_IPv6_basico/ejemplos/01_abreviar_y_expandir.py 2001:0db8:0000:0000:0001:0000:0000:0001
    python 05_IPv6_basico/ejemplos/01_abreviar_y_expandir.py 2001:db8:acad:12:a1b2::7/64

Python escribe la forma abreviada siguiendo el RFC 5952, la misma que pide el revisor.
Solo usa la biblioteca estándar.
"""

import ipaddress
import sys


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    texto = sys.argv[1] if len(sys.argv) > 1 else "2001:0db8:0000:0000:0001:0000:0000:0001"
    interfaz = ipaddress.IPv6Interface(texto if "/" in texto else texto + "/128")
    ip = interfaz.ip
    print(f"Abreviada: {ip.compressed}")
    print(f"Completa:  {ip.exploded}")
    if "/" in texto:
        print(f"Red:       {interfaz.network}")
    tipos = [("enlace local", ip.is_link_local), ("loopback", ip.is_loopback), ("multicast", ip.is_multicast),
             ("sin especificar", ip.is_unspecified), ("privada o reservada", ip.is_private)]
    print("Tipo:      " + (", ".join(n for n, si in tipos if si) or "unicast global"))


if __name__ == "__main__":
    main()
