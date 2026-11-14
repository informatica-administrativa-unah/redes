# Tema 09. Ejercicios

## Ejercicio 1

Una PC 192.168.30.14 de bodega abre 198.51.100.80 por HTTPS, y R_TGU la traduce a 203.0.113.2. Escribí cuál es el inside local, el inside global y el outside global.

## Ejercicio 2

¿Qué tipo de NAT usarías en cada caso? Justificá.

1. Cien PC que navegan, con una sola IP pública.
2. Un servidor de correo que tiene que recibir conexiones desde internet en todos sus puertos, con una pública propia.
3. Solo el puerto 443 de un servidor, con la única pública de la empresa.

## Ejercicio 3

Escribí las listas de acceso estándar (número y wildcard) para que se traduzcan:

1. Solo la VLAN de ventas, 192.168.10.0/24.
2. Las tres LAN de Tegucigalpa: 192.168.10.0/24, 192.168.20.0/24 y 192.168.30.0/24.
3. Todo 192.168.40.0/22.

## Ejercicio 4

Completá la tabla de PAT si estas conexiones pasan por R_TGU al mismo tiempo (pública 203.0.113.2) y el router mantiene el puerto de origen siempre que puede:

| Inside local | Outside global |
|---|---|
| 192.168.10.5:49200 | 198.51.100.80:443 |
| 192.168.40.9:49200 | 198.51.100.80:443 |
| 192.168.50.7:51515 | 192.0.2.53:53 |

## Ejercicio 5

Esta configuración no funciona: nadie navega. Encontrá los tres errores.

```
interface g0/0.10
 ip nat outside
interface g0/1
 ip nat inside
access-list 1 permit 192.168.10.0 255.255.255.0
ip nat inside source list 1 interface g0/1 overload
```

## Ejercicio 6

Después de configurar PAT, Tegucigalpa navega pero San Pedro Sula y La Ceiba no, aunque llegan sin problema al servidor 192.168.20.10. ¿Qué falta? Escribí los comandos.

## Ejercicio 7

La empresa quiere publicar dos servicios con su única pública 203.0.113.2: el catálogo web (192.168.20.30, TCP 443) y el acceso remoto de TI por SSH (192.168.99.10, TCP 22), este último por el puerto externo 2222. Escribí la configuración. Después escribí un párrafo sobre los riesgos del segundo y qué harías en lugar de publicarlo así.

## Ejercicio 8

Esta es la salida de `show ip nat translations` en R_TGU:

```
Pro  Inside global      Inside local        Outside local      Outside global
tcp  203.0.113.2:443    192.168.20.30:443   ---                ---
tcp  203.0.113.2:1025   192.168.10.25:51000 198.51.100.80:443  198.51.100.80:443
udp  203.0.113.2:50122  192.168.20.40:50122 192.0.2.53:53      192.0.2.53:53
```

Explicá cada línea. ¿Por qué la primera no tiene direcciones externas?

## Ejercicio 9

Un cliente se queja de que no puede entrar al catálogo desde su casa, pero desde la oficina, usando la dirección pública 203.0.113.2, sí... o eso dicen. Otro técnico dice que desde la oficina tampoco funciona por la pública, pero por la privada sí. Explicá por qué entrar a la pública desde adentro puede fallar aunque NAT esté bien, y cómo se resuelve con DNS.

## Ejercicio 10

El proveedor le cambia el servicio a la empresa y ahora el router recibe la IP 100.72.14.9 en g0/1. Desde ese día el catálogo publicado no se ve desde internet. ¿Qué pasó y qué opciones tiene la empresa?
