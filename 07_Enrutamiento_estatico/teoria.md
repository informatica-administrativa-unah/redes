# 07. Enrutamiento estático

Con lo que llevamos, cada sucursal de Comercial El Guayabo tiene su red bien partida. Ahora hay que unirlas: que una caja de San Pedro Sula llegue al servidor de Tegucigalpa y que todo el mundo salga a internet. Eso lo hacen los routers, y para hacerlo necesitan saber qué redes existen y por dónde se llega a cada una. Ese conocimiento está en la tabla de enrutamiento.

Hay dos formas de llenar esa tabla: a mano (enrutamiento estático) o dejando que los routers se cuenten entre ellos qué redes conocen (enrutamiento dinámico, con protocolos como OSPF). En este tema vemos el estático a fondo, porque es la base para entender el dinámico y porque en redes chicas, como la de la empresa, es lo más usado.

## La topología de la empresa

```
                         internet
                            |
                     203.0.113.1 (ISP)
                            |
                     203.0.113.2 g0/1
     LAN Tegucigalpa  +-------------+
  192.168.10.0/24 ----|    R_TGU    |
  192.168.20.0/24 ----|  g0/0 (VLAN)|
  192.168.30.0/24 ----|             |
  192.168.99.0/24 ----+-------------+
                 s0/0/0 10.0.0.1    s0/0/1 10.0.0.5
                      |                  |
                 s0/0/0 10.0.0.2    s0/0/0 10.0.0.6
                 +---------+        +---------+
                 |  R_SPS  |        |  R_LCE  |
                 +---------+        +---------+
                 s0/0/1 10.0.0.9 ---- s0/0/1 10.0.0.10   (enlace de respaldo)
                 g0/0 192.168.40.1     g0/0 192.168.50.1
                      |                  |
              LAN San Pedro Sula     LAN La Ceiba
              192.168.40.0/24        192.168.50.0/24
```

Enlaces WAN: Tegucigalpa y San Pedro Sula 10.0.0.0/30, Tegucigalpa y La Ceiba 10.0.0.4/30, San Pedro Sula y La Ceiba 10.0.0.8/30 (respaldo). El enlace a internet es 203.0.113.0/30, de un rango de documentación.

## La tabla de enrutamiento

Cada entrada de la tabla dice: "para llegar a esta red, mandá el paquete a este siguiente salto, o sacalo por esta interfaz". Las entradas pueden venir de tres lados:

1. Redes conectadas directamente: aparecen solas cuando una interfaz tiene IP y está encendida. En Cisco salen con la letra C, y con L la dirección exacta de la interfaz (ruta local /32).
2. Rutas estáticas: las escribe el administrador. Salen con S.
3. Rutas dinámicas: las aprende un protocolo. OSPF sale con O, por ejemplo.

Así se ve la tabla de R_SPS antes de configurar rutas estáticas:

```
C    10.0.0.0/30 is directly connected, Serial0/0/0
L    10.0.0.2/32 is directly connected, Serial0/0/0
C    10.0.0.8/30 is directly connected, Serial0/0/1
L    10.0.0.9/32 is directly connected, Serial0/0/1
C    192.168.40.0/24 is directly connected, GigabitEthernet0/0
L    192.168.40.1/32 is directly connected, GigabitEthernet0/0
```

R_SPS solo conoce las redes que tiene pegadas. Si le llega un paquete para 192.168.20.10 (el servidor de Tegucigalpa), no tiene ninguna entrada que sirva y lo descarta. Por eso hacen falta rutas.

## Cómo decide un router: la coincidencia más larga

Cuando llega un paquete, el router compara la IP de destino con todas las redes de su tabla y se queda con la que coincide en más bits. Eso se llama coincidencia del prefijo más largo.

### Caso resuelto 1: coincidencia más larga

R_TGU tiene en su tabla:

```
S    0.0.0.0/0 [1/0] via 203.0.113.1
S    192.168.40.0/22 [1/0] via 10.0.0.2
S    192.168.42.0/24 [1/0] via 10.0.0.6
```

Llega un paquete para 192.168.42.7. ¿Por dónde sale?

1. 0.0.0.0/0 coincide con cualquier destino (0 bits).
2. 192.168.40.0/22 cubre de 192.168.40.0 a 192.168.43.255: coincide, con 22 bits.
3. 192.168.42.0/24 coincide con 24 bits.

Gana la /24: sale hacia 10.0.0.6. Un paquete para 192.168.41.7 sale por la /22 hacia 10.0.0.2, y uno para 8.8.8.8 por la ruta por defecto.

Esto se cumple siempre, sin importar el orden en que se escribieron las rutas ni su distancia administrativa: primero manda el prefijo más largo.

## La ruta estática

En Cisco, la sintaxis es:

```
ip route RED MÁSCARA SIGUIENTE_SALTO
ip route RED MÁSCARA INTERFAZ_DE_SALIDA
ip route RED MÁSCARA INTERFAZ_DE_SALIDA SIGUIENTE_SALTO
```

Hay tres formas:

1. Con siguiente salto: `ip route 192.168.40.0 255.255.255.0 10.0.0.2`. Es la más común. El router tiene que saber llegar al siguiente salto (10.0.0.2 está en una red conectada, así que sí).
2. Con interfaz de salida: `ip route 192.168.40.0 255.255.255.0 s0/0/0`. Funciona bien en enlaces seriales punto a punto. En Ethernet no conviene, porque el router no sabe a qué MAC mandar y tiene que preguntar por cada destino.
3. Completa, con interfaz y siguiente salto: `ip route 192.168.40.0 255.255.255.0 g0/1 10.0.0.2`. Es la recomendada en enlaces Ethernet.

La ruta solo entra a la tabla si se puede usar: si la interfaz de salida está caída o el siguiente salto no es alcanzable, la ruta desaparece de la tabla hasta que se recupere.

## La ruta por defecto

Es la ruta que se usa cuando ninguna otra coincide: 0.0.0.0 con máscara 0.0.0.0. Es la que manda todo lo desconocido a internet.

```
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

En la tabla se ve como `S*` y aparece la línea "Gateway of last resort is 203.0.113.1".

Las sucursales chicas, que solo tienen una salida, pueden vivir con una sola ruta por defecto hacia Tegucigalpa. Eso se llama red de punta (stub): todo lo que no es local sale por el único camino.

## Caso resuelto 2: configurar toda la empresa

Hay que pensar en las dos direcciones. Si R_SPS sabe llegar a Tegucigalpa pero R_TGU no sabe volver a San Pedro Sula, el ping sale y la respuesta se pierde. Es el error más común.

### R_TGU

Conoce directamente sus cuatro VLANs, los dos enlaces y el enlace a internet. Le faltan las LAN de las sucursales y la salida a internet:

```
ip route 192.168.40.0 255.255.255.0 10.0.0.2
ip route 192.168.50.0 255.255.255.0 10.0.0.6
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

### R_SPS

Es una sucursal con una salida principal. Con una ruta por defecto hacia Tegucigalpa alcanza para llegar a todo, incluido internet y La Ceiba (Tegucigalpa sabe llegar a La Ceiba):

```
ip route 0.0.0.0 0.0.0.0 10.0.0.1
```

### R_LCE

Igual:

```
ip route 0.0.0.0 0.0.0.0 10.0.0.5
```

### Comprobación del camino de ida y vuelta

Ping de una caja de La Ceiba (192.168.50.30) al servidor 192.168.20.10:

1. La PC lo manda a su gateway, R_LCE.
2. R_LCE no tiene la red 192.168.20.0 pero tiene ruta por defecto: lo manda a 10.0.0.5, R_TGU.
3. R_TGU tiene 192.168.20.0/24 conectada en su subinterfaz de la VLAN 20 y se lo entrega al servidor.
4. La respuesta va a 192.168.50.30. R_TGU tiene la ruta 192.168.50.0/24 via 10.0.0.6 y la manda a R_LCE.
5. R_LCE tiene 192.168.50.0/24 conectada y se la entrega a la PC.

Si se te olvida la ruta del paso 4 en R_TGU, el ping de La Ceiba al servidor falla aunque el camino de ida esté perfecto: R_TGU mandaría la respuesta a internet por la ruta por defecto.

## Distancia administrativa y rutas flotantes

Si un router conoce la misma red por dos lados distintos, con el mismo prefijo, elige según la distancia administrativa (AD): un número que dice qué tan confiable es el origen de la ruta. Menor es mejor.

| Origen | AD |
|---|---:|
| Conectada | 0 |
| Estática | 1 |
| EIGRP | 90 |
| OSPF | 110 |
| RIP | 120 |

Una ruta estática flotante es una ruta de respaldo a la que se le pone una AD más alta a propósito. Mientras la principal funcione, la flotante no entra a la tabla. Si la principal se cae, la flotante "sale a flote".

### Caso resuelto 3: respaldo de La Ceiba por San Pedro Sula

Si el enlace entre Tegucigalpa y La Ceiba se cae, La Ceiba queda aislada aunque exista el enlace de respaldo hacia San Pedro Sula. Con rutas flotantes:

En R_LCE, una segunda ruta por defecto por San Pedro Sula, con AD 10:

```
ip route 0.0.0.0 0.0.0.0 10.0.0.5
ip route 0.0.0.0 0.0.0.0 10.0.0.9 10
```

En R_TGU, el camino de vuelta a La Ceiba por San Pedro Sula, con AD 10:

```
ip route 192.168.50.0 255.255.255.0 10.0.0.6
ip route 192.168.50.0 255.255.255.0 10.0.0.2 10
```

Y R_SPS tiene que saber llegar a La Ceiba por el enlace directo, si no el tráfico de respaldo se queda dando vueltas:

```
ip route 192.168.50.0 255.255.255.0 10.0.0.10
```

Cuando el enlace s0/0/1 de R_TGU se cae, la ruta con AD 1 desaparece (su siguiente salto ya no es alcanzable) y la de AD 10 entra a la tabla. Se puede probar en Packet Tracer apagando la interfaz con `shutdown`.

Un detalle importante: en enlaces Ethernet con un switch o un equipo del proveedor en medio, la interfaz puede seguir encendida aunque el otro router esté caído, y la ruta principal no desaparece. En la vida real eso se resuelve con un seguimiento del enlace (IP SLA en Cisco) o con un protocolo dinámico. En los enlaces seriales de Packet Tracer el ejemplo funciona tal cual.

## Rutas resumidas

Si en el futuro San Pedro Sula usa 192.168.40.0/24 a 192.168.43.0/24, en R_TGU no hacen falta cuatro rutas. Con lo que viste en el tema 04:

```
ip route 192.168.40.0 255.255.252.0 10.0.0.2
```

## Rutas estáticas en IPv6

La idea es la misma, con la sintaxis de IPv6:

```
ipv6 unicast-routing
ipv6 route 2001:db8:acad:40::/64 2001:db8:acad:ff01::2
ipv6 route ::/0 2001:db8:acad:ff01::1
```

`::/0` es la ruta por defecto en IPv6. Si el siguiente salto es una dirección fe80::, hay que poner también la interfaz, porque la misma enlace local puede existir en varias interfaces.

## Verificación y diagnóstico

| Comando | Qué te dice |
|---|---|
| `show ip route` | La tabla completa. Buscá que exista una entrada para el destino |
| `show ip route static` | Solo las estáticas |
| `show ip route 192.168.50.30` | Qué entrada usaría el router para esa IP concreta |
| `show ip interface brief` | Si las interfaces están up y con la IP correcta |
| `ping` y `traceroute` desde el router | Si llega y por dónde pasa |

Orden para diagnosticar "no hay comunicación entre A y B":

1. ¿A llega a su gateway? Si no, el problema está en la LAN de A (temas 02 y 06).
2. ¿El router de A tiene ruta hacia la red de B? `show ip route`.
3. ¿El siguiente salto está encendido y alcanzable?
4. ¿El router de B tiene ruta de vuelta hacia la red de A? Este es el que más se olvida.
5. ¿B tiene bien su gateway?
6. `traceroute` desde A: el último salto que responde te dice dónde se corta.

## Estático o dinámico

| | Estático | Dinámico (OSPF, por ejemplo) |
|---|---|---|
| Configuración | A mano, ruta por ruta | Se activa el protocolo y los routers se cuentan las redes |
| Si cambia la red | Hay que tocar cada router | Se ajusta solo |
| Si se cae un enlace | Solo se recupera con rutas flotantes | Busca otro camino solo |
| Consumo | Nada de CPU ni de ancho de banda | Algo de los dos |
| Seguridad y control | Total: el router solo sabe lo que le dijiste | Hay que proteger el protocolo |
| Conviene en | Redes chicas, sucursales de punta, salida a internet | Redes medianas y grandes con varios caminos |

Muchas redes usan las dos: dinámico entre los routers internos y una ruta estática por defecto hacia internet.

## Errores comunes

1. Configurar la ida y olvidar la vuelta.
2. Poner como siguiente salto la IP del propio router en vez de la del vecino.
3. Escribir la red con bits de host, como `ip route 192.168.40.1 255.255.255.0 ...`. Cisco lo rechaza; tiene que ser la dirección de red.
4. Usar interfaz de salida sola en un enlace Ethernet.
5. Poner una ruta flotante con AD menor que la principal: entonces la principal es la flotante.
6. Creer que la AD gana sobre el prefijo más largo. Primero se elige el prefijo más largo; la AD solo desempata entre rutas a la misma red con el mismo prefijo.
7. Sumarizar de más y mandar a una sucursal tráfico de redes que no son suyas.
8. No guardar la configuración con `copy running-config startup-config`.

## Preguntas de repaso

1. ¿Qué tres orígenes puede tener una entrada en la tabla de enrutamiento?
2. Explicá la coincidencia del prefijo más largo con un ejemplo propio.
3. ¿Qué diferencia hay entre una ruta con siguiente salto y una con interfaz de salida? ¿Cuál conviene en Ethernet?
4. ¿Para qué sirve la ruta por defecto? ¿Cómo se ve en la tabla?
5. ¿Qué es la distancia administrativa? ¿Cuándo se usa?
6. ¿Cómo funciona una ruta estática flotante y en qué caso no se activa sola?
7. ¿Por qué una sucursal de punta puede vivir con una sola ruta?
8. Un ping de A a B falla pero `traceroute` muestra que llega al router de B. ¿Qué revisás?

## Fuentes

1. [RFC 1812, requisitos para routers IPv4](https://www.rfc-editor.org/rfc/rfc1812) (en), la sección 5.2.4.3 explica la coincidencia más larga
2. [RFC 4632, CIDR](https://www.rfc-editor.org/rfc/rfc4632) (en)
3. [Networking Basics de Cisco NetAcad](https://www.netacad.com/courses/networking-basics) (en)
