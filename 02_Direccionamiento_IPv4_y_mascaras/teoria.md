# 02. Direccionamiento IPv4 y máscaras

Todo lo que viene después en el curso (subneteo, VLSM, enrutamiento, NAT) depende de que entendás bien este tema. Si algo de aquí te queda flojo, el subneteo se vuelve memorizar trucos sin entender, y en el primer caso raro te perdés. Tomate el tiempo, hacé las conversiones a mano y no pasés al tema 03 hasta que el ejercicio 6 te salga sin ver la solución.

## Qué es una dirección IPv4

Una dirección IPv4 es un número de 32 bits. Para que las personas lo podamos leer, se parte en cuatro grupos de 8 bits (octetos) y cada octeto se escribe en decimal, separado por puntos. A eso se le llama notación decimal con puntos.

```
Binario:  11000000 10101000 00001010 00100101
Decimal:     192      168       10       37      ->  192.168.10.37
```

Cada octeto tiene 8 bits, así que va de 0 (00000000) a 255 (11111111). Una dirección como 192.168.300.1 no existe.

Con 32 bits hay 2 elevado a la 32 combinaciones, unas 4 294 967 296 direcciones. Parecen muchas, pero no alcanzan para todos los equipos del mundo; por eso existen las direcciones privadas, NAT (tema 09) e IPv6 (tema 05).

## Binario a decimal y decimal a binario

No hay forma de evitarlo: para subnetear con seguridad tenés que convertir rápido. Cada posición de un octeto tiene un valor:

| Posición | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Valor | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

### Binario a decimal

Sumás los valores de las posiciones que tienen 1.

`10101000` = 128 + 32 + 8 = 168.

### Decimal a binario, por restas

Para 200: ¿cabe 128? Sí, queda 72, pongo 1. ¿Cabe 64 en 72? Sí, queda 8, pongo 1. ¿32 en 8? No, 0. ¿16 en 8? No, 0. ¿8 en 8? Sí, queda 0, pongo 1. Lo demás va en 0.

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

200 = `11001000`.

### Los valores que más vas a usar

Las máscaras solo usan unos pocos valores por octeto, porque los bits en 1 siempre van seguidos desde la izquierda. Aprendételos:

| Bits en 1 | Binario | Decimal |
|---:|---|---:|
| 0 | 00000000 | 0 |
| 1 | 10000000 | 128 |
| 2 | 11000000 | 192 |
| 3 | 11100000 | 224 |
| 4 | 11110000 | 240 |
| 5 | 11111000 | 248 |
| 6 | 11111100 | 252 |
| 7 | 11111110 | 254 |
| 8 | 11111111 | 255 |

## Red y host: las dos partes de una dirección

Una dirección IPv4 tiene dos partes:

1. La parte de red, que dice a qué red pertenece el equipo. Todos los equipos de la misma red la tienen igual.
2. La parte de host, que identifica al equipo dentro de esa red.

Es como una dirección postal: "Colonia Palmira, casa 37". La colonia es la red y el número es el host. El cartero (el router) solo necesita saber la colonia para llevar la carta a la zona correcta.

¿Cómo sabe un equipo dónde termina la red y empieza el host? Con la máscara.

## La máscara de subred

La máscara es otro número de 32 bits. Donde tiene 1, esa parte de la dirección es red. Donde tiene 0, es host. Los 1 siempre van primero y todos juntos.

```
Dirección: 11000000 10101000 00001010 00100101   192.168.10.37
Máscara:   11111111 11111111 11111111 00000000   255.255.255.0
           |------------ red -----------| host |
```

### Notación de prefijo (CIDR)

Escribir la máscara completa es largo, así que se usa la cantidad de bits en 1 después de una barra: 255.255.255.0 tiene 24 bits en 1, entonces se escribe /24. La dirección completa queda 192.168.10.37/24.

| Prefijo | Máscara | Bits de host | Direcciones | Hosts útiles |
|---|---|---:|---:|---:|
| /8 | 255.0.0.0 | 24 | 16 777 216 | 16 777 214 |
| /16 | 255.255.0.0 | 16 | 65 536 | 65 534 |
| /20 | 255.255.240.0 | 12 | 4096 | 4094 |
| /22 | 255.255.252.0 | 10 | 1024 | 1022 |
| /23 | 255.255.254.0 | 9 | 512 | 510 |
| /24 | 255.255.255.0 | 8 | 256 | 254 |
| /25 | 255.255.255.128 | 7 | 128 | 126 |
| /26 | 255.255.255.192 | 6 | 64 | 62 |
| /27 | 255.255.255.224 | 5 | 32 | 30 |
| /28 | 255.255.255.240 | 4 | 16 | 14 |
| /29 | 255.255.255.248 | 3 | 8 | 6 |
| /30 | 255.255.255.252 | 2 | 4 | 2 |

## Tres direcciones especiales en cada red

En cada red hay tres direcciones que tenés que saber sacar:

1. Dirección de red: todos los bits de host en 0. Identifica a la red y no se le puede poner a un equipo.
2. Broadcast: todos los bits de host en 1. Lo que se manda ahí le llega a todos los equipos de la red. Tampoco se le pone a un equipo.
3. Las de en medio son los hosts útiles. La primera es la red más 1 y la última el broadcast menos 1.

Por eso los hosts útiles son 2 elevado a los bits de host, menos 2. Con 8 bits de host: 256 menos 2, 254.

La excepción son los enlaces /31 entre dos routers, donde no se reservan red ni broadcast (RFC 3021). En este curso, igual que en la mayoría de exámenes, usamos /30 para los enlaces punto a punto, salvo que se diga otra cosa.

## Cómo sacar la red: la operación AND

El equipo saca la dirección de red haciendo un AND bit a bit entre su IP y su máscara: 1 y 1 da 1; cualquier otra combinación da 0. En la práctica significa "copiá los bits de la IP donde la máscara tiene 1, y poné 0 en el resto".

### Caso resuelto 1: 192.168.10.37/24

La máscara es 255.255.255.0. Los tres primeros octetos son todo red y el último todo host.

1. Red: copiás 192.168.10 y ponés el host en 0: 192.168.10.0.
2. Broadcast: host en 1, o sea 255: 192.168.10.255.
3. Primer host: 192.168.10.1. Último host: 192.168.10.254.
4. Hosts útiles: 2 a la 8, menos 2: 254.

### Caso resuelto 2: 172.16.45.200/16

Máscara 255.255.0.0. Red: 172.16.0.0. Broadcast: 172.16.255.255. Primer host: 172.16.0.1. Último: 172.16.255.254. Hosts: 2 a la 16, menos 2: 65 534.

Ojo con 172.16.0.255 y 172.16.1.0: en una /16 los dos son hosts válidos, porque el host son los dos últimos octetos juntos.

### Caso resuelto 3: 192.168.20.77/26, la máscara corta un octeto

Aquí la máscara es 255.255.255.192: el último octeto tiene 2 bits de red y 6 de host. Hacemos el AND solo en ese octeto, que es el interesante:

```
77  = 0100 1101
192 = 1100 0000
AND = 0100 0000 = 64
```

Red: 192.168.20.64. Para el broadcast ponemos los 6 bits de host en 1: `01 111111` = 64 + 63 = 127. Broadcast: 192.168.20.127. Primer host .65, último .126, 62 hosts útiles.

### El atajo del tamaño de bloque

Hacer AND en binario siempre funciona, pero hay un atajo que da lo mismo y es más rápido.

1. Buscá el octeto interesante: el primero donde la máscara no es 255.
2. Tamaño de bloque = 256 menos el valor de la máscara en ese octeto.
3. Las redes empiezan en múltiplos del tamaño de bloque: 0, bloque, 2 bloques, y así.
4. La red es el múltiplo más grande que no se pasa del valor de la IP en ese octeto.
5. El broadcast es la red siguiente menos 1.

Para 192.168.20.77/26: el octeto interesante es el cuarto, la máscara vale 192 ahí, el bloque es 256 menos 192, 64. Los múltiplos son 0, 64, 128, 192. El 77 cae entre 64 y 128, así que la red es .64 y el broadcast es .127. Igual que con el AND.

### Caso resuelto 4: 172.20.13.71/21, el octeto interesante es el tercero

/21 es 255.255.248.0. El octeto interesante es el tercero (248). Bloque: 256 menos 248, 8. Múltiplos de 8 en el tercer octeto: 0, 8, 16. El 13 cae entre 8 y 16.

1. Red: 172.20.8.0. El cuarto octeto, que es todo host, va en 0.
2. Broadcast: la red siguiente es 172.20.16.0, menos una dirección: 172.20.15.255.
3. Primer host: 172.20.8.1. Último: 172.20.15.254.
4. Bits de host: 32 menos 21, 11. Hosts útiles: 2048 menos 2, 2046.

Fijate que en esta red 172.20.9.0, 172.20.10.255 y 172.20.12.0 son hosts válidos. Una dirección que termina en 0 o en 255 no siempre es red o broadcast: depende de la máscara.

## Clases de direcciones: lo que todavía te van a preguntar

Antes de 1993 las direcciones se repartían por clases según el primer octeto. Hoy ya no se usan para asignar redes (se usa CIDR, RFC 4632), pero el vocabulario sigue en libros, exámenes y en la configuración de algunos equipos.

| Clase | Primer octeto | Máscara por defecto | Uso |
|---|---|---|---|
| A | 1 a 126 | /8 | Redes muy grandes |
| B | 128 a 191 | /16 | Redes medianas |
| C | 192 a 223 | /24 | Redes chicas |
| D | 224 a 239 | No tiene | Multicast |
| E | 240 a 255 | No tiene | Experimental |

El 127 no entra en la clase A porque está reservado para loopback.

## Direcciones privadas y especiales

El RFC 1918 reservó tres rangos para usar dentro de las organizaciones. No se enrutan en internet, así que cualquier empresa los puede repetir. Para salir a internet se traducen con NAT.

| Rango privado | Prefijo | Tamaño |
|---|---|---|
| 10.0.0.0 a 10.255.255.255 | 10.0.0.0/8 | Una red de clase A |
| 172.16.0.0 a 172.31.255.255 | 172.16.0.0/12 | 16 redes de clase B |
| 192.168.0.0 a 192.168.255.255 | 192.168.0.0/16 | 256 redes de clase C |

Un error frecuente: 172.32.0.1 no es privada. El rango 172 privado llega solo hasta 172.31.

Otras direcciones especiales que tenés que reconocer al verlas:

| Dirección | Para qué es |
|---|---|
| 127.0.0.0/8 (normalmente 127.0.0.1) | Loopback: el equipo hablando consigo mismo. Si `ping 127.0.0.1` falla, el problema es la pila TCP/IP de la PC |
| 169.254.0.0/16 | Enlace local, o APIPA en Windows. La PC se la pone sola cuando no le contestó ningún servidor DHCP |
| 0.0.0.0 | "Esta red" o "cualquier dirección". En una tabla de rutas, 0.0.0.0/0 es la ruta por defecto |
| 255.255.255.255 | Broadcast limitado, a toda la red local. DHCP la usa |
| 100.64.0.0/10 | Espacio compartido para NAT de proveedores (RFC 6598). Si tu router de casa recibe una IP de aquí, tu proveedor te tiene detrás de otro NAT |
| 192.0.2.0/24, 198.51.100.0/24 y 203.0.113.0/24 | Reservadas para documentación y ejemplos (RFC 5737). En este curso las usamos como "direcciones públicas" inventadas |

La IANA mantiene el registro completo de direcciones IPv4 de propósito especial.

## Unicast, broadcast y multicast

1. Unicast: de un equipo a otro. Casi todo el tráfico.
2. Broadcast: de un equipo a todos los de su red. ARP y DHCP lo usan. Los routers no lo reenvían a otras redes, y por eso cada red es un dominio de broadcast.
3. Multicast: de un equipo a un grupo que se suscribió (rango 224.0.0.0/4). Lo usan algunos protocolos de enrutamiento y el video en grupo.

## El gateway por defecto

Cuando una PC quiere hablar con una IP, primero hace la cuenta del AND: ¿el destino está en mi misma red? Si sí, le manda directo (con ARP saca la MAC). Si no, le manda al gateway por defecto, que es la dirección del router en su red.

El gateway tiene que estar en la misma red que la PC. Una PC con 192.168.10.37/24 y gateway 192.168.11.1 no va a poder salir nunca, porque no puede llegar a su propio gateway.

En Comercial El Guayabo usamos una regla para todo el curso: el gateway es la primera dirección útil de cada red. No es obligatorio, pero ordena y evita errores.

## Plan de direcciones de Comercial El Guayabo

Este es el plan que usan los ejemplos y laboratorios. Vas a ver por qué está así en los temas de subneteo, VLAN y enrutamiento.

| Red | Uso | Gateway |
|---|---|---|
| 192.168.10.0/24 | Tegucigalpa, ventas | 192.168.10.1 |
| 192.168.20.0/24 | Tegucigalpa, administración y servidores | 192.168.20.1 |
| 192.168.30.0/24 | Tegucigalpa, bodega | 192.168.30.1 |
| 192.168.40.0/24 | San Pedro Sula | 192.168.40.1 |
| 192.168.50.0/24 | La Ceiba | 192.168.50.1 |
| 10.0.0.0/30 | Enlace WAN Tegucigalpa y San Pedro Sula | No aplica |
| 10.0.0.4/30 | Enlace WAN Tegucigalpa y La Ceiba | No aplica |
| 203.0.113.0/30 | Enlace a internet de Tegucigalpa (dirección de documentación) | 203.0.113.1, del proveedor |

## Errores comunes

1. Pensar que toda dirección que termina en 0 es de red y toda la que termina en 255 es broadcast. Depende de la máscara, como viste en el caso 4.
2. Olvidar restar 2 al calcular hosts útiles, o restarlo en un /31.
3. Escribir máscaras imposibles, como 255.255.255.100. Los bits en 1 van seguidos, así que el octeto solo puede valer alguno de los nueve valores de la tabla.
4. Poner el gateway en otra red.
5. Confundir 172.16.0.0/12 (todo el rango privado) con 172.16.0.0/16 (solo una parte).
6. Asumir la máscara por la clase. 10.1.1.1 no es /8 si nadie lo dijo; siempre preguntá el prefijo.
7. Usar la dirección de red o la de broadcast en un equipo.

## Preguntas de repaso

1. ¿Por qué un octeto no puede valer 256?
2. Convertí a binario 172, 224 y 99. Convertí a decimal `11110000` y `00111111`.
3. ¿Qué hace la máscara? Explicalo con la comparación de la dirección postal.
4. ¿Cuántos hosts útiles tiene una red /27? ¿Y una /20?
5. ¿Por qué no se le puede poner a un equipo la dirección de broadcast?
6. ¿Qué te dice que una PC tenga 169.254.33.10?
7. ¿Es privada 172.30.5.1? ¿Y 172.33.5.1? ¿Y 192.169.1.1?
8. ¿Cómo decide una PC si manda un paquete directo o por el gateway?

## Fuentes

1. [RFC 791, protocolo IP](https://www.rfc-editor.org/rfc/rfc791) (en)
2. [RFC 1918, direcciones para redes privadas](https://www.rfc-editor.org/rfc/rfc1918) (en)
3. [RFC 4632, CIDR](https://www.rfc-editor.org/rfc/rfc4632) (en)
4. [RFC 5737, direcciones IPv4 para documentación](https://www.rfc-editor.org/rfc/rfc5737) (en)
5. [RFC 6598, espacio compartido 100.64.0.0/10](https://www.rfc-editor.org/rfc/rfc6598) (en)
6. [RFC 3021, prefijos /31 en enlaces punto a punto](https://www.rfc-editor.org/rfc/rfc3021) (en)
7. [Registro IANA de direcciones IPv4 de propósito especial](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml) (en)
8. [Módulo ipaddress de Python](https://docs.python.org/es/3/library/ipaddress.html) (es), el que usa el revisor de este repo
