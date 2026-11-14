# Tema 03. Ejercicios

Estos se responden en papel. Además de estos, hacé los niveles 1 a 4 de [`ejercicios/subneteo.yml`](../../ejercicios/subneteo.yml), que se revisan solos con `python herramientas/revisar.py`.

En todos, la primera subred es la número 1 y se usan la subred cero y la de todos unos.

## Ejercicio 1

Dividí 192.168.80.0/24 en 3 subredes iguales usando la menor cantidad de bits. Hacé la tabla completa con subred, primer host, último host y broadcast. ¿Cuántas subredes quedan libres?

## Ejercicio 2

Con 192.168.90.0/24 hay que armar subredes de 6 hosts para las cajas registradoras. Decí el prefijo, cuántas subredes salen, y escribí las cuatro primeras y la última con su broadcast.

## Ejercicio 3

La red 172.25.0.0/16 se tiene que partir en 20 subredes iguales. Sacá el prefijo, la máscara, cuántas subredes se forman de verdad, los hosts útiles por subred y la subred número 15 con su broadcast.

## Ejercicio 4

Con la misma 172.25.0.0/16, ahora el pedido es por hosts: cada segmento necesita 1000 hosts. ¿Qué prefijo usás y cuántos segmentos salen?

## Ejercicio 5

¿A qué subred pertenece cada dirección? Dá la subred con prefijo y su broadcast.

1. 192.168.80.150/26
2. 172.25.99.3/21
3. 10.200.77.77/19

## Ejercicio 6

10.0.0.0/8 se reparte en al menos 500 subredes iguales. Dá el prefijo y la subred número 300 con su broadcast. Mostrá cómo la sacaste sin escribirlas todas.

## Ejercicio 7

Un compañero propone partir 192.168.1.0/24 en 10 subredes de 20 hosts cada una con máscara fija. ¿Se puede? Justificá con las dos fórmulas. Si no se puede, decí qué cambiarías del pedido para que sí se pueda.

## Ejercicio 8

San Pedro Sula usa 192.168.40.0/24 y necesita cinco redes: ventas (25 PC), bodega (18), administración (12), cámaras (10) y wifi de clientes (25). Diseñá el plan con máscara fija: prefijo, tabla con cada red, su gateway (primer host), rango para equipos y broadcast. Dejá las subredes que sobren marcadas como reserva.

## Ejercicio 9

Este plan para 192.168.60.0/24 con /27 tiene tres errores. Encontralos y corregilos.

| Red | Subred | Gateway | Broadcast |
|---|---|---|---|
| Ventas | 192.168.60.0/27 | 192.168.60.1 | 192.168.60.31 |
| Bodega | 192.168.60.32/27 | 192.168.60.33 | 192.168.60.64 |
| Gerencia | 192.168.60.60/27 | 192.168.60.61 | 192.168.60.91 |
| Cámaras | 192.168.60.96/27 | 192.168.60.96 | 192.168.60.127 |

## Ejercicio 10

Contestá sin listar las subredes:

1. ¿Cuántas /30 caben en una /24?
2. ¿Cuántas /26 caben en una /22?
3. ¿Cuántas /24 caben en una /20?
4. ¿Cuántas direcciones en total tiene una /21 y cuántas /29 caben adentro?
