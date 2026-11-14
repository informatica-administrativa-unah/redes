# Tema 02. Soluciones

Podés comprobar cualquier cuenta con el ejemplo [`01_calcular_con_python.py`](../ejemplos/01_calcular_con_python.py).

## Ejercicio 1

| Decimal | Binario |
|---:|---|
| 10 | 00001010 |
| 172 | 10101100 |
| 192 | 11000000 |
| 224 | 11100000 |
| 255 | 11111111 |
| 99 | 01100011 (64 + 32 + 2 + 1) |

## Ejercicio 2

1. 192.168.1.10
2. 10.255.128.1

## Ejercicio 3

/19 es 255.255.224.0. /27 es 255.255.255.224. 255.255.255.248 es /29. 255.255.240.0 es /20. /12 es 255.240.0.0.

## Ejercicio 4

| Dirección | Tipo |
|---|---|
| 10.200.3.4 | Privada (10.0.0.0/8) |
| 172.31.255.1 | Privada (172.16.0.0/12 llega hasta 172.31.255.255) |
| 172.32.0.1 | Pública: ya se salió del rango privado |
| 192.168.300.1 | Inválida: 300 no cabe en un octeto |
| 127.0.0.53 | Especial: loopback (todo 127.0.0.0/8 lo es) |
| 169.254.10.10 | Especial: enlace local o APIPA, la PC no recibió DHCP |
| 100.70.1.1 | Especial: espacio compartido de proveedores, 100.64.0.0/10 |
| 8.8.8.8 | Pública |
| 203.0.113.5 | Especial: reservada para documentación |

## Ejercicio 5

/29: 6. /25: 126. /22: 1022. /18: 16 382. /30: 2.

## Ejercicio 6

1. 192.168.50.130/25. Octeto interesante: el cuarto, máscara 128, bloque 128. Múltiplos: 0, 128. El 130 cae en 128. Red 192.168.50.128, broadcast 192.168.50.255, hosts de .129 a .254, 126 útiles.
2. 172.16.77.9/20. Máscara 255.255.240.0, octeto interesante el tercero, bloque 16. Múltiplos: 0, 16, 32, 48, 64, 80. El 77 cae en 64. Red 172.16.64.0, broadcast 172.16.79.255 (la siguiente red es 172.16.80.0), hosts de 172.16.64.1 a 172.16.79.254, 4094 útiles.
3. 10.45.200.17/12. Máscara 255.240.0.0, octeto interesante el segundo, bloque 16. Múltiplos: 0, 16, 32, 48. El 45 cae en 32. Red 10.32.0.0, broadcast 10.47.255.255, hosts de 10.32.0.1 a 10.47.255.254. Bits de host: 20, así que 1 048 576 menos 2, 1 048 574 útiles.

## Ejercicio 7

La red va de 172.16.32.0 (red) a 172.16.35.255 (broadcast), porque /22 tiene bloque 4 en el tercer octeto.

1. 172.16.32.0: no, es la dirección de red.
2. 172.16.33.255: sí. Termina en 255 pero está en medio del rango.
3. 172.16.35.255: no, es el broadcast.
4. 172.16.36.1: no, es de otra red (172.16.36.0/22).
5. 172.16.34.0: sí, también está en medio del rango.

## Ejercicio 8

1. 255.255.255.100: inválida. 100 es `01100100`, los 1 no van seguidos desde la izquierda.
2. 255.255.0.255: inválida. Hay 1 después de un octeto de ceros.
3. 255.255.254.0: válida, /23.
4. 255.0.255.0: inválida, mismo problema que la 2.
5. 255.255.255.252: válida, /30.

## Ejercicio 9

La máscara 255.255.255.192 es /26, bloque 64. La PC 192.168.40.25 está en la red 192.168.40.0/26 (de .0 a .63). El gateway 192.168.40.65 está en la red 192.168.40.64/26. La PC no puede llegar a su gateway porque está en otra red, entonces no sale.

Dos arreglos posibles:

1. Si la red de la sucursal es /24, como en el plan de la empresa, la máscara correcta es 255.255.255.0 y el gateway 192.168.40.1.
2. Si de verdad la red es /26, hay que poner un gateway dentro de 192.168.40.0/26, normalmente 192.168.40.1, y configurar esa dirección en el router.

## Ejercicio 10

1. Mal: 192.168.50.0 es la dirección de red.
2. Mal: con /16 la PC cree que todo 192.168.x.x es su red local. Va a intentar hablar directo (con ARP) con equipos de Tegucigalpa como 192.168.20.10 en vez de mandarlos al gateway, y no va a llegar.
3. Mal: 192.168.50.255 es el broadcast de la red.
