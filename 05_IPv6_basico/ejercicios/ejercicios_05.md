# Tema 05. Ejercicios

El nivel 7 de [`ejercicios/subneteo.yml`](../../ejercicios/subneteo.yml) también es de este tema y se revisa solo.

## Ejercicio 1

Convertí a binario los grupos `ff00`, `0db8` y `acad`. ¿Cuántos bits tiene cada grupo?

## Ejercicio 2

Abreviá al máximo siguiendo el RFC 5952:

1. `2001:0db8:0000:0001:0000:0000:0000:00a0`
2. `fe80:0000:0000:0000:0202:b3ff:fe1e:8329`
3. `2001:0db8:acad:0000:0000:0000:0000:0000`
4. `0000:0000:0000:0000:0000:0000:0000:0001`
5. `2001:0db8:0000:0000:abcd:0000:0000:0000`

## Ejercicio 3

Expandí a 8 grupos de 4 dígitos: `2001:db8:acad:30::1`, `fe80::a:b`, `2001:db8::`, `::1`.

## Ejercicio 4

¿Cuáles de estas direcciones están mal escritas y por qué? `2001:db8::1::5`, `2001:db8:acad:10::g1`, `2001:db8:0:0:0:0:0:0:1`, `fe80::1`.

## Ejercicio 5

Clasificá cada dirección según su tipo: `2001:db8:acad:10::25`, `fe80::1`, `fd12:3456:789a:1::10`, `::1`, `ff02::1`, `ff02::2`, `::`.

## Ejercicio 6

Dá la red de cada dirección con su prefijo:

1. `2001:db8:acad:40:1::99/64`
2. `2001:db8:acad:ff01::2/64`
3. `2001:db8:acad:1234:5678::1/56`

## Ejercicio 7

Calculá el identificador de interfaz EUI 64 para las MAC `00:50:56:aa:bb:cc` y `3c:52:82:11:22:33`. Mostrá el paso del séptimo bit.

## Ejercicio 8

La empresa recibe 2001:db8:acad::/48. ¿Cuántas subredes /64 tiene? Si cada sucursal recibe una /52, ¿cuántas sucursales caben y cuántas /64 tiene cada una? Escribí el bloque /52 de la tercera sucursal.

## Ejercicio 9

Una PC de San Pedro Sula muestra esto en `ipconfig`:

```
Dirección IPv6 . . . . . . . . : 2001:db8:acad:40:8c1f:3a9:12e4:77b0
Dirección IPv6 temporal . . . . : 2001:db8:acad:40:51d2:aa0e:9c3:1f2
Vínculo: dirección IPv6 local . : fe80::8c1f:3a9:12e4:77b0%11
Puerta de enlace predeterminada : fe80::1%11
```

Explicá qué es cada línea, por qué la puerta de enlace es una dirección fe80:: y cómo obtuvo la PC las dos primeras direcciones.

## Ejercicio 10

Un técnico configuró IPv6 en el router de La Ceiba con `ipv6 address 2001:db8:acad:50::1/64` en la interfaz de la LAN, pero las PC solo tienen dirección fe80:: y ninguna 2001:. Dá dos causas posibles y cómo comprobarías cada una.
