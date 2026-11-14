# Tema 04. Soluciones

## Ejercicio 1

| Hosts | Prefijo | Por qué |
|---:|---|---|
| 5 | /29 | 8 menos 2 da 6 |
| 14 | /28 | 16 menos 2 da 14, justo |
| 15 | /27 | 14 ya no alcanza, 32 menos 2 da 30 |
| 33 | /26 | 62 |
| 100 | /25 | 126 |
| 254 | /24 | 254, justo |
| 255 | /23 | 510 |
| 600 | /22 | 1022 |

## Ejercicio 2

Orden: ventas 50 (/26), contabilidad 20 (/27), gerencia 8 (/28), WAN 1 y WAN 2 (/30). Suma: 64 más 32 más 16 más 4 más 4, 120.

| Red | Subred | Gateway | Último host | Broadcast |
|---|---|---|---|---|
| Ventas | 192.168.150.0/26 | .1 | .62 | .63 |
| Contabilidad | 192.168.150.64/27 | .65 | .94 | .95 |
| Gerencia | 192.168.150.96/28 | .97 | .110 | .111 |
| WAN 1 | 192.168.150.112/30 | .113 | .114 | .115 |
| WAN 2 | 192.168.150.116/30 | .117 | .118 | .119 |

Libre desde 192.168.150.120. La primera /26 libre completa es 192.168.150.128/26.

## Ejercicio 3

Orden: Tegucigalpa 400 (/23), San Pedro Sula 200 (/24), La Ceiba 100 (/25), servidores 14 (/28), dos WAN (/30). Suma: 512 más 256 más 128 más 16 más 8, 920. Caben en 1024.

| Red | Subred | Gateway | Último host | Broadcast |
|---|---|---|---|---|
| Tegucigalpa | 172.30.0.0/23 | 172.30.0.1 | 172.30.1.254 | 172.30.1.255 |
| San Pedro Sula | 172.30.2.0/24 | 172.30.2.1 | 172.30.2.254 | 172.30.2.255 |
| La Ceiba | 172.30.3.0/25 | 172.30.3.1 | 172.30.3.126 | 172.30.3.127 |
| Servidores | 172.30.3.128/28 | 172.30.3.129 | 172.30.3.142 | 172.30.3.143 |
| WAN 1 | 172.30.3.144/30 | 172.30.3.145 | 172.30.3.146 | 172.30.3.147 |
| WAN 2 | 172.30.3.148/30 | 172.30.3.149 | 172.30.3.150 | 172.30.3.151 |

## Ejercicio 4

Ventas 120 pide /25 (128), bodega 60 pide /26 (64), wifi 40 pide /26 (64), administración 20 pide /27 (32). Suma: 288. No cabe en 256.

Cambio posible: sacar el wifi de clientes a otra red, por ejemplo 192.168.6.0/26. Sin el wifi la suma da 224 y cabe. Otra opción es usar 192.168.4.0/23 para todo.

## Ejercicio 5

Errores:

1. No está ordenado de mayor a menor: administración (12) quedó primero.
2. Ventas /26 empieza en .16, que no es múltiplo de 64.
3. Bodega /27 en .80 no es múltiplo de 32.

Plan corregido (orden ventas 55, bodega 25, administración 12, WAN):

| Red | Subred | Broadcast |
|---|---|---|
| Ventas | 192.168.9.0/26 | .63 |
| Bodega | 192.168.9.64/27 | .95 |
| Administración | 192.168.9.96/28 | .111 |
| WAN | 192.168.9.112/30 | .115 |

## Ejercicio 6

1. 8 es `00001 000` y 15 es `00001 111`: 5 bits iguales en el tercer octeto. Resumen 192.168.8.0/21. Cubre de .8.0 a .15.255, exactamente las ocho.
2. 32 es `001000 00` y 35 es `001000 11`: 6 bits iguales. Resumen 10.10.32.0/22. Cubre de .32.0 a .35.255, exactamente las cuatro.

## Ejercicio 7

172.16.20.0/22 cubre de 172.16.20.0 a 172.16.23.255: incluye 172.16.23.0/24, que está en otra sucursal. El router mandaría ese tráfico al lugar equivocado. Rutas exactas: 172.16.20.0/23 (cubre .20 y .21) y 172.16.22.0/24.

## Ejercicio 8

Las tres juntas no se resumen en una sola ruta exacta, porque La Ceiba es solo una /26 dentro de 172.16.3.0/24: una ruta exacta necesitaría 172.16.0.0/23, 172.16.2.0/24 y 172.16.3.0/26. Pero todo lo asignado en el caso (incluidos servidores y enlaces) queda dentro de 172.16.0.0/22, de 172.16.0.0 a 172.16.3.255, y lo libre de 172.16.3.108 en adelante no está asignado a ningún otro sitio. Entonces 172.16.0.0/22 es un resumen aceptable para anunciar todo eso hacia afuera, siempre que se documente que lo libre de ese bloque es reserva de esos sitios.

## Ejercicio 9

Orden: ventas 120 (/25), wifi 60 (/26), bodega 50 (/26), administración 20 (/27), WAN (/30). Suma: 128 más 64 más 64 más 32 más 4, 292.

| Red | Subred | Gateway | Último host | Broadcast |
|---|---|---|---|---|
| Ventas | 172.16.4.0/25 | 172.16.4.1 | 172.16.4.126 | 172.16.4.127 |
| Wifi clientes | 172.16.4.128/26 | 172.16.4.129 | 172.16.4.190 | 172.16.4.191 |
| Bodega | 172.16.4.192/26 | 172.16.4.193 | 172.16.4.254 | 172.16.4.255 |
| Administración | 172.16.5.0/27 | 172.16.5.1 | 172.16.5.30 | 172.16.5.31 |
| WAN | 172.16.5.32/30 | 172.16.5.33 | 172.16.5.34 | 172.16.5.35 |

Libre: de 172.16.5.36 a 172.16.5.255, y completas 172.16.6.0/24 y 172.16.7.0/24. Toda Choluteca se sigue resumiendo con 172.16.4.0/22.

## Ejercicio 10

Respuesta modelo: "Si cada sucursal tiene su bloque, los routers de las otras sucursales necesitan una sola ruta para llegar a toda ella, sin importar cuántas redes internas tenga. Eso hace las tablas más cortas y los cambios más seguros: agregar una red en Choluteca no obliga a tocar los routers de Tegucigalpa. También ayuda a diagnosticar, porque con ver la dirección ya sabés de qué sucursal es. Las direcciones privadas no cuestan, así que dejar espacio libre no es un gasto; lo caro es tener que renumerar una sucursal entera cuando crece y ya no le cabe nada al lado."
