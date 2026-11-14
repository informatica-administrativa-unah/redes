# 10. Diagnóstico de red con ping, tracert, ipconfig y nslookup

El primer trabajo de mucha gente que sale de Informática Administrativa es de soporte, y la frase que más se escucha en soporte es "no hay internet". Detrás de esa frase puede haber un cable suelto, una IP mal puesta, un DNS caído, un enlace del proveedor o un programa que no tiene nada que ver con la red. Este tema junta todo el curso en un método para encontrar la falla rápido, con las herramientas que ya trae Windows.

## El método antes que las herramientas

Correr comandos al azar hace perder tiempo. Un método sencillo que funciona:

1. Entender el síntoma. ¿Qué no funciona exactamente? ¿Desde cuándo? ¿A quién le pasa: a una persona, a una oficina, a toda la sucursal? ¿Qué cambió? La mitad de los problemas se explican con la respuesta a "¿qué cambió?".
2. Definir el alcance. Si le pasa a una sola PC, el problema está en esa PC o en su cable. Si le pasa a toda una oficina, está en algo compartido: switch, VLAN, router, DHCP, enlace.
3. Ir por capas, con la estrategia de dividir: probar en la capa 3 con un ping. Si llega, el problema está arriba (DNS, aplicación, firewall). Si no llega, está abajo (cable, VLAN, IP, ruta).
4. Cambiar una sola cosa a la vez y probar después de cada cambio.
5. Anotar lo que encontraste y lo que hiciste. La próxima vez que pase, alguien lo va a agradecer.

### La escalera del ping

Es la secuencia clásica, de lo más cercano a lo más lejano. El primer escalón que falla te dice dónde buscar:

| Escalón | Comando (ejemplo en una PC de ventas de Tegucigalpa) | Si falla, el problema está en |
|---:|---|---|
| 1 | `ping 127.0.0.1` | La pila TCP/IP de la PC (raro; reinstalar o reiniciar) |
| 2 | `ping 192.168.10.37` (su propia IP) | La tarjeta de red o su configuración |
| 3 | `ping 192.168.10.1` (su gateway) | Cable, puerto, VLAN, IP o máscara de la PC |
| 4 | `ping 192.168.20.10` (servidor en otra red interna) | Enrutamiento entre redes o el servidor |
| 5 | `ping 203.0.113.1` (el router del proveedor) | Ruta por defecto, NAT o el enlace a internet |
| 6 | `ping 8.8.8.8` (un equipo de internet) | El proveedor o más allá |
| 7 | `ping www.ejemplo.hn` (por nombre) | DNS, si el escalón 6 funcionó |

## ipconfig

Muestra y maneja la configuración IP en Windows.

| Comando | Para qué |
|---|---|
| `ipconfig` | IP, máscara y gateway de cada adaptador |
| `ipconfig /all` | Todo: MAC, si usa DHCP, qué servidor DHCP respondió, cuándo vence el préstamo, servidores DNS |
| `ipconfig /release` y `ipconfig /renew` | Soltar y volver a pedir la dirección a DHCP |
| `ipconfig /flushdns` | Borrar la caché DNS |
| `ipconfig /displaydns` | Ver la caché DNS |

Qué buscar en la salida:

1. ¿La IP está en la red correcta para esa oficina? Una IP de otra red suele ser VLAN equivocada o un servidor DHCP falso.
2. ¿Es 169.254.x.x? No le contestó ningún DHCP.
3. ¿El gateway está en la misma red que la IP?
4. ¿Los DNS son los de la empresa?
5. ¿Dice "Medios desconectados"? Es capa 1: cable o wifi.

## ping

Manda mensajes ICMP de solicitud de eco y espera la respuesta. Mide si hay camino de ida y vuelta y cuánto tarda.

```
C:\> ping 192.168.20.10

Haciendo ping a 192.168.20.10 con 32 bytes de datos:
Respuesta desde 192.168.20.10: bytes=32 tiempo=2ms TTL=127
Respuesta desde 192.168.20.10: bytes=32 tiempo=1ms TTL=127
Respuesta desde 192.168.20.10: bytes=32 tiempo=1ms TTL=127
Respuesta desde 192.168.20.10: bytes=32 tiempo=1ms TTL=127

Estadísticas de ping para 192.168.20.10:
    Paquetes: enviados = 4, recibidos = 4, perdidos = 0 (0% perdidos),
```

Cómo leer las respuestas:

| Lo que dice | Qué significa |
|---|---|
| "Respuesta desde X: ... tiempo=..." | Llegó y volvió. El tiempo es la ida y vuelta |
| "Tiempo de espera agotado para esta solicitud" | No volvió nada. Puede ser que no llegue, que la respuesta no vuelva, o que un firewall bloquee ICMP |
| "Respuesta desde 192.168.10.37: Host de destino inaccesible" | La propia PC (o un router, según la IP que aparece) no sabe llegar o nadie contestó al ARP en la red local |
| "TTL expiró en tránsito" | El paquete dio demasiadas vueltas. Típico de un bucle de rutas entre dos routers |
| "Error general" o "La solicitud de ping no pudo encontrar el host" | Problema local, o el nombre no resolvió en DNS |

El TTL de la respuesta también da pistas: Windows arranca en 128 y Linux en 64, y cada router resta 1. TTL=127 significa que la respuesta cruzó un router.

Opciones útiles: `ping -t` hace ping sin parar hasta Ctrl+C (sirve para ver si un cable intermitente falla al moverlo), `ping -n 20` manda 20, `ping -l 1400` manda paquetes más grandes, `ping -a` intenta mostrar el nombre de la IP, y `ping -4` o `ping -6` fuerza IPv4 o IPv6.

Una advertencia: que el ping falle no siempre significa que el equipo esté caído. Muchos servidores y el firewall de Windows bloquean ICMP por defecto. Si un servidor no responde al ping pero su sistema sí abre, no hay falla de red.

## tracert

Muestra los routers por los que pasa un paquete hasta el destino. Funciona con el TTL: manda paquetes con TTL 1, luego 2, luego 3; cada router que recibe un paquete con TTL que se acaba responde "TTL expiró" y así se delata.

```
C:\> tracert 8.8.8.8

Traza a la dirección 8.8.8.8 sobre un máximo de 30 saltos:

  1     1 ms     1 ms     1 ms  192.168.40.1
  2    12 ms    11 ms    12 ms  10.0.0.1
  3    15 ms    14 ms    15 ms  203.0.113.1
  4     *        *        *     Tiempo de espera agotado para esta solicitud.
  5    40 ms    39 ms    41 ms  198.51.100.9
  ...
```

Cómo leerlo:

1. Cada línea es un salto, con tres mediciones de tiempo.
2. Un `*` aislado en medio del camino, con saltos siguientes que sí responden, no es un problema: ese router simplemente no contesta estos mensajes.
3. Si después de un salto todo es `*` hasta el final, el camino se corta ahí o después: el último router que respondió es la pista.
4. Un salto que se repite (A, B, A, B) es un bucle de rutas.
5. Un salto donde el tiempo sube mucho y se queda alto en los siguientes indica dónde está la demora.

`tracert -d` no intenta resolver nombres y va más rápido. `pathping` combina ping y tracert y mide pérdida en cada salto; tarda unos minutos pero es muy útil para fallas intermitentes.

## nslookup

Pregunta al DNS. Lo viste en el tema 08.

```
C:\> nslookup ventas.interno.guayabo.example
Servidor:  srv01.interno.guayabo.example
Address:  192.168.20.10

Nombre:  srv01.interno.guayabo.example
Address:  192.168.20.10
Aliases:  ventas.interno.guayabo.example
```

La primera parte dice qué servidor DNS respondió; la segunda, la respuesta. Para comparar, preguntá a otro servidor: `nslookup ventas.interno.guayabo.example 192.168.20.10`.

## Otras herramientas que conviene conocer

| Herramienta | Para qué |
|---|---|
| `arp -a` | La tabla ARP: qué MAC corresponde a cada IP de la red local. Si el gateway aparece con una MAC distinta a la de siempre, puede haber un ataque o un equipo duplicado |
| `netstat -ano` | Conexiones abiertas y puertos en escucha, con el número de proceso. Sirve para ver si un servicio está escuchando |
| `Test-NetConnection 192.168.20.10 -Port 443` | En PowerShell: prueba si un puerto TCP responde. Mejor que ping cuando ICMP está bloqueado |
| `Get-NetIPConfiguration` | En PowerShell: resumen de la configuración IP |
| En Linux: `ip a`, `ip route`, `ping`, `traceroute`, `dig` | Lo mismo en servidores Linux |
| En Cisco: `show ip interface brief`, `show ip route`, `show vlan brief`, `show interfaces trunk`, `show ip nat translations`, `show ip dhcp binding` | Ver el lado de la red |

## Casos resueltos

### Caso 1. "No hay internet" en una PC de bodega

Síntoma: una sola PC de la bodega de Tegucigalpa no navega. Las demás sí.

1. Alcance: una PC. Problema local.
2. `ipconfig`: IP 169.254.71.3. No recibió DHCP.
3. Luz del puerto en el switch: encendida. Capa 1 parece bien.
4. En el switch, `show vlan brief`: el puerto de esa PC está en la VLAN 1 (alguien lo movió de puerto y el nuevo no estaba configurado).
5. Arreglo: poner el puerto en la VLAN 30 y `ipconfig /renew` en la PC. Recibe 192.168.30.45 y navega.

### Caso 2. "El sistema no abre" en San Pedro Sula

Síntoma: toda la sucursal de San Pedro Sula dice que el sistema de ventas no abre. Navegan en internet sin problema. Dato que hay que saber: desde el mes pasado San Pedro Sula sale a internet por un enlace propio con un proveedor local, no por Tegucigalpa.

1. Alcance: toda una sucursal, solo con un servicio interno.
2. `ping 192.168.40.1` (su gateway): responde.
3. `ping 192.168.20.10` (el servidor): tiempo de espera agotado.
4. `tracert 192.168.20.10`: responde 192.168.40.1, después 10.0.0.1, y después todo `*`.
5. El paquete llega a R_TGU. Desde una PC de Tegucigalpa el servidor responde. Entonces la ida llega y la vuelta falla, o el servidor no responde a esa red.
6. En R_TGU, `show ip route 192.168.40.25`: no hay ruta específica, usa la ruta por defecto a internet. Alguien borró la ruta a San Pedro Sula en un cambio de la noche anterior.
7. Arreglo: `ip route 192.168.40.0 255.255.255.0 10.0.0.2` y guardar la configuración.

¿Por qué navegaban? Porque su salida a internet ya no pasa por R_TGU y no necesita esa ruta. Si no hubieras sabido lo del enlace propio, el síntoma "internet sí, sistema no" te habría parecido imposible. Moraleja: la documentación de la red es parte de la red.

### Caso 3. Internet sí, nombres no

Síntoma: una laptop de un gerente abre `8.8.8.8` por ping, pero el navegador dice que no encuentra ninguna página.

1. `ping 8.8.8.8`: responde. Capas 1 a 3 bien, y la salida a internet también.
2. `ping www.ejemplo.hn`: "La solicitud de ping no pudo encontrar el host".
3. `ipconfig /all`: DNS 192.168.1.1. Esa dirección no es de la empresa: el gerente configuró a mano el DNS de su casa.
4. Arreglo: volver la configuración a automática, `ipconfig /renew`, `ipconfig /flushdns`.

### Caso 4. Lentitud en La Ceiba

Síntoma: en La Ceiba "todo está lento" desde la mañana.

1. `ping 192.168.50.1` desde varias PC: 1 ms, sin pérdida. La LAN está bien.
2. `ping -n 50 10.0.0.5` (el otro extremo del enlace con Tegucigalpa): tiempos de 300 ms y 20 % de pérdida. Normalmente son 15 ms sin pérdida.
3. `pathping 192.168.20.10`: la pérdida empieza en el enlace WAN.
4. Conclusión: falla del enlace del proveedor. Se abre un reporte con el proveedor con la evidencia (salidas de ping y pathping con hora), y mientras tanto se puede activar el respaldo por San Pedro Sula si existe (tema 07).

### Caso 5. Dos equipos con la misma IP

Síntoma: la impresora de administración "se cae y vuelve" cada rato. A veces imprime, a veces no.

1. `ping -t 192.168.20.15`: responde casi siempre, pero el tiempo varía y a veces falla.
2. `arp -a` en una PC, varias veces: la MAC de 192.168.20.15 cambia entre dos valores.
3. Hay dos equipos con la misma IP. Uno es la impresora (IP fija) y el otro una PC que se configuró a mano con esa dirección, que además estaba dentro del pool DHCP.
4. Arreglo: corregir la PC y sacar las direcciones fijas del pool DHCP (exclusiones o reservas, tema 08).

## Cómo reportar un problema

Cuando tenés que pasar un caso a otra persona (el proveedor, otro nivel de soporte), un buen reporte ahorra horas:

1. Qué pasa, en una oración, y desde cuándo.
2. A quién le pasa: usuarios, sucursal, red.
3. Qué probaste y qué salió, con las salidas de los comandos y la hora.
4. Qué cambió recientemente, si sabés.
5. Qué descartaste.

## Errores comunes

1. Empezar reiniciando todo sin haber mirado nada. Si se arregla, nunca sabés qué fue y va a volver.
2. Concluir que un equipo está caído porque no responde al ping.
3. Leer un `*` aislado en un `tracert` como una falla.
4. Cambiar varias cosas a la vez.
5. Probar solo la ida y olvidar que la respuesta tiene que volver.
6. No preguntar qué cambió.
7. No anotar la solución.

## Preguntas de repaso

1. ¿Qué preguntas hacés antes de tocar cualquier equipo?
2. Explicá la escalera del ping. ¿Qué te dice que falle el tercer escalón y no el segundo?
3. ¿Qué diferencia hay entre "Tiempo de espera agotado" y "Host de destino inaccesible"?
4. ¿Cómo funciona `tracert`? ¿Por qué aparece `*` en algunos saltos?
5. ¿Qué te dice un TTL=127 en una respuesta de ping?
6. ¿Para qué sirve `Test-NetConnection` cuando ping no funciona?
7. ¿Qué buscás en `ipconfig /all` cuando alguien "no tiene internet"?
8. ¿Qué lleva un buen reporte para el proveedor?

## Fuentes

1. Documentación de comandos de Windows de Microsoft, en español: [ipconfig](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/ipconfig), [ping](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/ping), [tracert](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/tracert), [pathping](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/pathping), [nslookup](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/nslookup), [arp](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/arp) y [netstat](https://learn.microsoft.com/es-es/windows-server/administration/windows-commands/netstat)
2. [RFC 792, ICMP](https://www.rfc-editor.org/rfc/rfc792) (en), los mensajes que usan ping y tracert
3. [RFC 1122](https://www.rfc-editor.org/rfc/rfc1122) (en), sección sobre el TTL
