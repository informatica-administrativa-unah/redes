# Tema 05. Soluciones

## Ejercicio 1

`ff00` = `1111 1111 0000 0000`. `0db8` = `0000 1101 1011 1000`. `acad` = `1010 1100 1010 1101`. Cada grupo tiene 16 bits (4 dígitos de 4 bits).

## Ejercicio 2

1. `2001:db8:0:1::a0`. La secuencia larga de ceros son los grupos 5 a 7; el grupo 3 es un solo cero y se escribe `0`.
2. `fe80::202:b3ff:fe1e:8329`
3. `2001:db8:acad::`
4. `::1`
5. `2001:db8:0:0:abcd::`. Hay dos secuencias: dos ceros (grupos 3 y 4) y tres ceros (grupos 6 a 8). Va en la más larga, aunque esté a la derecha.

## Ejercicio 3

1. `2001:0db8:acad:0030:0000:0000:0000:0001`
2. `fe80:0000:0000:0000:0000:0000:000a:000b`
3. `2001:0db8:0000:0000:0000:0000:0000:0000`
4. `0000:0000:0000:0000:0000:0000:0000:0001`

## Ejercicio 4

1. `2001:db8::1::5`: mal, `::` dos veces.
2. `2001:db8:acad:10::g1`: mal, `g` no es un dígito hexadecimal.
3. `2001:db8:0:0:0:0:0:0:1`: mal, tiene 9 grupos.
4. `fe80::1`: bien.

## Ejercicio 5

| Dirección | Tipo |
|---|---|
| `2001:db8:acad:10::25` | Unicast global (de documentación, en la vida real sería una 2000::/3 asignada) |
| `fe80::1` | Enlace local |
| `fd12:3456:789a:1::10` | Local única (ULA) |
| `::1` | Loopback |
| `ff02::1` | Multicast, todos los nodos de la red local |
| `ff02::2` | Multicast, todos los routers de la red local |
| `::` | Sin especificar |

## Ejercicio 6

1. `2001:db8:acad:40::/64`
2. `2001:db8:acad:ff01::/64`
3. `2001:db8:acad:1200::/56`. Con /56 la red llega hasta la mitad del cuarto grupo: 48 bits más 8, los dos primeros dígitos de `1234`. Los otros dos van en cero.

## Ejercicio 7

MAC `00:50:56:aa:bb:cc`:

1. Partir en dos y meter `fffe`: `00 50 56 ff fe aa bb cc`
2. Primer byte `00` = `0000 0000`. Invertir el séptimo bit (el segundo de la derecha): `0000 0010` = `02`.
3. Resultado: `0250:56ff:feaa:bbcc`

MAC `3c:52:82:11:22:33`:

1. `3c 52 82 ff fe 11 22 33`
2. `3c` = `0011 1100`. Invertir el séptimo bit: `0011 1110` = `3e`.
3. Resultado: `3e52:82ff:fe11:2233`

## Ejercicio 8

De /48 a /64 hay 16 bits: 65 536 subredes /64. De /48 a /52 hay 4 bits: 16 sucursales, cada una con 2 a la 12, 4096 subredes /64. Contando desde la primera (`0000`), la tercera es `2001:db8:acad:2000::/52`.

## Ejercicio 9

1. Dirección IPv6: unicast global, prefijo `2001:db8:acad:40::/64` de la red de San Pedro Sula. La parte de interfaz no tiene `fffe`, así que no es EUI 64: Windows la generó al azar.
2. Dirección temporal: otra global del mismo prefijo, que Windows cambia cada cierto tiempo y usa para salir a internet por privacidad.
3. Enlace local: la `fe80::` que toda interfaz tiene. El `%11` es el número de la interfaz.
4. Puerta de enlace: los routers anuncian su dirección de enlace local como gateway. Es así por diseño: la enlace local no cambia si la organización cambia de proveedor y de prefijo.

Las dos globales salieron por SLAAC: el router mandó un anuncio con el prefijo `2001:db8:acad:40::/64` y la PC armó las direcciones con identificadores propios.

## Ejercicio 10

1. Falta `ipv6 unicast-routing` en el modo global. Sin eso el router no manda anuncios de router y las PC nunca reciben el prefijo. Se comprueba con `show running-config | include unicast-routing`.
2. La interfaz está apagada o es otra. Si está en `shutdown` o la dirección se puso en la interfaz que no da a la LAN, las PC no reciben nada. Se comprueba con `show ipv6 interface brief`, que muestra el estado y las direcciones de cada interfaz.

También puede ser que las PC tengan IPv6 deshabilitado en la tarjeta, pero entonces no tendrían ni la fe80::.
