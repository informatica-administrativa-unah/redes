# 08. DHCP y DNS

Hay dos servicios que nadie ve cuando funcionan y que todos notan cuando fallan. DHCP le da a cada equipo su dirección, su máscara, su gateway y su servidor DNS sin que nadie tenga que escribirlos. DNS traduce nombres como `ventas.interno.guayabo.example` a direcciones IP. Cuando una cajera dice "no hay internet", la mitad de las veces el problema es uno de estos dos.

## Parte 1. DHCP

### El problema que resuelve

Comercial El Guayabo tiene más de cien equipos entre las tres sucursales. Configurar a mano la IP de cada uno tiene tres problemas: lleva tiempo, es fácil equivocarse (dos equipos con la misma IP, una máscara mal puesta) y cada cambio de la red obliga a visitar cada PC. Con laptops y celulares que entran y salen, es imposible.

DHCP (Dynamic Host Configuration Protocol, RFC 2131) automatiza todo eso: un servidor tiene un rango de direcciones (un pool o ámbito) y se las presta a los equipos que las piden.

### Qué entrega

Lo mínimo:

1. Dirección IP y máscara.
2. Gateway por defecto.
3. Servidores DNS.
4. Tiempo de préstamo (lease).

Y puede entregar mucho más: nombre de dominio, servidor de hora, datos para teléfonos IP. Esas "opciones" están definidas en el RFC 2132.

### El proceso DORA

Cuando una PC se enciende sin IP, pasa por cuatro mensajes. Se recuerdan con la palabra DORA:

| Paso | Mensaje | De | A | Qué dice |
|---|---|---|---|---|
| 1 | Discover | Cliente, desde 0.0.0.0 | Broadcast 255.255.255.255 | "¿Hay algún servidor DHCP?" |
| 2 | Offer | Servidor | Cliente | "Te ofrezco 192.168.40.37 por 24 horas" |
| 3 | Request | Cliente | Broadcast | "Acepto la oferta de ese servidor" |
| 4 | Acknowledge (ACK) | Servidor | Cliente | "Confirmado, es tuya" |

¿Por qué el Request va por broadcast si ya conoce al servidor? Porque si hubo dos servidores que ofrecieron, el broadcast le avisa al otro que su oferta no se aceptó y puede liberar esa dirección.

DHCP usa UDP: el servidor escucha en el puerto 67 y el cliente en el 68.

### El préstamo y su renovación

La dirección no es para siempre. A la mitad del tiempo de préstamo el cliente le pide al mismo servidor que se lo renueve. Si no le contesta, vuelve a intentar más adelante con cualquier servidor. Si se vence sin renovar, el cliente deja de usar la dirección.

¿Qué tiempo conviene? Préstamos cortos (unas horas) en redes con mucho movimiento, como el wifi de clientes, para que las direcciones de los que ya se fueron vuelvan rápido al pool. Préstamos largos (días) en redes de oficina estables.

### Direcciones excluidas y reservas

No todo se reparte. El gateway, los servidores, las impresoras y los equipos de red necesitan direcciones fijas. Hay dos formas:

1. Excluir un rango del pool y configurar esos equipos a mano. Es lo que se hace con el gateway y los servidores.
2. Reservar: el servidor le da siempre la misma IP a una MAC concreta. Es cómodo para impresoras: la dirección no cambia y se sigue administrando desde el servidor.

Una costumbre ordenada: las primeras direcciones de cada red (de .1 a .20, por ejemplo) quedan fuera del pool para equipos fijos.

### Caso resuelto 1: DHCP en el router de San Pedro Sula

La red es 192.168.40.0/24, el gateway 192.168.40.1, el DNS interno está en Tegucigalpa en 192.168.20.10, y se dejan las primeras 20 direcciones para equipos fijos.

```
ip dhcp excluded-address 192.168.40.1 192.168.40.20
ip dhcp pool SPS_LAN
 network 192.168.40.0 255.255.255.0
 default-router 192.168.40.1
 dns-server 192.168.20.10 8.8.8.8
 domain-name interno.guayabo.example
 lease 1
```

1. La exclusión va antes del pool, en modo global.
2. `lease 1` es un día.
3. Se ponen dos DNS: el interno primero y uno público de respaldo. Ojo que el público no conoce los nombres internos.

Para revisar: `show ip dhcp binding` muestra qué IP se le dio a qué MAC, y `show ip dhcp pool` cuántas quedan.

### DHCP entre redes: el agente de retransmisión

El Discover va por broadcast, y los routers no reenvían broadcast. Entonces, si el servidor DHCP de la empresa está en Tegucigalpa (por ejemplo un Windows Server en 192.168.20.10), los pedidos de las PC de La Ceiba nunca le llegarían.

La solución es el agente de retransmisión (relay): el router de La Ceiba recibe el broadcast y lo reenvía como unicast al servidor, anotando en el mensaje de qué red viene. El servidor ve esa nota y elige el pool correcto. En Cisco se configura en la interfaz que da a las PC:

```
interface g0/0
 ip helper-address 192.168.20.10
```

El servidor necesita un pool para 192.168.50.0/24 y una ruta de vuelta hacia esa red. Sin la ruta, recibe el pedido pero su respuesta no vuelve.

### Cuando DHCP falla

Si una PC con Windows no recibe respuesta, se pone sola una dirección 169.254.x.x (APIPA). Con esa dirección solo puede hablar con otras PC que también tengan 169.254, así que en la práctica se queda sin red. Ver 169.254 en `ipconfig` es una pista clarísima: el problema está entre la PC y el servidor DHCP.

Causas típicas, en el orden en que conviene revisarlas:

1. Cable, puerto o wifi: la PC no tiene enlace.
2. Puerto del switch en la VLAN equivocada: la PC pide en una red donde no hay servidor.
3. Falta `ip helper-address` o apunta a una IP equivocada.
4. El pool se llenó: todas las direcciones están prestadas.
5. El servidor DHCP está apagado o su servicio detenido.

Comandos en la PC: `ipconfig /release` suelta la dirección y `ipconfig /renew` la pide de nuevo, y así ves si el servidor responde.

### Seguridad en DHCP

Dos ataques conocidos:

1. Servidor DHCP falso: alguien conecta un router de casa o una laptop con DHCP. Algunas PC reciben su oferta, con un gateway falso, y todo su tráfico pasa por el atacante o se pierde. Pasa mucho por accidente, cuando un empleado conecta un router wifi en su escritorio.
2. Agotamiento: un programa pide cientos de direcciones con MAC inventadas hasta vaciar el pool, y los equipos legítimos se quedan sin IP.

La defensa en switches empresariales es DHCP snooping: el switch solo permite ofertas DHCP por los puertos marcados como confiables (los que van al servidor o al router) y limita cuántos pedidos puede hacer cada puerto.

## Parte 2. DNS

### El problema que resuelve

Las personas recordamos nombres; las redes usan números. DNS (Domain Name System, RFC 1034 y 1035) es una base de datos distribuida por todo el mundo que traduce nombres a direcciones, y algunas cosas más.

### La jerarquía

Los nombres se leen de derecha a izquierda, del más general al más específico:

```
ventas.interno.guayabo.example.
  |       |       |       |    |
  |       |       |       |    +-- raíz (el punto final, que casi nunca se escribe)
  |       |       |       +------- dominio de nivel superior (TLD): .example, .hn, .com
  |       |       +--------------- dominio de la organización
  |       +----------------------- subdominio
  +------------------------------- nombre del equipo
```

Cada nivel delega en el siguiente: los servidores raíz saben quién maneja `.hn`, los de `.hn` saben quién maneja `algo.hn`, y así. Nadie tiene toda la base completa.

Sobre los nombres que usamos en el curso: `.example` está reservado para ejemplos (RFC 2606), así que `guayabo.example` no existe de verdad y no choca con nadie. En una empresa real se usa un subdominio de un dominio que la empresa tiene registrado, por ejemplo `interno.miempresa.hn`. No conviene usar `.local` para la red interna, porque está reservado para la resolución de nombres sin servidor (mDNS, RFC 6762) que usan impresoras y equipos Apple, y los dos sistemas chocan.

### Tipos de registros

| Registro | Qué guarda | Ejemplo |
|---|---|---|
| A | Nombre a dirección IPv4 | `ventas.interno.guayabo.example` → 192.168.20.10 |
| AAAA | Nombre a dirección IPv6 | `ventas.interno.guayabo.example` → 2001:db8:acad:20::10 |
| CNAME | Un nombre que es apodo de otro | `inventario` → `ventas.interno.guayabo.example` |
| MX | Qué servidor recibe el correo del dominio | `guayabo.example` → `correo.guayabo.example`, prioridad 10 |
| PTR | Al revés: dirección a nombre | `10.20.168.192.in-addr.arpa` → `ventas.interno.guayabo.example` |
| NS | Qué servidores manejan el dominio | `guayabo.example` → `ns1.guayabo.example` |
| TXT | Texto libre. Se usa para verificar dominios y para reglas de correo (SPF, DMARC) | `v=spf1 ...` |

### Cómo se resuelve un nombre

#### Caso resuelto 2: una PC de La Ceiba abre `www.ejemplo.hn`

Participan tres actores: el resolvedor de la PC (parte del sistema operativo), el servidor DNS recursivo que le dio DHCP (192.168.20.10) y los servidores autoritativos de internet.

1. La PC revisa su caché. Si ya lo resolvió hace poco y no venció, usa esa respuesta. Si no, le pregunta al recursivo: "¿cuál es la IP de www.ejemplo.hn?". Esta es una consulta recursiva: la PC espera la respuesta final.
2. El recursivo revisa su caché. Si no lo tiene, empieza las consultas iterativas.
3. Le pregunta a un servidor raíz. La raíz no sabe la IP, pero responde: "preguntale a los servidores de .hn, que están aquí".
4. Le pregunta a un servidor de `.hn`. Responde: "ejemplo.hn lo manejan estos servidores".
5. Le pregunta al servidor autoritativo de `ejemplo.hn`. Este sí sabe: "www.ejemplo.hn es 198.51.100.20".
6. El recursivo guarda la respuesta en caché por el tiempo que diga el registro (TTL) y se la da a la PC.

La próxima PC que pregunte lo mismo recibe la respuesta de la caché en milisegundos. Por eso el primer acceso a un sitio a veces tarda un poquito más.

El TTL es un arma de doble filo: un TTL largo hace todo más rápido, pero si cambiás la IP de un servidor, los clientes pueden seguir yendo a la vieja hasta que venza. Antes de mudar un servidor se baja el TTL con días de anticipación.

### DNS interno de la empresa

En Comercial El Guayabo el servidor 192.168.20.10 hace dos trabajos:

1. Autoritativo para `interno.guayabo.example`: tiene los registros A de los servidores y equipos internos.
2. Recursivo para todo lo demás: las PC le preguntan por cualquier sitio de internet y él resuelve.

Por eso a las PC se les da ese DNS primero. Si a una PC se le pone solo 8.8.8.8, navega en internet pero no encuentra los nombres internos: es el síntoma "internet sí, el sistema no".

### DNS usa UDP y TCP

Las consultas normales van por UDP al puerto 53 porque son chicas y rápidas. Si la respuesta es muy grande, o para copiar zonas completas entre servidores, se usa TCP 53. Hoy existen también DNS cifrado sobre TLS (RFC 7858, puerto 853) y sobre HTTPS (RFC 8484, puerto 443), que evitan que alguien en el camino vea qué nombres consultás.

### Herramientas

En Windows:

| Comando | Para qué |
|---|---|
| `nslookup ventas.interno.guayabo.example` | Pregunta al DNS configurado y muestra quién respondió |
| `nslookup ventas.interno.guayabo.example 8.8.8.8` | Pregunta a un servidor específico, útil para comparar |
| `nslookup -type=mx guayabo.example` | Pregunta por otro tipo de registro |
| `ipconfig /displaydns` | Muestra la caché DNS de la PC |
| `ipconfig /flushdns` | Borra la caché, después de un cambio de IP |

Una respuesta "no autoritativa" en `nslookup` solo quiere decir que vino de la caché de un recursivo y no del servidor dueño del dominio. No es un error.

### Seguridad en DNS

1. Envenenamiento de caché: un atacante logra meter una respuesta falsa en la caché de un recursivo, y todos los que preguntan van a un sitio falso. DNSSEC firma las respuestas para que se pueda comprobar que son legítimas.
2. Cambio del DNS en las PC o en el router: un programa malicioso pone un DNS del atacante. Se previene limitando quién puede cambiar la configuración de red y bloqueando en el firewall las consultas DNS que no vayan al servidor de la empresa.
3. DNS como filtro: muchas empresas usan su DNS para bloquear dominios conocidos de malware o phishing. Es una defensa barata y efectiva.

## Errores comunes

1. Crear el pool DHCP sin excluir el gateway y los servidores: el servidor le presta a una PC la IP del router.
2. Olvidar `ip helper-address` cuando el servidor DHCP está en otra red, o ponerlo en la interfaz equivocada (va en la que da a las PC).
3. Dar como DNS solo uno público en una red con nombres internos.
4. Pensar que 169.254 es un problema del DNS. Es de DHCP.
5. No bajar el TTL antes de cambiar la IP de un servidor.
6. Usar `.local` como dominio interno.
7. Dejar puertos de usuarios sin protección contra servidores DHCP falsos.

## Preguntas de repaso

1. Explicá los cuatro mensajes de DORA. ¿Cuáles van por broadcast y por qué?
2. ¿Para qué sirven las exclusiones y las reservas? ¿Cuándo usás cada una?
3. ¿Por qué hace falta un agente de retransmisión y qué datos agrega?
4. Una PC tiene 169.254.20.7. Dá cuatro causas posibles en orden de revisión.
5. ¿Qué diferencia hay entre una consulta recursiva y una iterativa?
6. ¿Para qué sirve el TTL y qué riesgo trae un TTL largo?
7. ¿Qué registro usarías para el correo, para un apodo y para resolver una IP a nombre?
8. ¿Por qué no conviene `.local` como dominio interno?

## Fuentes

1. [RFC 2131, DHCP](https://www.rfc-editor.org/rfc/rfc2131) (en) y [RFC 2132, opciones de DHCP](https://www.rfc-editor.org/rfc/rfc2132) (en)
2. [RFC 1034, conceptos de DNS](https://www.rfc-editor.org/rfc/rfc1034) (en) y [RFC 1035, implementación](https://www.rfc-editor.org/rfc/rfc1035) (en)
3. [RFC 2606, nombres reservados para ejemplos](https://www.rfc-editor.org/rfc/rfc2606) (en) y [RFC 6762, mDNS y el dominio .local](https://www.rfc-editor.org/rfc/rfc6762) (en)
4. [RFC 7858, DNS sobre TLS](https://www.rfc-editor.org/rfc/rfc7858) (en) y [RFC 8484, DNS sobre HTTPS](https://www.rfc-editor.org/rfc/rfc8484) (en)
5. [Documentación de nslookup](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/nslookup) (es) y [de ipconfig](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/ipconfig) (es), de Microsoft
