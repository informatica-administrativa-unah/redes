# Tema 04. Ejercicios

Hacelos en papel. Los niveles 5 y 6 de [`ejercicios/subneteo.yml`](../../ejercicios/subneteo.yml) también son de este tema y se revisan solos.

Reglas para todos: se asigna de mayor a menor, cada red pegada a la anterior, si dos empatan va primero la que aparece antes en la lista, y el gateway es el primer host.

## Ejercicio 1

¿Qué prefijo le toca a una red que necesita 5, 14, 15, 33, 100, 254, 255 y 600 hosts?

## Ejercicio 2

Con 192.168.150.0/24: gerencia 8 hosts, ventas 50, contabilidad 20 y dos enlaces WAN. Hacé la tabla VLSM completa (subred, gateway, último host, broadcast) y decí dónde empieza el espacio libre.

## Ejercicio 3

Con 172.30.0.0/22: Tegucigalpa 400 hosts, San Pedro Sula 200, La Ceiba 100, servidores 14 y dos enlaces WAN. Hacé la tabla VLSM.

## Ejercicio 4

¿Cabe este pedido en 192.168.5.0/24? Ventas 120, bodega 60, wifi 40 y administración 20. Mostrá la suma de bloques. Si no cabe, proponé un cambio concreto.

## Ejercicio 5

Este plan VLSM sobre 192.168.9.0/24 tiene errores. Encontralos y escribí el plan corregido.

| Red | Hosts | Subred |
|---|---:|---|
| Administración | 12 | 192.168.9.0/28 |
| Ventas | 55 | 192.168.9.16/26 |
| Bodega | 25 | 192.168.9.80/27 |
| WAN | 2 | 192.168.9.112/30 |

## Ejercicio 6

Calculá la ruta resumida de cada grupo y comprobá que no cubra de más.

1. De 192.168.8.0/24 a 192.168.15.0/24.
2. De 10.10.32.0/24 a 10.10.35.0/24.

## Ejercicio 7

Un técnico quiere resumir 172.16.20.0/24, 172.16.21.0/24 y 172.16.22.0/24 con 172.16.20.0/22. ¿Qué problema tiene? Escribí las rutas exactas que usarías si 172.16.23.0/24 está en otra sucursal.

## Ejercicio 8

En el caso resuelto 2 del tema, Tegucigalpa, San Pedro Sula y La Ceiba usan 172.16.0.0/23, 172.16.2.0/24 y 172.16.3.0/26. ¿Se pueden resumir las tres en una sola ruta exacta? ¿Qué ruta cubriría todo lo que se asignó en ese caso, contando servidores y enlaces?

## Ejercicio 9

Siguiendo el caso 2 del tema, abren una sucursal en Choluteca y le dan 172.16.4.0/22. Necesita ventas 120, wifi de clientes 60, bodega 50, administración 20 y un enlace WAN. Hacé la tabla VLSM y decí qué parte de la /22 queda libre.

## Ejercicio 10

Explicá en un párrafo, como si se lo contaras al gerente de TI de la empresa, por qué conviene que cada sucursal tenga un bloque de direcciones contiguo y con espacio para crecer, aunque al principio parezca que se desperdician direcciones.
