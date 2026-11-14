# 05. IPv6 básico

IPv4 tiene unos 4300 millones de direcciones y se acabaron hace años: los registros regionales ya no tienen bloques libres para repartir como antes. Las redes siguieron funcionando gracias a NAT y a las direcciones privadas, pero esa solución tiene costos. IPv6 es el reemplazo: direcciones de 128 bits, tantas que no se van a acabar. Hoy convive con IPv4 en casi todas las redes grandes, y muchos proveedores de internet y de telefonía móvil ya lo entregan. Si administrás una red, lo vas a encontrar.

Este tema cubre lo que necesitás para leer, escribir y planear direcciones IPv6, y cómo un equipo obtiene una.

## Qué cambia respecto a IPv4

| | IPv4 | IPv6 |
|---|---|---|
| Largo | 32 bits | 128 bits |
| Escritura | Decimal con puntos: 192.168.10.1 | Hexadecimal con dos puntos: 2001:db8:acad:10::1 |
| Cantidad | Unos 4300 millones | 2 elevado a la 128, un número de 39 cifras |
| Broadcast | Sí | No existe. Se usa multicast |
| De IP a MAC | ARP | NDP (Neighbor Discovery), con mensajes ICMPv6 |
| Configuración automática | DHCP | SLAAC (sin servidor), DHCPv6, o las dos |
| NAT | Muy usado | No hace falta en el diseño normal |
| Encabezado | Variable, con suma de verificación | Fijo de 40 bytes, sin suma de verificación |
| Máscara | 255.255.255.0 o /24 | Solo prefijo: /64 |

## Cómo se escribe una dirección

128 bits se parten en 8 grupos de 16 bits. Cada grupo se escribe con 4 dígitos hexadecimales (cada dígito hexadecimal son 4 bits) y los grupos se separan con dos puntos.

```
2001:0db8:0000:0000:0000:ff00:0042:8329
```

Repaso de hexadecimal: va de 0 a 9 y sigue con a (10), b (11), c (12), d (13), e (14), f (15). Un grupo como `ff00` en binario es `1111 1111 0000 0000`.

### Las dos reglas para abreviar

Escribir 32 dígitos es largo, así que hay dos reglas, y el RFC 5952 dice cómo aplicarlas para que todos escribamos lo mismo:

1. Se quitan los ceros a la izquierda de cada grupo. `0db8` queda `db8`, `0042` queda `42`, `0000` queda `0`. Los ceros de la derecha no se tocan: `ff00` sigue siendo `ff00`.
2. Una sola vez en toda la dirección, una secuencia de dos o más grupos seguidos que valen 0 se cambia por `::`.

Detalles del RFC 5952 que se preguntan en examen:

1. Se usa `::` en la secuencia de ceros más larga.
2. Si hay dos secuencias del mismo largo, se usa en la primera (la de la izquierda).
3. No se usa `::` para un solo grupo de ceros; ahí se escribe `0`.
4. Las letras van en minúscula.

### Caso resuelto 1: abreviar

`2001:0db8:0000:0000:0000:ff00:0042:8329`

1. Quitar ceros a la izquierda: `2001:db8:0:0:0:ff00:42:8329`
2. La secuencia de ceros más larga son los grupos 3, 4 y 5: `2001:db8::ff00:42:8329`

### Caso resuelto 2: dos secuencias del mismo largo

`2001:0db8:0000:0000:0001:0000:0000:0001`

1. Sin ceros a la izquierda: `2001:db8:0:0:1:0:0:1`
2. Hay dos secuencias de dos ceros. Va en la primera: `2001:db8::1:0:0:1`

`2001:db8:0:0:1::1` representa la misma dirección y un equipo la acepta, pero no es la forma recomendada.

### Caso resuelto 3: expandir

`fe80::1a:2b`

1. Contá los grupos que hay: `fe80`, `1a`, `2b`, tres. Faltan cinco.
2. El `::` vale esos cinco grupos de ceros: `fe80:0:0:0:0:0:1a:2b`
3. Completá cada grupo a 4 dígitos: `fe80:0000:0000:0000:0000:0000:001a:002b`

Por qué `::` solo se puede usar una vez: si escribieras `2001::1::1`, no habría forma de saber cuántos ceros van en cada hueco.

## Prefijos

En IPv6 no hay máscara en decimal, solo prefijo: `2001:db8:acad:10::25/64`. El significado es el mismo que en IPv4: los primeros 64 bits son la red.

Los tamaños que vas a ver:

| Prefijo | Para qué |
|---|---|
| /32 | Lo que un registro regional le da a un proveedor de internet |
| /48 | Lo que se le suele dar a una organización o un sitio |
| /56 | Lo que algunos proveedores le dan a un hogar |
| /64 | Una red local. Es el tamaño estándar de una subred |
| /127 | Enlaces entre routers (RFC 6164) |
| /128 | Una sola dirección, por ejemplo una interfaz loopback |

¿Por qué /64 si una red nunca va a tener 2 elevado a la 64 equipos? Porque la configuración automática (SLAAC) usa los 64 bits de la derecha para el identificador de la interfaz. Una red más chica que /64 rompe SLAAC. En IPv6 no se ahorran direcciones dentro de una LAN: se ahorran prefijos.

## Tipos de direcciones

En IPv6 una interfaz normalmente tiene varias direcciones a la vez. Esto confunde al principio: `ipconfig` te puede mostrar tres o cuatro y está bien.

| Tipo | Prefijo | Para qué |
|---|---|---|
| Unicast global | 2000::/3 (empiezan con 2 o 3) | Como una IP pública: se enruta en internet |
| Enlace local | fe80::/10 | Solo sirve dentro de la red local. Toda interfaz con IPv6 tiene una, aunque no haya router. Los routers la usan como gateway |
| Local única (ULA) | fc00::/7, en la práctica fd00::/8 | Parecidas a las privadas de IPv4: dentro de la organización, no salen a internet |
| Loopback | ::1/128 | El equipo hablando consigo mismo, como 127.0.0.1 |
| Sin especificar | ::/128 | "Todavía no tengo dirección" |
| Multicast | ff00::/8 | A un grupo. ff02::1 es "todos los nodos de la red local", ff02::2 "todos los routers" |
| Documentación | 2001:db8::/32 | Para ejemplos y libros (RFC 3849). Todo este curso la usa |

Fijate que no hay broadcast. Lo que en IPv4 se hacía con broadcast (ARP, DHCP) en IPv6 se hace con grupos multicast, y así no se molesta a todos los equipos.

## Estructura de una dirección unicast global

Con una /48 de la organización y subredes /64, una dirección se lee así:

```
2001:0db8:acad : 0010 : 0000:0000:0000:0025
|-- prefijo --|  |sub|  |-- id de interfaz --|
   48 bits      16 bits       64 bits
```

1. Prefijo global de enrutamiento (48 bits): lo asigna el proveedor. Identifica a la organización en internet.
2. Identificador de subred (16 bits): lo elige la organización. Da 65 536 subredes /64.
3. Identificador de interfaz (64 bits): identifica al equipo dentro de la subred.

## Subneteo en IPv6

Es mucho más simple que en IPv4 porque se trabaja con el cuarto grupo, el de subred, y no hace falta pensar en cuántos hosts caben.

### Caso resuelto 4: plan de IPv6 para Comercial El Guayabo

El proveedor le da a la empresa 2001:db8:acad::/48. Usamos el grupo de subred para que coincida con las redes de IPv4, así es fácil de recordar:

| Red | IPv4 | IPv6 | Gateway IPv6 |
|---|---|---|---|
| Tegucigalpa, ventas | 192.168.10.0/24 | 2001:db8:acad:10::/64 | 2001:db8:acad:10::1 |
| Tegucigalpa, administración | 192.168.20.0/24 | 2001:db8:acad:20::/64 | 2001:db8:acad:20::1 |
| Tegucigalpa, bodega | 192.168.30.0/24 | 2001:db8:acad:30::/64 | 2001:db8:acad:30::1 |
| San Pedro Sula | 192.168.40.0/24 | 2001:db8:acad:40::/64 | 2001:db8:acad:40::1 |
| La Ceiba | 192.168.50.0/24 | 2001:db8:acad:50::/64 | 2001:db8:acad:50::1 |
| Enlace Tegucigalpa y San Pedro Sula | 10.0.0.0/30 | 2001:db8:acad:ff01::/64 | No aplica |

Ojo: `10` en el grupo de subred es hexadecimal, o sea 16 en decimal. No importa, aquí lo usamos como etiqueta, pero no confundás que la subred "10" es la número 16.

### Caso resuelto 5: ¿cuál es la red de esta dirección?

La PC de gerencia tiene `2001:db8:acad:12:a1b2::7/64`. Con /64 la red son los primeros 4 grupos y el resto va en cero: `2001:db8:acad:12::/64`.

Con prefijos que no caen en el borde de un grupo es más trabajo (hay que pasar a binario el grupo partido), por eso en la práctica se usan prefijos múltiplos de 4 bits, que caen en el borde de un dígito hexadecimal.

### Caso resuelto 6: partir una /48 en /52

Si cada sucursal recibe su propia parte: de /48 a /52 son 4 bits, el primer dígito hexadecimal del grupo de subred. Salen 16 bloques: 2001:db8:acad:0000::/52, 2001:db8:acad:1000::/52, 2001:db8:acad:2000::/52, y así hasta f000. Cada bloque tiene 4096 subredes /64. Tegucigalpa podría usar 2001:db8:acad:1000::/52 y San Pedro Sula 2001:db8:acad:2000::/52.

## Cómo obtiene un equipo su dirección

### Dirección de enlace local, siempre

Apenas se activa IPv6 en una interfaz, el equipo se arma una dirección fe80:: por su cuenta y comprueba que nadie más la use (detección de direcciones duplicadas). Con eso ya puede hablar con su router.

### SLAAC

El router manda periódicamente un mensaje "anuncio de router" (Router Advertisement) al grupo de todos los nodos. Ese mensaje dice el prefijo de la red (por ejemplo 2001:db8:acad:10::/64) y que el gateway es la dirección de enlace local del router. El equipo arma su dirección con el prefijo más un identificador de interfaz de 64 bits que genera él mismo. No hace falta servidor. Lo define el RFC 4862.

El identificador de interfaz puede salir de dos formas:

1. EUI 64: a partir de la MAC. Se parte la MAC en dos, se mete `fffe` en medio y se invierte el séptimo bit del primer byte. Para la MAC `00:1a:2b:3c:4d:5e` queda `021a:2bff:fe3c:4d5e`. El problema es que la MAC queda visible en la dirección y se puede rastrear al equipo en cualquier red.
2. Aleatorio: Windows, macOS, Android e iOS generan identificadores al azar por privacidad, y además direcciones temporales que cambian cada cierto tiempo. Por eso en `ipconfig` vas a ver "Dirección IPv6 temporal".

### DHCPv6

Existe y se usa cuando la organización quiere controlar qué dirección recibe cada equipo o entregar otros datos. Hay dos modos: con estado (el servidor asigna la dirección, como DHCP en IPv4) y sin estado (la dirección sale de SLAAC y el servidor solo entrega datos como el DNS). El anuncio del router le dice al equipo cuál usar. Lo define el RFC 8415.

### NDP en lugar de ARP

Para saber la MAC de un vecino, IPv6 usa mensajes ICMPv6 de solicitud y anuncio de vecino, definidos en el RFC 4861. Por eso en IPv6 bloquear todo ICMP en un firewall rompe la red: ICMPv6 no es opcional.

## Convivencia con IPv4

La transición no es un cambio de un día. Lo más común es doble pila: cada equipo y cada router tiene IPv4 e IPv6 a la vez, y usa IPv6 cuando el destino lo tiene. Hay otras técnicas (túneles, traducción NAT64), pero para empezar alcanza con saber que la doble pila es lo normal.

## Configuración en un router Cisco, lo mínimo

```
! En R_TGU, modo de configuración global
ipv6 unicast-routing
interface g0/0
 ipv6 address 2001:db8:acad:10::1/64
 ipv6 address fe80::1 link-local
 no shutdown
```

La primera línea activa el enrutamiento IPv6; sin ella el router no manda anuncios y las PC no se configuran solas. Poner `fe80::1` como enlace local a mano hace que el gateway sea fácil de leer en todas las redes. Para revisar: `show ipv6 interface brief` y `show ipv6 route`.

En Windows, `ipconfig` muestra las direcciones IPv6 y `ping ::1` prueba la pila. Para hacer ping a una enlace local hay que decir por qué interfaz, por ejemplo `ping fe80::1%12`, donde 12 es el número de la interfaz.

## Errores comunes

1. Usar `::` dos veces en una dirección.
2. Quitar ceros de la derecha de un grupo: `ff00` no es `ff`.
3. Olvidar que el grupo de subred está en hexadecimal.
4. Usar prefijos más chicos que /64 en una LAN y después preguntarse por qué SLAAC no funciona.
5. Bloquear todo ICMPv6 "por seguridad".
6. Asustarse porque una interfaz tiene varias direcciones IPv6. Es normal.
7. Creer que IPv6 trae seguridad por sí solo. Un equipo con IPv6 global es alcanzable desde internet si el firewall lo permite; hay que tener reglas también para IPv6.

## Preguntas de repaso

1. ¿Por qué IPv6 usa /64 para las LAN si nunca habrá tantos equipos?
2. Abreviá `2001:0db8:0a00:0000:0000:0000:0000:0001` y expandí `2001:db8::abc:0:1`.
3. ¿Qué reemplaza al broadcast en IPv6? ¿Y a ARP?
4. ¿Qué diferencia hay entre una dirección fe80:: y una 2001:db8::?
5. ¿Cómo arma una PC su dirección con SLAAC? ¿Qué necesita del router?
6. ¿Por qué los sistemas operativos actuales no usan EUI 64 por defecto?
7. Con 2001:db8:acad::/48, ¿cuántas /64 tenés?
8. ¿Qué hace `ipv6 unicast-routing` y qué pasa si se te olvida?

## Practicá con revisión automática

El nivel 7 de [`ejercicios/subneteo.yml`](../ejercicios/subneteo.yml) es de este tema.

## Fuentes

1. [RFC 8200, especificación de IPv6](https://www.rfc-editor.org/rfc/rfc8200) (en)
2. [RFC 4291, arquitectura de direcciones IPv6](https://www.rfc-editor.org/rfc/rfc4291) (en)
3. [RFC 5952, cómo escribir direcciones IPv6 como texto](https://www.rfc-editor.org/rfc/rfc5952) (en)
4. [RFC 3849, prefijo para documentación 2001:db8::/32](https://www.rfc-editor.org/rfc/rfc3849) (en)
5. [RFC 4193, direcciones locales únicas](https://www.rfc-editor.org/rfc/rfc4193) (en)
6. [RFC 4861, descubrimiento de vecinos](https://www.rfc-editor.org/rfc/rfc4861) (en) y [RFC 4862, SLAAC](https://www.rfc-editor.org/rfc/rfc4862) (en)
7. [RFC 8415, DHCPv6](https://www.rfc-editor.org/rfc/rfc8415) (en)
8. [Registro IANA de direcciones IPv6 de propósito especial](https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml) (en)
