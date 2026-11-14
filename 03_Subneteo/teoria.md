# 03. Subneteo

Subnetear es partir una red grande en redes más chicas. Es el tema que más pesa en los exámenes de redes y el que más se usa en el trabajo cuando hay que ordenar una red que creció sin plan. Este capítulo es largo a propósito: trae el porqué, el método, seis casos resueltos completos y los errores que más se repiten. Necesitás tener firme el tema 02, sobre todo la tabla de máscaras y el tamaño de bloque.

## Por qué partir una red

Imaginá que Comercial El Guayabo pone todas las PC, impresoras, cámaras y servidores de Tegucigalpa en una sola red 192.168.10.0/24. Funciona, pero tiene tres problemas:

1. Broadcast. Cada ARP, cada pedido de DHCP y muchos anuncios de impresoras llegan a todos los equipos de la red. Con 200 equipos eso se nota. Partir la red parte los dominios de broadcast.
2. Seguridad. Si la PC de una cajera está en la misma red que el servidor de planilla, nada en medio controla el tráfico entre ellas. Cuando están en redes distintas, el tráfico pasa por un router o firewall donde se pueden poner reglas.
3. Orden. Si sabés que 192.168.30.0 es la bodega, un problema en esa red te dice de una vez dónde buscar. Y podés crecer una red sin desordenar las demás.

El costo de partir es que en cada subred pierdes dos direcciones (red y broadcast) y que necesitás un router o un switch de capa 3 para que las subredes se hablen.

## La idea: pedir bits prestados

Una red /24 tiene 8 bits de host. Si le tomamos prestados 3 de esos bits para la parte de red, el prefijo pasa a /27 y quedan 5 bits de host.

```
Red original /24:   RRRRRRRR.RRRRRRRR.RRRRRRRR.HHHHHHHH
Subredes /27:       RRRRRRRR.RRRRRRRR.RRRRRRRR.SSSHHHHH
                                               |  |
                       3 bits de subred -------+  +--- 5 bits de host
```

Con 3 bits de subred hay 2 elevado a la 3, 8 combinaciones: 8 subredes. Con 5 bits de host hay 2 elevado a la 5, 32 direcciones por subred, de las que 30 son útiles.

Todo el subneteo sale de dos fórmulas:

1. Subredes que se forman: 2 elevado a s, donde s son los bits prestados.
2. Hosts útiles por subred: 2 elevado a h, menos 2, donde h son los bits que quedan de host.

Y de una regla: los bits que prestás para subredes se los quitás a los hosts. Más subredes significa subredes más chicas.

### Tabla de potencias de 2

Tenela a mano hasta que te la sepás:

| n | 2 a la n | n | 2 a la n |
|---:|---:|---:|---:|
| 1 | 2 | 9 | 512 |
| 2 | 4 | 10 | 1024 |
| 3 | 8 | 11 | 2048 |
| 4 | 16 | 12 | 4096 |
| 5 | 32 | 13 | 8192 |
| 6 | 64 | 14 | 16 384 |
| 7 | 128 | 15 | 32 768 |
| 8 | 256 | 16 | 65 536 |

## El método en seis pasos

Siempre el mismo, para cualquier caso:

1. Leé qué te piden: una cantidad de subredes, o una cantidad de hosts por subred.
2. Sacá los bits. Si piden subredes, buscá el menor s con 2 a la s mayor o igual a lo pedido. Si piden hosts, buscá el menor h con 2 a la h menos 2 mayor o igual a lo pedido.
3. Calculá el prefijo nuevo y la máscara: prefijo original más s, o 32 menos h.
4. Ubicá el octeto interesante (el primero de la máscara que no es 255) y el tamaño de bloque (256 menos el valor de la máscara en ese octeto).
5. Listá las subredes sumando el bloque en el octeto interesante, empezando desde la red original.
6. Para cada subred sacá primer host, último host y broadcast. El broadcast es la subred siguiente menos 1.

Siempre comprobá al final: la última subred tiene que terminar justo en el broadcast de la red original. Si no, hay un error en el bloque.

## Caso resuelto 1: subredes por cantidad, red de clase C

Comercial El Guayabo tiene 192.168.60.0/24 para un edificio nuevo en Tegucigalpa y quiere 5 subredes: ventas, administración, bodega, gerencia y cámaras.

Paso 1. Piden 5 subredes.

Paso 2. ¿2 a la 2? Da 4, no alcanza. ¿2 a la 3? Da 8, alcanza. s = 3.

Paso 3. Prefijo nuevo: 24 más 3, /27. Máscara 255.255.255.224. Bits de host: 5, hosts útiles: 30.

Paso 4. Octeto interesante: el cuarto. Bloque: 256 menos 224, 32.

Paso 5 y 6.

| N.° | Subred | Primer host | Último host | Broadcast |
|---:|---|---|---|---|
| 1 | 192.168.60.0/27 | .1 | .30 | .31 |
| 2 | 192.168.60.32/27 | .33 | .62 | .63 |
| 3 | 192.168.60.64/27 | .65 | .94 | .95 |
| 4 | 192.168.60.96/27 | .97 | .126 | .127 |
| 5 | 192.168.60.128/27 | .129 | .158 | .159 |
| 6 | 192.168.60.160/27 | .161 | .190 | .191 |
| 7 | 192.168.60.192/27 | .193 | .222 | .223 |
| 8 | 192.168.60.224/27 | .225 | .254 | .255 |

Comprobación: la última termina en .255, el broadcast de la /24. Bien.

Se usan 5 y quedan 3 libres para crecer. Antes de entregar el diseño, preguntate: ¿30 hosts le alcanzan a ventas? Si ventas tiene 45 PC, este diseño no sirve y hay que ir a VLSM (tema 04).

## Caso resuelto 2: subredes por cantidad de hosts

En la bodega de Tegucigalpa quieren redes chicas para separar lectores de código de barras, cámaras, impresoras y PC. Cada red necesita como mucho 14 equipos. La red disponible es 192.168.70.0/24.

Paso 1. Piden 14 hosts por subred.

Paso 2. ¿2 a la 3 menos 2? Da 6, no alcanza. ¿2 a la 4 menos 2? Da 14, alcanza justo. h = 4.

Paso 3. Prefijo: 32 menos 4, /28. Máscara 255.255.255.240. Subredes: los bits prestados son 28 menos 24, 4, así que 16 subredes.

Paso 4. Bloque: 256 menos 240, 16.

Primeras subredes:

| N.° | Subred | Primer host | Último host | Broadcast |
|---:|---|---|---|---|
| 1 | 192.168.70.0/28 | .1 | .14 | .15 |
| 2 | 192.168.70.16/28 | .17 | .30 | .31 |
| 3 | 192.168.70.32/28 | .33 | .46 | .47 |
| 4 | 192.168.70.48/28 | .49 | .62 | .63 |
| ... | | | | |
| 16 | 192.168.70.240/28 | .241 | .254 | .255 |

Ojo: si mañana compran un lector más y una red pasa a 15 equipos, /28 ya no alcanza. Cuando el número pedido cae justo en el límite, conviene preguntar cuánto van a crecer. En el trabajo casi siempre se deja margen.

## Caso resuelto 3: red de clase B, el bloque está en el tercer octeto

La empresa decide usar 172.20.0.0/16 para toda la red interna y quiere 100 subredes iguales, pensando en abrir más sucursales.

Paso 2. ¿2 a la 6? 64, no alcanza. ¿2 a la 7? 128, alcanza. s = 7.

Paso 3. Prefijo: 16 más 7, /23. Máscara 255.255.254.0. Bits de host: 9. Hosts útiles: 512 menos 2, 510.

Paso 4. Octeto interesante: el tercero (254). Bloque: 2. Las subredes avanzan de 2 en 2 en el tercer octeto.

| N.° | Subred | Primer host | Último host | Broadcast |
|---:|---|---|---|---|
| 1 | 172.20.0.0/23 | 172.20.0.1 | 172.20.1.254 | 172.20.1.255 |
| 2 | 172.20.2.0/23 | 172.20.2.1 | 172.20.3.254 | 172.20.3.255 |
| 3 | 172.20.4.0/23 | 172.20.4.1 | 172.20.5.254 | 172.20.5.255 |
| ... | | | | |
| 128 | 172.20.254.0/23 | 172.20.254.1 | 172.20.255.254 | 172.20.255.255 |

¿Cuál es la subred número 20? No hace falta escribir las 20. La subred n empieza en (n menos 1) por el bloque: 19 por 2, 38. Subred 20: 172.20.38.0/23, broadcast 172.20.39.255.

Fijate que en una /23 el host 172.20.38.255 es válido, porque el broadcast está en el .39.

## Caso resuelto 4: los bits prestados cruzan de octeto

Un caso de examen clásico: 10.0.0.0/8 se tiene que dividir en al menos 2000 subredes.

Paso 2. 2 a la 10 es 1024, no alcanza. 2 a la 11 es 2048, alcanza. s = 11.

Paso 3. Prefijo: 8 más 11, /19. Máscara 255.255.224.0. Bits de host: 13. Hosts útiles: 8192 menos 2, 8190.

Paso 4. Octeto interesante: el tercero (224). Bloque: 32. Pero los bits de subred empiezan en el segundo octeto, así que cuando el tercer octeto llega a 256 se suma 1 al segundo:

| N.° | Subred |
|---:|---|
| 1 | 10.0.0.0/19 |
| 2 | 10.0.32.0/19 |
| 3 | 10.0.64.0/19 |
| ... | |
| 8 | 10.0.224.0/19 |
| 9 | 10.1.0.0/19 |
| 10 | 10.1.32.0/19 |

Por cada valor del segundo octeto caben 256 entre 32, 8 subredes. ¿La subred 100? Restá 1: 99. Dividí entre 8: da 12 y sobran 3. El segundo octeto es 12 y el tercero es 3 por 32, 96. Subred 100: 10.12.96.0/19, broadcast 10.12.127.255.

## Caso resuelto 5: el camino al revés, ¿a qué subred pertenece?

Con el diseño del caso 3 (172.20.0.0/16 partido en /23), un técnico encuentra la IP 172.20.77.130 en un log. ¿De qué subred es y cuál sería su gateway?

1. Octeto interesante: el tercero, bloque 2.
2. El múltiplo de 2 más grande que no se pasa de 77 es 76.
3. Subred: 172.20.76.0/23. Broadcast: 172.20.77.255.
4. Gateway según la regla del curso: primer host, 172.20.76.1.
5. Número de subred: 76 entre 2, 38, más 1: es la subred 39.

## Caso resuelto 6: diseño completo para una sucursal

La Ceiba va a crecer y le asignan 192.168.50.0/24. Necesitan:

1. Ventas: 40 PC.
2. Bodega: 20 equipos.
3. Administración: 10 PC.
4. Una red para cámaras: 12 cámaras.

Con subneteo de máscara fija todas las subredes son del mismo tamaño, así que manda la más grande: 40 hosts.

Paso 2. 2 a la 6 menos 2 es 62, alcanza para 40. h = 6.

Paso 3. /26, máscara 255.255.255.192, bloque 64. Subredes: 4.

| Red | Subred | Gateway | Rango de hosts | Broadcast | Sobran |
|---|---|---|---|---|---:|
| Ventas | 192.168.50.0/26 | .1 | .2 a .62 | .63 | 21 |
| Bodega | 192.168.50.64/26 | .65 | .66 a .126 | .127 | 41 |
| Administración | 192.168.50.128/26 | .129 | .130 a .190 | .191 | 51 |
| Cámaras | 192.168.50.192/26 | .193 | .194 a .254 | .255 | 49 |

"Sobran" cuenta los hosts libres después de quitar el gateway. Funciona, pero se ve el problema: se usaron las 4 subredes y no queda espacio para una quinta red, aunque sobran más de 150 direcciones repartidas. Eso es lo que resuelve VLSM en el tema 04.

## La máscara wildcard

Algunos comandos de Cisco (las listas de acceso y OSPF) no usan la máscara sino su inverso, la wildcard. Se saca restando cada octeto de la máscara a 255.

| Máscara | Wildcard |
|---|---|
| 255.255.255.0 | 0.0.0.255 |
| 255.255.255.192 | 0.0.0.63 |
| 255.255.240.0 | 0.0.15.255 |

En la wildcard, un 0 significa "este bit tiene que coincidir" y un 1 "este bit no importa". La vas a usar en el tema 09 para decir qué redes salen a internet con NAT.

## Subred cero y la subred de todos unos

En libros viejos vas a leer que la primera subred (la de los bits de subred en 0) y la última (todos en 1) no se usan, y que entonces una /24 partida en /27 da 6 subredes y no 8. Esa regla venía del RFC 950 y de equipos antiguos. Hoy todos los equipos y CIDR usan las dos, y Cisco las permite por defecto desde hace muchos años. En este curso contamos todas. Si en un examen te piden lo contrario, el enunciado lo va a decir; si no lo dice, preguntá.

## Errores comunes

1. Usar la fórmula de hosts sin restar 2. Para 30 hosts, /27 da justo 30; si te piden 31, ya no alcanza y es /26.
2. Confundir bits prestados con bits de host. Prestar más bits da más subredes y menos hosts, no al revés.
3. Sumar el bloque en el octeto equivocado. El bloque se suma en el octeto interesante, el primero donde la máscara no es 255.
4. Olvidar que en /23, /22 o más grandes el broadcast no termina en el mismo tercer octeto donde empieza la red.
5. Numerar la primera subred como cero en una respuesta que pide "la tercera subred". Aclará siempre si contás desde 0 o desde 1; en este curso contamos desde 1.
6. No comprobar el final. Si la última subred no termina justo en el broadcast original, algo está mal.
7. Diseñar justo al límite sin preguntar por el crecimiento.
8. Querer subnetear con máscara fija cuando las redes tienen tamaños muy distintos. Ahí corresponde VLSM.

## Preguntas de repaso

1. ¿Qué tres problemas resuelve partir una red? ¿Cuál es el costo?
2. ¿Qué relación hay entre los bits prestados, la cantidad de subredes y los hosts por subred?
3. Explicá con un ejemplo cómo encontrar la subred número n sin escribirlas todas.
4. ¿Por qué en el caso 6 se eligió /26 si administración solo necesitaba 10 hosts?
5. Si una red /22 se parte en /26, ¿cuántas subredes salen? ¿Por qué?
6. ¿Qué es la wildcard y en qué se diferencia de la máscara?
7. ¿Por qué hoy se usan la subred cero y la de todos unos?
8. Un compañero dice que 172.20.38.255/23 no se puede usar porque termina en 255. ¿Tiene razón?

## Practicá con revisión automática

En [`ejercicios/subneteo.yml`](../ejercicios/subneteo.yml) están los ejercicios de los niveles 1 a 4 de este tema. Llenás las respuestas y corrés `python herramientas/revisar.py`. El README explica cómo.

## Fuentes

1. [RFC 950, procedimiento de subneteo en internet](https://www.rfc-editor.org/rfc/rfc950) (en), el documento que definió las subredes en 1985
2. [RFC 4632, CIDR](https://www.rfc-editor.org/rfc/rfc4632) (en)
3. [Módulo ipaddress de Python](https://docs.python.org/es/3/library/ipaddress.html) (es): `subnets(new_prefix=27)` te lista las subredes para comprobar tus tablas
