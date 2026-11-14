# 01. Modelo OSI y modelo TCP/IP

Cuando una cajera de Comercial El Guayabo en San Pedro Sula registra una venta, el sistema le manda los datos a un servidor en Tegucigalpa. Entre la caja y el servidor hay un cable, un switch, un router, un enlace de un proveedor, otro router y otro switch. Cada uno hace una parte del trabajo y ninguno sabe hacer todo. Los modelos por capas sirven para entender quién hace qué, y sobre todo para saber dónde buscar cuando algo falla.

En este tema vas a ver los dos modelos que se usan: OSI, que tiene siete capas y se usa para explicar y diagnosticar, y TCP/IP, que tiene cuatro y es el que de verdad corre en las redes. Al final vas a poder seguir un paquete desde que sale de una PC hasta que llega al servidor, y decir en qué capa está cada problema.

## Por qué existen los modelos por capas

Imaginá que cada fabricante hiciera su red a su manera: una impresora de una marca no podría hablar con una PC de otra. En los años setenta y ochenta eso pasaba. La solución fue partir el problema de comunicarse en pedazos, ponerle reglas a cada pedazo (los protocolos) y decir qué le entrega cada pedazo al siguiente.

Esa división trae tres ventajas que vas a usar todo el tiempo:

1. Cada capa se puede cambiar sin tocar las demás. Pasar de cable a wifi cambia la capa física y la de enlace, pero el navegador sigue igual.
2. Los fabricantes pueden especializarse. Quien hace tarjetas de red no necesita saber de HTML.
3. Los problemas se ordenan. Si el cable está desconectado, no tiene sentido revisar el DNS.

## El modelo OSI, capa por capa

OSI (Open Systems Interconnection) lo publicó la ISO a finales de los setenta y principios de los ochenta. Casi ningún equipo implementa OSI tal cual, pero su vocabulario se quedó: cuando alguien dice "es un problema de capa 2" o "un switch de capa 3", está hablando en OSI.

Las capas se numeran de abajo hacia arriba:

| N.° | Capa | Qué resuelve | Unidad de datos | Ejemplos |
|---:|---|---|---|---|
| 7 | Aplicación | Lo que el usuario o el programa necesita de la red | Datos | HTTP, DNS, SMTP, DHCP |
| 6 | Presentación | Formato, codificación y cifrado de los datos | Datos | TLS, UTF 8, JPEG |
| 5 | Sesión | Abrir, mantener y cerrar conversaciones | Datos | Control de sesiones de una app |
| 4 | Transporte | Entrega de extremo a extremo entre programas | Segmento (TCP) o datagrama (UDP) | TCP, UDP |
| 3 | Red | Direcciones lógicas y elegir el camino entre redes | Paquete | IPv4, IPv6, ICMP |
| 2 | Enlace de datos | Entrega dentro de la misma red local | Trama | Ethernet, wifi (802.11), ARP |
| 1 | Física | Bits como señales eléctricas, de luz o de radio | Bits | Cable UTP, fibra, conectores RJ45 |

Una forma de recordarlas de abajo hacia arriba es "Felipe Envió Rosas Tras Sentirse Profundamente Arrepentido": Física, Enlace, Red, Transporte, Sesión, Presentación, Aplicación. Inventá la tuya si esa no te sirve.

### Capa 1, física

Su trabajo es mover bits. No sabe qué significan, solo los convierte en voltajes por un cable de cobre, pulsos de luz por fibra u ondas de radio. Aquí entran el tipo de cable (UTP categoría 5e o 6), los conectores, el largo máximo (100 metros para UTP en Ethernet), la velocidad y las interferencias.

Los equipos de esta capa son los cables, los conectores, los repetidores y los antiguos hubs. Un hub repite lo que le llega por un puerto a todos los demás, sin entender nada.

Problemas típicos: cable dañado o mal ponchado, conector flojo, cable demasiado largo, puerto quemado, interferencia en wifi. Lo primero que se mira son las lucecitas del puerto.

### Capa 2, enlace de datos

Toma los bits y los organiza en tramas, con una dirección de origen y una de destino dentro de la red local. Esas direcciones son las MAC: 48 bits escritos en hexadecimal, por ejemplo `00:1A:2B:3C:4D:5E`. La MAC viene grabada en la tarjeta de red (aunque se puede cambiar por software) y solo tiene sentido dentro de la misma red local.

La trama Ethernet lleva MAC de destino, MAC de origen, el tipo de lo que va adentro, los datos y al final un código para detectar errores (FCS). Si la trama llega dañada, el equipo que la recibe la descarta.

El equipo típico de la capa 2 es el switch. Aprende qué MAC está detrás de cada puerto mirando el origen de cada trama, y arma una tabla. Cuando le llega una trama, la manda solo por el puerto donde está el destino. Si todavía no conoce el destino, la manda por todos los puertos menos por el que entró (eso se llama inundar).

Aquí también vive ARP, que traduce una dirección IP a la MAC que le corresponde dentro de la red local. Lo vas a ver con calma en el tema 10.

### Capa 3, red

Le da a cada equipo una dirección lógica, la IP, que dice en qué red está y qué equipo es dentro de esa red. Y decide por dónde mandar un paquete para que llegue a otra red. Ese trabajo de elegir el camino se llama enrutamiento y lo hacen los routers.

La diferencia con la capa 2 es el alcance. La MAC sirve para el siguiente salto dentro de la misma red; la IP sirve de punta a punta. Cuando un paquete va de San Pedro Sula a Tegucigalpa, la IP de origen y de destino se mantienen todo el viaje (salvo que haya NAT, tema 09), pero las MAC cambian en cada router.

Protocolos de esta capa: IPv4, IPv6 e ICMP (el de `ping`). Equipos: routers y switches de capa 3.

### Capa 4, transporte

Una PC tiene muchos programas usando la red a la vez: el navegador, el correo, el sistema de ventas. La capa 4 se encarga de que los datos lleguen al programa correcto, usando números de puerto. Un servidor web escucha en el puerto 443 (HTTPS); un servidor DNS en el 53.

Hay dos protocolos principales:

| | TCP | UDP |
|---|---|---|
| Conexión | Sí, se establece antes de mandar datos (saludo de tres pasos: SYN, SYN ACK, ACK) | No, manda y ya |
| Confiabilidad | Confirma lo que llega y reenvía lo que se pierde | Si algo se pierde, se perdió |
| Orden | Entrega en orden | Puede llegar desordenado |
| Costo | Más encabezado y más espera | Liviano y rápido |
| Se usa en | Web, correo, transferencia de archivos, bases de datos | DNS, DHCP, voz y video en vivo, juegos |

¿Por qué la voz por internet usa UDP? Porque si un pedacito de audio llega tarde ya no sirve: es mejor perderlo que esperar el reenvío y escuchar la llamada con retraso. En cambio una factura no puede llegar con una línea menos, por eso el sistema de ventas usa TCP.

Algunos puertos que conviene saber de memoria: 20 y 21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 67 y 68 DHCP, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 3389 escritorio remoto de Windows. La lista oficial la mantiene la IANA.

### Capas 5, 6 y 7: sesión, presentación y aplicación

En la práctica estas tres casi siempre las hace el mismo programa, y por eso TCP/IP las junta en una sola. Igual conviene saber qué idea representa cada una:

1. Sesión: mantener una conversación que dura varios intercambios, por ejemplo saber que todas las peticiones de tu navegador son de tu misma sesión en el sistema.
2. Presentación: ponerse de acuerdo en el formato. Si un equipo manda texto en UTF 8 y el otro lo lee en otra codificación, las tildes salen rotas. El cifrado (TLS) se suele ubicar aquí.
3. Aplicación: los protocolos que usan los programas, como HTTP para la web, DNS para traducir nombres, SMTP para mandar correo o DHCP para recibir una IP.

Ojo con una confusión común: la capa de aplicación no es el programa (Chrome, Outlook), sino el protocolo que el programa usa para hablar por la red.

## El modelo TCP/IP

TCP/IP nació de la investigación de ARPANET en Estados Unidos y es el que de verdad usa internet. Sus reglas están en documentos públicos llamados RFC. El RFC 1122 describe cómo se dividen las capas en un equipo conectado a internet.

| TCP/IP | Corresponde en OSI | Protocolos |
|---|---|---|
| Aplicación | 7, 6 y 5 | HTTP, DNS, DHCP, SMTP, SSH |
| Transporte | 4 | TCP, UDP |
| Internet | 3 | IPv4, IPv6, ICMP |
| Acceso a la red (o enlace) | 2 y 1 | Ethernet, wifi |

Algunos libros y cursos (Cisco NetAcad, por ejemplo) usan una versión de cinco capas que separa física y enlace. No es otro modelo, es la misma idea con la capa de abajo partida en dos.

¿Cuál usar? Para diagnosticar y para hablar con otros técnicos se usa la numeración OSI ("capa 2", "capa 3"). Para entender qué protocolos existen y cómo se relacionan, TCP/IP.

## Encapsulamiento: cómo viaja un dato

Cada capa le agrega su propio encabezado a lo que le entrega la capa de arriba. A eso se le llama encapsular. Cuando llega al destino, cada capa quita su encabezado y le pasa el resto a la de arriba (desencapsular).

```
Aplicación   [ datos de la venta                                  ]
Transporte   [ TCP | datos de la venta                            ]   segmento
Red          [ IP  | TCP | datos de la venta                      ]   paquete
Enlace       [ Eth | IP  | TCP | datos de la venta          | FCS ]   trama
Física       0101100101011100011010...                                bits
```

### Caso resuelto: una venta de San Pedro Sula llega a Tegucigalpa

Datos del caso:

1. La caja de San Pedro Sula tiene la IP 192.168.40.25, su gateway (el router de la sucursal, R_SPS) es 192.168.40.1.
2. El servidor de ventas en Tegucigalpa tiene 192.168.20.10 y escucha HTTPS en el puerto 443.
3. Entre R_SPS y R_TGU hay un enlace WAN.

Paso a paso:

1. Aplicación. El sistema de ventas arma una petición HTTPS con los datos de la venta. TLS la cifra.
2. Transporte. TCP le pone puerto de destino 443 y un puerto de origen al azar que la PC elige, por ejemplo 51544. Si es la primera vez, antes hace el saludo de tres pasos con el servidor.
3. Red. IP le pone origen 192.168.40.25 y destino 192.168.20.10. La PC compara su red con la del destino: 192.168.40.0/24 no es 192.168.20.0/24, así que el paquete tiene que salir por el gateway.
4. Enlace. La PC necesita la MAC del gateway, no la del servidor. La pregunta con ARP ("¿quién tiene 192.168.40.1?"), R_SPS contesta, y la trama sale con MAC de destino igual a la de R_SPS.
5. Física. La tarjeta convierte la trama en señales por el cable hasta el switch de la sucursal, que la entrega por el puerto donde está R_SPS.
6. En R_SPS. El router quita la trama (capa 2), mira la IP de destino (capa 3), busca en su tabla de enrutamiento y ve que 192.168.20.0/24 se alcanza por el enlace WAN. Arma una trama nueva para ese enlace y la manda. Las IP no cambiaron; las MAC sí.
7. En R_TGU pasa lo mismo: ve que 192.168.20.0/24 está conectada directamente, pregunta con ARP la MAC del servidor y le entrega la trama.
8. En el servidor se desencapsula hacia arriba: Ethernet ve que la trama es para su MAC, IP ve que el paquete es para su IP, TCP ve el puerto 443 y le entrega los datos al servicio web, TLS descifra y la aplicación registra la venta.

Lo que tenés que llevarte de este caso: la IP de origen y destino viaja igual de punta a punta; la MAC se reescribe en cada salto. Si eso te queda claro, el resto de redes se entiende mucho mejor.

## Qué equipo trabaja en qué capa

| Equipo | Capa más alta que entiende | Qué mira para decidir |
|---|---|---|
| Hub, repetidor | 1 | Nada, repite todo |
| Switch | 2 | MAC de destino |
| Router | 3 | IP de destino y su tabla de enrutamiento |
| Switch de capa 3 | 3 | MAC y también IP |
| Firewall | 3, 4 y a veces 7 | IP, puertos y en algunos casos el contenido |
| PC, servidor | 7 | Todas las capas |

## Diagnosticar por capas

La gran utilidad del modelo en el trabajo es ordenar la búsqueda de fallas. Hay tres formas de recorrer las capas:

1. De abajo hacia arriba: empezás por el cable y subís. Sirve cuando no tenés idea de qué pasa o cuando es algo nuevo.
2. De arriba hacia abajo: empezás por la aplicación. Sirve cuando la red funciona para otras cosas y solo falla un programa.
3. Divide y vencerás: empezás en la capa 3 con un `ping`. Si responde, el problema está arriba; si no, abajo. Es lo que más usan los técnicos con experiencia.

Ejemplo: "en la bodega de La Ceiba no abre el sistema de inventario".

1. ¿Los demás de la bodega sí pueden? Si nadie puede, es algo compartido (switch, router, enlace). Si solo una PC, es esa PC.
2. Capa 1 y 2: ¿la luz del puerto está encendida? ¿La PC tiene red o dice "cable desconectado"?
3. Capa 3: `ipconfig` para ver si tiene IP. Si tiene 169.254.x.x, no le llegó DHCP. Después `ping` al gateway y al servidor.
4. Capa 4: ¿el servidor escucha en el puerto? ¿Algún firewall lo bloquea?
5. Capa 7: ¿el nombre del servidor resuelve? ¿Las credenciales están bien?

El tema 10 está dedicado a estas herramientas.

## Errores comunes

1. Pensar que la MAC sirve para llegar a otra red. La MAC solo sirve dentro de la red local; para salir, la trama va a la MAC del gateway.
2. Decir que un switch "trabaja con IP". Un switch común de capa 2 no mira la IP. Un switch de capa 3 sí, pero eso es otro equipo.
3. Confundir el programa con el protocolo. Chrome no es la capa 7; HTTP sí.
4. Creer que UDP es "malo" porque no confirma. Es la elección correcta cuando la rapidez importa más que repetir lo perdido.
5. Aprenderse las capas de memoria sin poder decir qué hace cada una. En los exámenes y en las entrevistas preguntan casos, no la lista.
6. Pensar que TCP/IP y OSI compiten. OSI es el mapa para explicar; TCP/IP es lo que se implementa.

## Preguntas de repaso

1. ¿Por qué se dividió la comunicación en capas? Da dos ventajas con un ejemplo de Comercial El Guayabo.
2. ¿Qué cambia y qué se mantiene en un paquete cuando cruza un router?
3. Un usuario tiene la luz del puerto apagada. ¿En qué capa está el problema y qué revisarías primero?
4. ¿Por qué una llamada por internet usa UDP y una transferencia de archivos usa TCP?
5. Relacioná las cuatro capas de TCP/IP con las siete de OSI.
6. ¿Qué es encapsular? Dibujá los encabezados que lleva una trama que transporta una consulta DNS.
7. ¿Para qué necesita una PC la MAC de su gateway?
8. Nombrá un equipo de capa 1, uno de capa 2 y uno de capa 3, y qué mira cada uno para decidir.

## Fuentes

1. [RFC 1122, requisitos para equipos de internet: capas de comunicación](https://www.rfc-editor.org/rfc/rfc1122) (en)
2. [RFC 791, protocolo IP](https://www.rfc-editor.org/rfc/rfc791) (en)
3. [RFC 9293, protocolo TCP](https://www.rfc-editor.org/rfc/rfc9293) (en) y [RFC 768, protocolo UDP](https://www.rfc-editor.org/rfc/rfc768) (en)
4. [Registro de puertos y servicios de la IANA](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml) (en)
5. [Networking Basics de Cisco NetAcad](https://www.netacad.com/courses/networking-basics), curso gratuito con cuenta (en)
