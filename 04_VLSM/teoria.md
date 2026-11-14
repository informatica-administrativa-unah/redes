# 04. VLSM y sumarización de rutas

En el caso 6 del tema 03, La Ceiba se quedó sin espacio para una quinta red aunque le sobraban más de 150 direcciones. El problema era la máscara fija: todas las subredes tenían que ser del tamaño de la más grande. VLSM (Variable Length Subnet Masking, máscaras de largo variable) deja que cada subred tenga el tamaño que necesita. Es lo que se usa en cualquier diseño real.

En la segunda parte del tema vas a ver la operación contraria: juntar varias redes en una sola ruta, que es la sumarización. Las dos van juntas porque un buen plan VLSM se diseña para que después se pueda resumir.

## La idea

Con VLSM partís la red en pedazos de distintos tamaños, como cuando cortás una tabla de madera: primero sacás las piezas grandes y con lo que sobra sacás las chicas. Si lo hacés al revés, las piezas chicas quedan en medio y ya no cabe una grande.

Hay dos reglas que hacen que VLSM funcione:

1. Se asigna de la red más grande a la más chica.
2. Cada red tiene que empezar en un múltiplo de su propio tamaño de bloque. Una /26 (bloque 64) solo puede empezar en .0, .64, .128 o .192. Si la asignás en orden de mayor a menor y cada una pegada a la anterior, esto se cumple solo.

## El método en siete pasos

1. Hacé la lista de redes con los hosts que necesita cada una. No te olvidés de los enlaces entre routers (2 hosts cada uno).
2. Ordenala de más hosts a menos.
3. Para cada red, buscá el prefijo más chico que alcanza: el menor h con 2 a la h menos 2 mayor o igual a los hosts, y el prefijo es 32 menos h.
4. Sumá los tamaños de bloque y comprobá que caben en la red disponible. Si no caben, no sigás: hay que pedir más espacio o cambiar el pedido.
5. Asigná la primera red al inicio del espacio disponible.
6. La siguiente empieza en el broadcast de la anterior más 1.
7. Para cada red sacá gateway (primer host), rango y broadcast.

Una tabla de referencia para el paso 3:

| Hosts que necesitás | Prefijo | Bloque |
|---|---|---:|
| 2 | /30 | 4 |
| 3 a 6 | /29 | 8 |
| 7 a 14 | /28 | 16 |
| 15 a 30 | /27 | 32 |
| 31 a 62 | /26 | 64 |
| 63 a 126 | /25 | 128 |
| 127 a 254 | /24 | 256 |
| 255 a 510 | /23 | 512 |
| 511 a 1022 | /22 | 1024 |

## Caso resuelto 1: La Ceiba con VLSM

Misma red del tema 03: 192.168.50.0/24. Ahora piden cinco redes: ventas 40 PC, bodega 20 equipos, cámaras 12, administración 10 y un enlace WAN de 2 hosts.

Paso 1 y 2. Ordenadas: ventas 40, bodega 20, cámaras 12, administración 10, WAN 2.

Paso 3.

| Red | Hosts | Prefijo | Bloque |
|---|---:|---|---:|
| Ventas | 40 | /26 | 64 |
| Bodega | 20 | /27 | 32 |
| Cámaras | 12 | /28 | 16 |
| Administración | 10 | /28 | 16 |
| WAN | 2 | /30 | 4 |

Paso 4. 64 más 32 más 16 más 16 más 4 da 132. Caben en 256.

Pasos 5 a 7.

| Red | Subred | Gateway | Rango para equipos | Broadcast |
|---|---|---|---|---|
| Ventas | 192.168.50.0/26 | .1 | .2 a .62 | .63 |
| Bodega | 192.168.50.64/27 | .65 | .66 a .94 | .95 |
| Cámaras | 192.168.50.96/28 | .97 | .98 a .110 | .111 |
| Administración | 192.168.50.112/28 | .113 | .114 a .126 | .127 |
| WAN | 192.168.50.128/30 | .129 (router de La Ceiba) | .130 (otro extremo) | .131 |

Libre: de 192.168.50.132 a 192.168.50.255. Fijate que el espacio libre no arranca en un múltiplo grande: si mañana piden otra /26, no puede empezar en .132; la primera /26 libre es 192.168.50.192/26. Con máscara fija no cabía ni una quinta red; con VLSM caben las cinco y queda casi la mitad libre.

Comprobá cada red con la regla del múltiplo: .64 es múltiplo de 32, .96 y .112 son múltiplos de 16, .128 es múltiplo de 4. Todo bien.

## Caso resuelto 2: toda la empresa

Comercial El Guayabo quiere ordenar toda su red con 172.16.0.0/21 (2048 direcciones):

1. Tegucigalpa: 300 equipos.
2. San Pedro Sula: 150.
3. La Ceiba: 60.
4. Servidores: 25.
5. Tres enlaces WAN entre las sucursales: 2 hosts cada uno.

Paso 3.

| Red | Hosts | Prefijo | Bloque |
|---|---:|---|---:|
| Tegucigalpa | 300 | /23 | 512 |
| San Pedro Sula | 150 | /24 | 256 |
| La Ceiba | 60 | /26 | 64 |
| Servidores | 25 | /27 | 32 |
| WAN 1, 2 y 3 | 2 cada uno | /30 | 4 cada uno |

Paso 4. 512 más 256 más 64 más 32 más 12 da 876. Caben en 2048.

Aquí los bloques grandes pasan de un octeto a otro, así que conviene llevar la cuenta con cuidado:

1. Tegucigalpa /23 empieza en 172.16.0.0. Bloque de 512 direcciones, o sea 2 en el tercer octeto. Broadcast: 172.16.1.255.
2. San Pedro Sula /24 empieza en 172.16.2.0. Broadcast 172.16.2.255.
3. La Ceiba /26 empieza en 172.16.3.0. Broadcast 172.16.3.63.
4. Servidores /27 empieza en 172.16.3.64. Broadcast 172.16.3.95.
5. WAN 1 /30: 172.16.3.96, broadcast .99.
6. WAN 2 /30: 172.16.3.100, broadcast .103.
7. WAN 3 /30: 172.16.3.104, broadcast .107.

| Red | Subred | Gateway | Último host | Broadcast |
|---|---|---|---|---|
| Tegucigalpa | 172.16.0.0/23 | 172.16.0.1 | 172.16.1.254 | 172.16.1.255 |
| San Pedro Sula | 172.16.2.0/24 | 172.16.2.1 | 172.16.2.254 | 172.16.2.255 |
| La Ceiba | 172.16.3.0/26 | 172.16.3.1 | 172.16.3.62 | 172.16.3.63 |
| Servidores | 172.16.3.64/27 | 172.16.3.65 | 172.16.3.94 | 172.16.3.95 |
| WAN 1 | 172.16.3.96/30 | 172.16.3.97 | 172.16.3.98 | 172.16.3.99 |
| WAN 2 | 172.16.3.100/30 | 172.16.3.101 | 172.16.3.102 | 172.16.3.103 |
| WAN 3 | 172.16.3.104/30 | 172.16.3.105 | 172.16.3.106 | 172.16.3.107 |

Queda libre todo 172.16.4.0/22 (1024 direcciones seguidas) y un pedazo de 172.16.3.108 a 172.16.3.255. Haber puesto lo grande primero dejó un bloque grande libre para una sucursal nueva.

## Caso resuelto 3: cuando no cabe

Piden con 192.168.200.0/24: ventas 100, bodega 70, wifi 60 y administración 30.

| Red | Hosts | Prefijo | Bloque |
|---|---:|---|---:|
| Ventas | 100 | /25 | 128 |
| Bodega | 70 | /25 | 128 |
| Wifi | 60 | /26 | 64 |
| Administración | 30 | /27 | 32 |

Suma: 128 más 128 más 64 más 32, 352. No cabe en 256. Si no hacés esta suma al principio, te das cuenta a la mitad, cuando ya asignaste.

¿Qué se hace? Cuatro opciones, de la que más se usa a la que menos:

1. Pedir más espacio: una /23 tiene 512 y alcanza.
2. Revisar el pedido: ¿bodega necesita de verdad 70 equipos o eran 60? Si bodega baja a 62, cabe en /26, y la suma da 128 más 64 más 64 más 32, 288. Todavía no cabe. Tendría que bajar también el wifi.
3. Partir el wifi a otra red privada, por ejemplo 192.168.201.0/26, porque el wifi de clientes normalmente va aparte de todos modos.
4. Nunca: poner dos departamentos en la misma red sin decirle a nadie.

## Empates y orden

Cuando dos redes piden los mismos hosts, da igual cuál va primero mientras las dos queden pegadas y respeten su múltiplo. Para que los ejercicios del repo tengan una sola respuesta, la regla es: si empatan, va primero la que aparece primero en la lista.

## Sumarización de rutas

VLSM parte; la sumarización junta. Si San Pedro Sula tiene cuatro redes, 192.168.40.0/24, 192.168.41.0/24, 192.168.42.0/24 y 192.168.43.0/24, el router de Tegucigalpa no necesita cuatro rutas hacia allá: le basta una que las cubra a todas. Menos rutas significa tablas más chicas, menos trabajo para los routers y menos errores de configuración.

### Cómo se calcula

1. Escribí en binario el octeto donde las redes cambian.
2. Contá cuántos bits de la izquierda tienen en común todas.
3. El prefijo del resumen es la cantidad de bits iguales en total. La red del resumen son esos bits comunes con todo lo demás en 0.

### Caso resuelto 4: las cuatro redes de San Pedro Sula

Las redes cambian en el tercer octeto: 40, 41, 42 y 43.

```
40 = 001010 00
41 = 001010 01
42 = 001010 10
43 = 001010 11
     |----| iguales: 6 bits
```

Bits iguales: 8 más 8 más 6, 22. Resumen: 192.168.40.0/22.

Comprobación: una /22 tiene bloque 4 en el tercer octeto, y 40 es múltiplo de 4. La /22 va de 192.168.40.0 a 192.168.43.255: cubre exactamente las cuatro y nada más.

### Caso resuelto 5: ocho redes

De 172.16.64.0/24 a 172.16.71.0/24. En el tercer octeto: 64 es `01000 000` y 71 es `01000 111`. Iguales: 5 bits. Resumen: 16 más 5, 172.16.64.0/21. Bloque 8 y 64 es múltiplo de 8. Bien.

### Caso resuelto 6: cuando no resume limpio

10.5.4.0/24, 10.5.5.0/24 y 10.5.6.0/24. En binario 4, 5 y 6 son `000001 00`, `000001 01` y `000001 10`: tienen 6 bits iguales, entonces el resumen sería 10.5.4.0/22. Pero esa /22 también cubre 10.5.7.0/24, que no está en la lista.

Eso se llama sumarizar de más. Si 10.5.7.0/24 existe en otro lado de la red, el tráfico hacia ella se va a ir por el camino equivocado. Tenés dos opciones:

1. Si nadie usa 10.5.7.0/24, el resumen /22 es aceptable y se documenta que esa red queda reservada para ese sitio.
2. Si no estás seguro, usá dos rutas exactas: 10.5.4.0/23 (cubre .4 y .5) y 10.5.6.0/24.

### Por qué VLSM y sumarización se diseñan juntos

En el caso 2 todas las redes de Tegucigalpa quedaron dentro de 172.16.0.0/23. Si después Tegucigalpa crece con más redes y se las das de 172.16.4.0/22, para resumir lo de Tegucigalpa vas a necesitar varias rutas porque quedó partido. Un buen plan deja a cada sitio un bloque contiguo con espacio para crecer, así una sola ruta resumida lo cubre todo.

## Errores comunes

1. Asignar en el orden en que vienen en el enunciado y no de mayor a menor. Una red chica en medio te parte el espacio.
2. Poner una red en una dirección que no es múltiplo de su bloque, por ejemplo una /26 en .32.
3. Olvidarse de los enlaces WAN entre routers.
4. No sumar los bloques al principio para ver si cabe.
5. Elegir el prefijo por los hosts sin contar el gateway. Si te dicen "30 PC" y el gateway es una dirección más, son 31 y ya no cabe en /27. Leé con cuidado si los hosts del enunciado incluyen al router.
6. Sumarizar de más y mandar tráfico de redes que no existen o que están en otro lado.
7. Pensar que el resumen tiene que ser el primer octeto que cambia. Se cuentan bits, no octetos.

## Preguntas de repaso

1. ¿Qué problema de la máscara fija resuelve VLSM?
2. ¿Por qué se asigna de mayor a menor? Mostralo con un ejemplo donde hacerlo al revés deja un hueco.
3. ¿Por qué una /27 no puede empezar en 192.168.1.48?
4. ¿Qué tenés que comprobar antes de empezar a asignar?
5. En el caso 2, ¿dónde pondrías una sucursal nueva de 400 hosts?
6. ¿Qué es sumarizar de más y qué riesgo trae?
7. Calculá el resumen de 192.168.8.0/24 a 192.168.15.0/24.
8. ¿Por qué conviene que cada sitio tenga un bloque contiguo?

## Practicá con revisión automática

Los niveles 5 (VLSM) y 6 (wildcard y sumarización) de [`ejercicios/subneteo.yml`](../ejercicios/subneteo.yml) son de este tema.

## Fuentes

1. [RFC 4632, CIDR y agregación de rutas](https://www.rfc-editor.org/rfc/rfc4632) (en)
2. [RFC 1812, requisitos para routers IPv4](https://www.rfc-editor.org/rfc/rfc1812) (en), sección sobre prefijos de largo variable
3. [Módulo ipaddress de Python](https://docs.python.org/es/3/library/ipaddress.html) (es): `collapse_addresses` calcula resúmenes y sirve para comprobar
