"""Corre la escalera del ping y dice en qué escalón se corta.

Uso:
    python 10_Diagnostico_de_red/ejemplos/01_escalera_del_ping.py GATEWAY SERVIDOR_INTERNO [NOMBRE]
    python 10_Diagnostico_de_red/ejemplos/01_escalera_del_ping.py 192.168.10.1 192.168.20.10 ventas.interno.guayabo.example

Usa el comando ping del sistema (Windows, Linux o macOS) y solo la biblioteca estándar de Python.
No reemplaza pensar: te dice dónde mirar primero.
"""

import platform
import subprocess
import sys


def responde(destino):
    cuenta = "-n" if platform.system() == "Windows" else "-c"
    r = subprocess.run(["ping", cuenta, "2", destino], capture_output=True, text=True)
    return r.returncode == 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    gateway, servidor = sys.argv[1], sys.argv[2]
    nombre = sys.argv[3] if len(sys.argv) > 3 else None
    escalones = [
        ("127.0.0.1", "La pila TCP/IP de esta compu"),
        (gateway, "Cable, puerto, VLAN, IP o máscara de esta compu"),
        (servidor, "Enrutamiento entre redes internas, o el servidor bloquea ICMP"),
        ("8.8.8.8", "Ruta por defecto, NAT o el enlace a internet"),
    ]
    if nombre:
        escalones.append((nombre, "DNS: el nombre no resuelve o el servidor DNS no responde"))
    for n, (destino, si_falla) in enumerate(escalones, 1):
        ok = responde(destino)
        print(f"{n}. ping {destino:<35} {'responde' if ok else 'NO responde'}")
        if not ok:
            print(f"\nSe corta aquí. Empezá a buscar en: {si_falla}.")
            return 1
    print("\nTodos los escalones responden. Si algo no funciona, mirá la aplicación o el servidor.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
