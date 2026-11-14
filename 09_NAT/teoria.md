# 09. NAT

Todas las PC de Comercial El Guayabo tienen direcciones privadas (192.168.x.x), y en el tema 02 vimos que esas direcciones no se enrutan en internet. Sin embargo, una cajera abre el portal del banco sin problema. Lo que hace posible eso es NAT (Network Address Translation, traducción de direcciones): el router de Tegucigalpa cambia la dirección privada de cada paquete por su dirección pública al salir, y la vuelve a cambiar al entrar la respuesta.

NAT fue la solución que permitió que IPv4 durara décadas más de lo previsto. Entenderlo bien te sirve para configurar la salida a internet, para publicar un servidor y para diagnosticar cuando "la red interna anda y el internet no".

## La idea

El proveedor le da a la empresa una sola dirección pública, 203.0.113.2 (usamos un rango de documentación). Adentro hay más de cien equipos. Cuando una PC manda un paquete a internet:

1. Sale de la PC con origen 192.168.10.25 y destino, por ejemplo, 198.51.100.80.
2. R_TGU cambia el origen a 203.0.113.2 y anota el cambio en su tabla de traducciones.
3. El servidor de internet responde a 203.0.113.2.
4. R_TGU busca en la tabla, ve que esa conversación era de 192.168.10.25, cambia el destino y se lo entrega.

Para el resto de internet, toda la empresa es una sola dirección.

## El vocabulario de Cisco

Los cuatro nombres que usa Cisco confunden al principio, pero son lógicos si se leen como "de qué lado está el equipo" y "desde dónde se mira la dirección":

| Término | Qué es | En el ejemplo |
|---|---|---|
| Inside local | La dirección del equipo interno, como se ve adentro | 192.168.10.25 |
| Inside global | La dirección del equipo interno, como se ve afuera | 203.0.113.2 |
| Outside global | La dirección del equipo externo, como se ve afuera | 198.51.100.80 |
| Outside local | La dirección del equipo externo, como se ve adentro | 198.51.100.80 (casi siempre igual a la global) |

Las interfaces también se marcan: `ip nat inside` en las que dan a la red interna y `ip nat outside` en la que da a internet. Si te olvidás de marcar una, NAT no funciona.

## Los tres tipos de NAT

### NAT estática: una a una, fija

Una dirección privada se traduce siempre a la misma pública. Sirve para que un servidor interno sea alcanzable desde internet con una dirección fija. Necesita una pública por cada servidor.

### NAT dinámica: de un grupo de públicas

El router tiene un grupo (pool) de direcciones públicas y se las va prestando a los equipos internos a medida que salen. Si el pool tiene 5 y quieren salir 6 equipos a la vez, el sexto no puede. Hoy casi no se usa, porque las públicas son caras.

### PAT o NAT con sobrecarga: muchas a una

Es la que se usa en casi todas las empresas y en todos los routers de casa. Todos los equipos comparten una sola pública y el router los distingue por el puerto de origen. Si dos PC usan el mismo puerto de origen, el router le cambia el puerto a una de ellas.

#### Caso resuelto 1: la tabla de PAT

Tres equipos de Tegucigalpa navegan al mismo tiempo:

| Inside local | Inside global | Outside global |
|---|---|---|
| 192.168.10.25:51000 | 203.0.113.2:51000 | 198.51.100.80:443 |
| 192.168.10.26:51000 | 203.0.113.2:1024 | 198.51.100.80:443 |
| 192.168.20.40:50122 | 203.0.113.2:50122 | 192.0.2.53:53 |

La segunda PC usó el mismo puerto de origen que la primera hacia el mismo destino, así que el router le asignó otro (1024). Cuando vuelve una respuesta a 203.0.113.2:1024, el router sabe que es para 192.168.10.26:51000.

Con un puerto de 16 bits hay unas 65 000 combinaciones por dirección pública y por destino, de sobra para una empresa como esta.

## Configuración en Cisco

### Caso resuelto 2: PAT para toda la empresa en R_TGU

```
interface g0/0.10
 ip nat inside
interface g0/0.20
 ip nat inside
interface g0/0.30
 ip nat inside
interface s0/0/0
 ip nat inside
interface s0/0/1
 ip nat inside
interface g0/1
 ip nat outside
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface g0/1 overload
```

Paso por paso:

1. Las subinterfaces de las VLAN y los enlaces hacia las sucursales son "inside", porque el tráfico de San Pedro Sula y La Ceiba también sale a internet por Tegucigalpa.
2. g0/1, la que va al proveedor, es "outside".
3. La lista de acceso 1 dice qué direcciones se traducen. Con la wildcard 0.0.255.255 cubre todo 192.168.0.0/16: todas las LAN de la empresa. Los enlaces 10.0.0.x no se incluyen porque no navegan.
4. La última línea dice: a lo que entre por inside y coincida con la lista 1, cambiale el origen por la dirección de la interfaz g0/1, con sobrecarga (PAT).

Usar `interface g0/1` en lugar de escribir la IP pública tiene una ventaja: si el proveedor cambia la dirección por DHCP, NAT sigue funcionando.

Y no te olvidés de la ruta por defecto hacia el proveedor del tema 07. Sin ruta, NAT no tiene nada que traducir porque el paquete no sale.

### Caso resuelto 3: publicar un servidor con NAT estática de puerto

La empresa quiere que los clientes vean el catálogo en línea, que corre en el servidor 192.168.20.30 en el puerto 443. Solo tiene una pública. Se traduce solo ese puerto (esto se llama redirección de puerto o port forwarding):

```
ip nat inside source static tcp 192.168.20.30 443 interface g0/1 443
```

Lo que llegue a 203.0.113.2 por TCP 443 se manda a 192.168.20.30:443. Todo lo demás sigue funcionando con PAT.

Ojo con lo que esto significa: ese servidor queda expuesto a todo internet. Tiene que estar actualizado y, si se puede, en una red separada (una DMZ) para que si lo comprometen no tengan paso libre al resto de la empresa.

### Caso resuelto 4: NAT estática completa y NAT dinámica

Si el proveedor le diera a la empresa un bloque 198.51.100.0/29 (seis públicas útiles):

NAT estática completa para un servidor:

```
ip nat inside source static 192.168.20.30 198.51.100.2
```

NAT dinámica con un pool:

```
ip nat pool PUBLICAS 198.51.100.3 198.51.100.6 netmask 255.255.255.248
access-list 2 permit 192.168.10.0 0.0.0.255
ip nat inside source list 2 pool PUBLICAS
```

Si al final se agrega `overload`, el pool se usa con PAT y deja de haber límite de cuatro equipos.

## Verificar y diagnosticar

| Comando | Qué mirar |
|---|---|
| `show ip nat translations` | La tabla de traducciones activas. Si está vacía mientras una PC navega, NAT no está traduciendo |
| `show ip nat statistics` | Cuántas traducciones hay, qué interfaces son inside y outside, cuántos paquetes no coincidieron |
| `clear ip nat translation *` | Borra las traducciones dinámicas, útil después de cambiar la configuración |
| `debug ip nat` | Muestra cada traducción en vivo. En un router de producción con mucho tráfico, mejor no |

Orden de diagnóstico para "las PC no salen a internet":

1. ¿La PC llega a su gateway y a la IP pública del router? Si no, el problema es interno.
2. ¿El router llega a internet? `ping 8.8.8.8` desde el router. Si no, es el enlace o la ruta por defecto.
3. ¿Las interfaces están bien marcadas como inside y outside? `show ip nat statistics`.
4. ¿La lista de acceso cubre la red de la PC? Un error típico es una wildcard mal escrita.
5. ¿Aparecen traducciones cuando la PC intenta salir? `show ip nat translations`.
6. Si sale por IP pero no por nombre, es DNS, no NAT.

## Lo que NAT rompe y lo que no es

1. NAT no es un firewall. Es cierto que con PAT nadie de afuera puede iniciar una conexión a una PC interna si no hay una regla de redirección, y eso protege. Pero no inspecciona nada: lo que la PC inicia hacia afuera (un programa malicioso que se conecta a su servidor) pasa sin problema. La seguridad la da el firewall.
2. NAT complica las aplicaciones que meten direcciones IP dentro de sus datos o que necesitan conexiones desde afuera, como algunas llamadas de voz o los juegos en línea. Hay técnicas para manejarlo, pero a veces dan problemas.
3. NAT esconde quién hizo qué. En un registro de un servidor externo, todas las conexiones de la empresa salen con la misma IP. Por eso, si hay que investigar un incidente, los registros del propio router son importantes.
4. NAT del proveedor (CGNAT): muchos proveedores, sobre todo móviles, ponen a sus clientes detrás de otro NAT, con direcciones del rango 100.64.0.0/10. En ese caso la empresa no puede publicar servidores aunque configure bien su router, porque su "pública" no es pública.

## NAT e IPv6

IPv6 tiene direcciones de sobra y el diseño normal no usa NAT: cada equipo tiene su dirección global. La protección que antes daba NAT de forma accidental la tiene que dar el firewall con una regla clara: permitir lo que sale y sus respuestas, y bloquear lo que intenta entrar sin haberlo pedido. Existen traducciones entre IPv6 e IPv4 (NAT64), pero son para la convivencia de los dos, no para ahorrar direcciones.

## Errores comunes

1. Olvidar `ip nat inside` en alguna interfaz interna, por ejemplo en los enlaces de las sucursales: Tegucigalpa navega y las sucursales no.
2. Wildcard al revés en la lista de acceso: `255.255.0.0` en lugar de `0.0.255.255`.
3. Olvidar `overload` y quedarse con NAT dinámica de una sola dirección: solo un equipo navega a la vez.
4. Olvidar la ruta por defecto.
5. Publicar un servidor con redirección de puerto sin separarlo ni actualizarlo.
6. Pensar que NAT reemplaza al firewall.
7. Traducir también el tráfico entre sucursales: si la lista incluye destinos internos y las interfaces están mal marcadas, las sucursales ven todo con la IP pública y los registros pierden sentido.

## Preguntas de repaso

1. ¿Por qué hace falta NAT en IPv4? ¿Por qué no en IPv6?
2. Explicá inside local, inside global y outside global con un ejemplo de la empresa.
3. ¿En qué se diferencian NAT estática, dinámica y PAT? ¿Cuándo usás cada una?
4. ¿Cómo hace PAT para saber a qué PC devolver una respuesta?
5. ¿Qué hace cada línea de la configuración del caso 2?
6. ¿Qué riesgos trae publicar un servidor con redirección de puerto?
7. ¿Por qué se dice que NAT no es un firewall?
8. ¿Qué es CGNAT y cómo te das cuenta de que estás detrás de uno?

## Fuentes

1. [RFC 3022, NAT tradicional](https://www.rfc-editor.org/rfc/rfc3022) (en)
2. [RFC 1918, direcciones privadas](https://www.rfc-editor.org/rfc/rfc1918) (en)
3. [RFC 6598, espacio compartido para CGNAT](https://www.rfc-editor.org/rfc/rfc6598) (en)
4. [RFC 5737, direcciones de documentación](https://www.rfc-editor.org/rfc/rfc5737) (en), las que usamos como públicas inventadas
