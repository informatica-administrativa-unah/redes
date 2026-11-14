"""Revisa tus respuestas de subneteo, VLSM, sumarización e IPv6.

Uso, desde la carpeta del repo:
    python herramientas/revisar.py                 revisa ejercicios/subneteo.yml
    python herramientas/revisar.py otro.yml        revisa otro archivo con el mismo formato
    python herramientas/revisar.py --soluciones    revisa soluciones/subneteo.yml (lo usa el repo original)

Las respuestas correctas no están guardadas en ningún lado: este programa las calcula con el
módulo ipaddress de Python a partir de los datos de cada ejercicio (la lista PREGUNTAS de abajo).
Si no te cuadra una, la pista te dice qué revisar, sin darte el número.

Formato del archivo: YAML sencillo, un bloque por ejercicio y un campo por línea.

    e03:
      red: 192.168.20.64
      mascara: 255.255.255.192

Las máscaras se aceptan como 255.255.255.192, como /26 o como 26.
Solo usa la biblioteca estándar de Python.
"""

import argparse
import ipaddress
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Cada ejercicio: id, tipo y datos. El enunciado completo está en ejercicios/subneteo.yml.
PREGUNTAS = [
    # Nivel 1. Datos de una red a partir de una dirección con prefijo
    {"id": "e01", "tipo": "subred", "ip": "192.168.10.37/24"},
    {"id": "e02", "tipo": "subred", "ip": "172.16.45.200/16"},
    {"id": "e03", "tipo": "subred", "ip": "192.168.20.77/26"},
    {"id": "e04", "tipo": "subred", "ip": "10.10.5.130/25"},
    {"id": "e05", "tipo": "subred", "ip": "192.168.1.100/28"},
    {"id": "e06", "tipo": "subred", "ip": "172.20.13.71/21"},
    {"id": "e07", "tipo": "subred", "ip": "10.0.0.255/23"},
    # Nivel 2. ¿Están en la misma red?
    {"id": "e08", "tipo": "misma_red", "ip1": "192.168.5.65", "ip2": "192.168.5.62", "prefijo": 26},
    {"id": "e09", "tipo": "misma_red", "ip1": "10.1.14.3", "ip2": "10.1.15.250", "prefijo": 23},
    # Nivel 3. Dividir una red en cierta cantidad de subredes
    {"id": "e10", "tipo": "dividir", "red": "192.168.30.0/24", "necesarias": 6, "pedida": 3},
    {"id": "e11", "tipo": "dividir", "red": "172.16.0.0/16", "necesarias": 50, "pedida": 10},
    {"id": "e12", "tipo": "dividir", "red": "10.0.0.0/8", "necesarias": 1000, "pedida": 5},
    # Nivel 4. Dividir una red según los hosts que necesita cada segmento
    {"id": "e13", "tipo": "hosts", "red": "192.168.40.0/24", "hosts": 50},
    {"id": "e14", "tipo": "hosts", "red": "172.18.0.0/16", "hosts": 500},
    {"id": "e15", "tipo": "hosts", "red": "192.168.50.0/24", "hosts": 2},
    # Nivel 5. VLSM: de la red más grande a la más chica
    {"id": "e16", "tipo": "vlsm", "red": "192.168.100.0/24",
     "segmentos": [("ventas", 60), ("bodega", 28), ("administracion", 12), ("wan1", 2), ("wan2", 2)]},
    {"id": "e17", "tipo": "vlsm", "red": "172.16.32.0/22",
     "segmentos": [("tegucigalpa", 200), ("san_pedro_sula", 120), ("la_ceiba", 50), ("servidores", 20),
                   ("wan_tgu_sps", 2), ("wan_tgu_lce", 2), ("wan_sps_lce", 2)]},
    {"id": "e18", "tipo": "vlsm", "red": "10.20.0.0/23",
     "segmentos": [("contabilidad", 25), ("ventas", 100), ("gerencia", 6), ("bodega", 60), ("wifi_invitados", 100)]},
    # Nivel 6. Máscara wildcard y sumarización de rutas
    {"id": "e19", "tipo": "wildcard", "mascara": "255.255.255.224"},
    {"id": "e20", "tipo": "wildcard", "mascara": "255.255.252.0"},
    {"id": "e21", "tipo": "resumen", "redes": ["192.168.16.0/24", "192.168.17.0/24", "192.168.18.0/24", "192.168.19.0/24"]},
    {"id": "e22", "tipo": "resumen", "redes": ["172.16.8.0/24", "172.16.9.0/24", "172.16.10.0/24", "172.16.11.0/24",
                                                "172.16.12.0/24", "172.16.13.0/24", "172.16.14.0/24", "172.16.15.0/24"]},
    # Nivel 7. IPv6
    {"id": "e23", "tipo": "ipv6_abreviar", "ip": "2001:0db8:0000:0000:0000:ff00:0042:8329"},
    {"id": "e24", "tipo": "ipv6_abreviar", "ip": "2001:0db8:0000:0000:0001:0000:0000:0001"},
    {"id": "e25", "tipo": "ipv6_expandir", "ip": "2001:db8:acad:1::1"},
    {"id": "e26", "tipo": "ipv6_red", "ip": "2001:db8:acad:12:a1b2::7/64"},
]


# Cálculo de las respuestas -----------------------------------------------------------------------

def prefijo_para_subredes(prefijo_base, necesarias):
    bits = 0
    while 2 ** bits < necesarias:
        bits += 1
    return prefijo_base + bits


def prefijo_para_hosts(hosts):
    for prefijo in range(30, -1, -1):
        if 2 ** (32 - prefijo) - 2 >= hosts:
            return prefijo
    raise ValueError(hosts)


def utiles(prefijo):
    return 2 ** (32 - prefijo) - 2


def esperado(p):
    """Devuelve {campo: valor esperado} para un ejercicio."""
    t = p["tipo"]
    if t == "subred":
        iface = ipaddress.ip_interface(p["ip"])
        red = iface.network
        return {"red": red.network_address, "mascara": red.netmask, "broadcast": red.broadcast_address,
                "primer_host": red.network_address + 1, "ultimo_host": red.broadcast_address - 1,
                "hosts_utiles": utiles(red.prefixlen)}
    if t == "misma_red":
        r1 = ipaddress.ip_interface(f"{p['ip1']}/{p['prefijo']}").network
        r2 = ipaddress.ip_interface(f"{p['ip2']}/{p['prefijo']}").network
        return {"red_ip1": r1.network_address, "red_ip2": r2.network_address, "misma_red": "si" if r1 == r2 else "no"}
    if t == "dividir":
        base = ipaddress.ip_network(p["red"])
        nuevo = prefijo_para_subredes(base.prefixlen, p["necesarias"])
        sub = list(base.subnets(new_prefix=nuevo)) if nuevo - base.prefixlen <= 12 else None
        pedida = sub[p["pedida"] - 1] if sub else \
            ipaddress.ip_network((int(base.network_address) + (p["pedida"] - 1) * 2 ** (32 - nuevo), nuevo))
        return {"prefijo": nuevo, "mascara": ipaddress.ip_network(f"0.0.0.0/{nuevo}").netmask,
                "subredes": 2 ** (nuevo - base.prefixlen), "hosts_por_subred": utiles(nuevo),
                "subred_pedida": pedida, "broadcast_pedida": pedida.broadcast_address}
    if t == "hosts":
        base = ipaddress.ip_network(p["red"])
        nuevo = prefijo_para_hosts(p["hosts"])
        return {"prefijo": nuevo, "mascara": ipaddress.ip_network(f"0.0.0.0/{nuevo}").netmask,
                "hosts_por_subred": utiles(nuevo), "subredes": 2 ** (nuevo - base.prefixlen)}
    if t == "vlsm":
        base = ipaddress.ip_network(p["red"])
        siguiente = int(base.network_address)
        resultado = {}
        # Se ordena de más hosts a menos; si empatan, queda el orden en que aparecen.
        for nombre, hosts in sorted(p["segmentos"], key=lambda s: -s[1]):
            prefijo = prefijo_para_hosts(hosts)
            red = ipaddress.ip_network((siguiente, prefijo))
            if not red.subnet_of(base):
                raise ValueError(f"{p['id']}: no cabe {nombre}")
            resultado[f"{nombre}_red"] = red
            resultado[f"{nombre}_gateway"] = red.network_address + 1
            resultado[f"{nombre}_broadcast"] = red.broadcast_address
            siguiente = int(red.broadcast_address) + 1
        return resultado
    if t == "wildcard":
        return {"wildcard": ipaddress.ip_address(int(ipaddress.ip_address(p["mascara"])) ^ 0xFFFFFFFF)}
    if t == "resumen":
        redes = [ipaddress.ip_network(r) for r in p["redes"]]
        resumen = list(ipaddress.collapse_addresses(redes))
        if len(resumen) != 1:
            raise ValueError(f"{p['id']}: las redes no se resumen en una sola")
        return {"resumen": resumen[0]}
    if t == "ipv6_abreviar":
        return {"abreviada": ipaddress.IPv6Address(p["ip"]).compressed}
    if t == "ipv6_expandir":
        return {"expandida": ipaddress.IPv6Address(p["ip"]).exploded}
    if t == "ipv6_red":
        return {"red": ipaddress.IPv6Interface(p["ip"]).network}
    raise ValueError(t)


# Lectura del archivo ------------------------------------------------------------------------------

def leer(ruta):
    """Lee un YAML de dos niveles (ejercicio y campos). Devuelve {ejercicio: {campo: texto}}."""
    datos, actual = {}, None
    for n, linea in enumerate(pathlib.Path(ruta).read_text(encoding="utf-8").splitlines(), 1):
        sin_comentario = re.sub(r"(^|\s)#.*$", "", linea).rstrip()
        if not sin_comentario.strip():
            continue
        m = re.match(r"^(\w+):\s*$", sin_comentario)
        if m:
            actual = m.group(1)
            datos[actual] = {}
            continue
        m = re.match(r"^\s+(\w+):\s*(.*)$", sin_comentario)
        if m and actual:
            valor = m.group(2).strip().strip("'\"").strip()
            datos[actual][m.group(1)] = valor
            continue
        raise SystemExit(f"{ruta}, línea {n}: no entiendo \"{linea.strip()}\". "
                         "Cada respuesta va así:   campo: valor   (con dos espacios al inicio)")
    return datos


# Comparación ---------------------------------------------------------------------------------------

PISTAS = {
    "red": "la dirección de red tiene todos los bits de host en 0. Buscá el múltiplo del tamaño de bloque",
    "mascara": "contá los bits en 1 del prefijo y pasalos a decimal por octeto",
    "broadcast": "el broadcast es la última dirección del bloque: la red más el tamaño del bloque, menos 1",
    "primer_host": "es la dirección de red más 1",
    "ultimo_host": "es el broadcast menos 1",
    "hosts_utiles": "2 elevado a los bits de host, menos 2 (la red y el broadcast)",
    "prefijo": "buscá cuántos bits tenés que pedir prestados o dejar para hosts",
    "subredes": "2 elevado a los bits que pediste prestados",
    "hosts_por_subred": "2 elevado a los bits de host que quedan, menos 2",
    "subred_pedida": "la primera subred es la número 1 y arranca en la red original; cada una suma un bloque",
    "broadcast_pedida": "la subred siguiente menos 1",
    "misma_red": "sacá la red de las dos direcciones con la misma máscara y comparalas",
    "wildcard": "es la máscara al revés: 255 menos cada octeto",
    "resumen": "escribí las redes en binario y quedate con los bits que tienen en común",
    "abreviada": "quitá los ceros a la izquierda de cada grupo y cambiá por :: el grupo de ceros más largo, una sola vez",
    "expandida": "8 grupos de 4 dígitos hexadecimales, con todos los ceros",
    "gateway": "en este curso el gateway es el primer host de cada red",
    "red_ip1": "hacé un AND entre la dirección y la máscara, octeto por octeto",
    "red_ip2": "hacé un AND entre la dirección y la máscara, octeto por octeto",
}


def pista(campo):
    if campo in PISTAS:
        return PISTAS[campo]
    for sufijo in ("_red", "_gateway", "_broadcast"):
        if campo.endswith(sufijo):
            base = "Ordená los segmentos de más hosts a menos y asigná cada uno justo después del anterior. "
            return base + PISTAS.get(sufijo[1:], "") if sufijo != "_red" else \
                base + "Va en formato red/prefijo, por ejemplo 192.168.1.0/26"
    return ""


def interpretar(campo, texto, valor_esperado):
    """Convierte el texto del estudiante al mismo tipo que el valor esperado. Devuelve (valor, problema)."""
    texto = texto.strip()
    try:
        if isinstance(valor_esperado, int):
            return int(texto.replace(",", "").replace(" ", "")), None
        if campo in ("mascara", "prefijo"):
            if texto.lstrip("/").isdigit():
                prefijo = int(texto.lstrip("/"))
            else:
                prefijo = ipaddress.ip_network(f"0.0.0.0/{texto}").prefixlen
            if campo == "prefijo":
                return prefijo, None
            return ipaddress.ip_network(f"0.0.0.0/{prefijo}").netmask, None
        if isinstance(valor_esperado, str) and campo == "misma_red":
            t = texto.lower().replace("í", "i")
            if t not in ("si", "no"):
                return None, "respondé si o no"
            return t, None
        if isinstance(valor_esperado, str):
            return texto.lower(), None
        if isinstance(valor_esperado, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
            if "/" not in texto:
                return None, "va con prefijo, por ejemplo 192.168.1.0/26"
            try:
                return ipaddress.ip_network(texto, strict=True), None
            except ValueError:
                return None, f"{texto} no es una dirección de red: tiene bits de host encendidos"
        return ipaddress.ip_address(texto), None
    except ValueError:
        return None, f"no entiendo \"{texto}\" como respuesta para {campo}"


def revisar(ruta):
    respuestas = leer(ruta)
    filas = []
    for p in PREGUNTAS:
        bloque = respuestas.get(p["id"], {})
        for campo, correcto in esperado(p).items():
            texto = bloque.get(campo, "")
            if campo not in bloque:
                filas.append((p["id"], campo, "falta", "el campo no está en el archivo; no lo borrés"))
                continue
            if not texto:
                filas.append((p["id"], campo, "pendiente", ""))
                continue
            valor, problema = interpretar(campo, texto, correcto)
            if problema:
                filas.append((p["id"], campo, "revisar", problema))
            elif valor == correcto:
                filas.append((p["id"], campo, "bien", ""))
            elif campo == "abreviada" and ipaddress.IPv6Address(texto) == ipaddress.IPv6Address(p["ip"]):
                filas.append((p["id"], campo, "revisar", "es la misma dirección, pero no está abreviada al máximo"))
            else:
                filas.append((p["id"], campo, "revisar", f"\"{texto}\" no es. Pista: {pista(campo)}"))
    return filas


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("archivo", nargs="?", default=str(RAIZ / "ejercicios" / "subneteo.yml"))
    ap.add_argument("--soluciones", action="store_true", help="revisa soluciones/subneteo.yml")
    a = ap.parse_args()
    ruta = RAIZ / "soluciones" / "subneteo.yml" if a.soluciones else pathlib.Path(a.archivo)
    if not ruta.exists():
        sys.exit(f"No encuentro {ruta}.")

    filas = revisar(ruta)
    cuenta = {"bien": 0, "revisar": 0, "pendiente": 0, "falta": 0}
    por_ejercicio = {}
    for ej, campo, estado, detalle in filas:
        cuenta[estado] += 1
        por_ejercicio.setdefault(ej, []).append((campo, estado, detalle))

    print(f"Revisando {ruta}\n")
    for ej, campos in por_ejercicio.items():
        malos = [c for c in campos if c[1] != "bien"]
        if not malos:
            print(f"{ej}  BIEN")
        elif all(c[1] == "pendiente" for c in campos):
            print(f"{ej}  PENDIENTE")
        else:
            print(f"{ej}  {len(campos) - len(malos)} de {len(campos)} campos bien")
            for campo, estado, detalle in malos:
                print(f"     {campo:<22} {estado.upper():<10} {detalle}".rstrip())

    print(f"\nResumen: {cuenta['bien']} campos bien, {cuenta['revisar']} por revisar, "
          f"{cuenta['pendiente']} sin responder, {cuenta['falta']} borrados.")
    if cuenta["revisar"] or cuenta["pendiente"] or cuenta["falta"]:
        print("Corregí lo que dice REVISAR o PENDIENTE y volvé a correr este archivo.")
        return 1
    print("Todo bien. Ahora intentá explicarle a alguien cómo sacaste cada uno.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
