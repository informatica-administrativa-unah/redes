# Tema 03. Soluciones

## Ejercicio 1

Para 3 subredes: 2 a la 1 da 2, no alcanza; 2 a la 2 da 4, alcanza. Se prestan 2 bits: /26, máscara 255.255.255.192, bloque 64.

| N.° | Subred | Primer host | Último host | Broadcast |
|---:|---|---|---|---|
| 1 | 192.168.80.0/26 | .1 | .62 | .63 |
| 2 | 192.168.80.64/26 | .65 | .126 | .127 |
| 3 | 192.168.80.128/26 | .129 | .190 | .191 |
| 4 | 192.168.80.192/26 | .193 | .254 | .255 |

Queda 1 libre.

## Ejercicio 2

Para 6 hosts: 2 a la 3 menos 2 da 6, alcanza justo. h = 3, prefijo /29, bloque 8. Salen 2 a la 5, 32 subredes.

| N.° | Subred | Broadcast |
|---:|---|---|
| 1 | 192.168.90.0/29 | 192.168.90.7 |
| 2 | 192.168.90.8/29 | 192.168.90.15 |
| 3 | 192.168.90.16/29 | 192.168.90.23 |
| 4 | 192.168.90.24/29 | 192.168.90.31 |
| 32 | 192.168.90.248/29 | 192.168.90.255 |

Una caja más en un segmento y ya no cabe: conviene preguntar si van a crecer.

## Ejercicio 3

2 a la 4 da 16, no alcanza; 2 a la 5 da 32. Se prestan 5 bits: /21, máscara 255.255.248.0. Se forman 32 subredes de 2046 hosts útiles (11 bits de host).

Octeto interesante: el tercero, bloque 8. Subred 15: (15 menos 1) por 8, 112. Subred 172.25.112.0/21, broadcast 172.25.119.255.

## Ejercicio 4

Para 1000 hosts: 2 a la 10 menos 2 da 1022, alcanza (2 a la 9 menos 2 da 510, no). h = 10, prefijo /22. Bits prestados: 22 menos 16, 6. Salen 64 segmentos.

## Ejercicio 5

1. /26, bloque 64 en el cuarto octeto. 150 cae entre 128 y 192: subred 192.168.80.128/26, broadcast 192.168.80.191.
2. /21, bloque 8 en el tercer octeto. 99 cae entre 96 y 104: subred 172.25.96.0/21, broadcast 172.25.103.255.
3. /19, bloque 32 en el tercer octeto. 77 cae entre 64 y 96: subred 10.200.64.0/19, broadcast 10.200.95.255.

## Ejercicio 6

2 a la 8 da 256, no alcanza; 2 a la 9 da 512. Prefijo 8 más 9, /17, máscara 255.255.128.0. Bloque 128 en el tercer octeto, así que por cada valor del segundo octeto caben 2 subredes.

Subred 300: restá 1, 299. Dividí entre 2: 149 y sobra 1. Segundo octeto 149, tercero 1 por 128, 128. Subred 10.149.128.0/17, broadcast 10.149.255.255.

## Ejercicio 7

No se puede. Para 10 subredes hacen falta 4 bits prestados (2 a la 4 da 16), y eso deja 4 bits de host: 2 a la 4 menos 2, 14 hosts. No alcanzan para 20. Si se dejan 5 bits de host (30 hosts), solo quedan 3 bits de subred: 8 subredes, no 10.

Formas de arreglarlo: aceptar 8 subredes de 30 hosts, aceptar 16 subredes de 14 hosts, usar una red más grande (por ejemplo una /23 da 16 subredes /27 de 30 hosts), o usar VLSM si no todas las redes necesitan 20 hosts.

## Ejercicio 8

Manda la más grande: 25 hosts. 2 a la 5 menos 2 da 30, alcanza. Prefijo /27, bloque 32, 8 subredes.

| Red | Subred | Gateway | Rango para equipos | Broadcast |
|---|---|---|---|---|
| Ventas | 192.168.40.0/27 | .1 | .2 a .30 | .31 |
| Bodega | 192.168.40.32/27 | .33 | .34 a .62 | .63 |
| Administración | 192.168.40.64/27 | .65 | .66 a .94 | .95 |
| Cámaras | 192.168.40.96/27 | .97 | .98 a .126 | .127 |
| Wifi clientes | 192.168.40.128/27 | .129 | .130 a .158 | .159 |
| Reserva | 192.168.40.160/27 | | | .191 |
| Reserva | 192.168.40.192/27 | | | .223 |
| Reserva | 192.168.40.224/27 | | | .255 |

Ojo con el wifi de clientes: 25 celulares es poco para una tienda. Si se llena, es la primera red que hay que agrandar.

## Ejercicio 9

1. Bodega: el broadcast de 192.168.60.32/27 es .63, no .64 (.64 es la red siguiente).
2. Gerencia: 192.168.60.60 no es una dirección de red /27, porque no es múltiplo de 32. La subred correcta es 192.168.60.64/27, con gateway .65 y broadcast .95.
3. Cámaras: el gateway no puede ser .96, que es la dirección de red. Va .97.

## Ejercicio 10

1. De /24 a /30 hay 6 bits: 2 a la 6, 64.
2. De /22 a /26 hay 4 bits: 16.
3. De /20 a /24 hay 4 bits: 16.
4. Una /21 tiene 11 bits de host: 2048 direcciones. De /21 a /29 hay 8 bits: 256 subredes /29.
