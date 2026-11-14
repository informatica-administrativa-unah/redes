# Tema 01. Soluciones

Hay más de una forma correcta de explicar varios de estos. Si tu respuesta dice lo mismo con otras palabras, está bien.

## Ejercicio 1

Física, enlace de datos, red, transporte, sesión, presentación, aplicación.

## Ejercicio 2

| Elemento | Capa |
|---|---|
| Cable UTP | 1, física |
| Switch | 2, enlace de datos |
| Router | 3, red |
| ARP | 2, enlace (une la capa 2 con la 3: traduce IP a MAC) |
| HTTP | 7, aplicación |
| TCP | 4, transporte |
| Dirección MAC | 2, enlace de datos |
| Dirección IP | 3, red |
| Fibra óptica | 1, física |
| TLS | 6, presentación (en TCP/IP queda dentro de aplicación) |

## Ejercicio 3

| Servicio | Protocolo | Puerto |
|---|---|---|
| HTTPS | TCP | 443 |
| DNS, consulta normal | UDP | 53 (usa TCP 53 para respuestas grandes y transferencias de zona) |
| SSH | TCP | 22 |
| DHCP, servidor | UDP | 67 (el cliente usa el 68) |
| SMTP | TCP | 25 (587 para que los clientes manden correo) |
| Escritorio remoto | TCP | 3389 |

## Ejercicio 4

Aplicación: datos. Transporte con TCP: segmento (con UDP se dice datagrama). Red: paquete. Enlace: trama. Física: bits.

## Ejercicio 5

En una videollamada un pedazo de audio o imagen que llega tarde ya no sirve: si TCP lo reenviara, la llamada se trabaría esperando. Es preferible perder unos milisegundos de imagen y seguir. La planilla, en cambio, no puede llegar con una fila menos ni con números cambiados; TCP confirma cada parte, reenvía lo perdido y entrega en orden, y eso vale más que la rapidez.

## Ejercicio 6

| TCP/IP | OSI |
|---|---|
| Aplicación | 7, 6 y 5 |
| Transporte | 4 |
| Internet | 3 |
| Acceso a la red | 2 y 1 |

Las junta porque en la práctica las hace el mismo programa: el navegador maneja la sesión, el formato y el protocolo HTTP. Separarlas en el diseño de TCP/IP no aportaba nada.

## Ejercicio 7

1. A la MAC del gateway, 192.168.50.1 (el router de La Ceiba). El servidor está en otra red, así que la trama va al router.
2. 192.168.20.10, la del servidor. La IP de destino no cambia en el camino.
3. IP de origen: 192.168.50.30, la de la cajera (no hay NAT entre sucursales). MAC de origen: la de la interfaz del router de Tegucigalpa que da a la red del servidor. En cada salto la trama se arma de nuevo.

## Ejercicio 8

1. Capa 1. Cable conectado y ponchado, puerto del switch con luz, probar otro cable u otro puerto.
2. Capa 7, DNS. La red funciona hasta la capa 3 porque el ping por IP responde. Revisá qué servidor DNS tiene la PC (`ipconfig /all`) y probá `nslookup ventas.interno.guayabo.example`.
3. Capa 3. Están en el mismo switch (la capa 2 está bien), pero en redes distintas: sin un router de por medio no se pueden hablar. Hay que corregir la IP o la máscara de una de ellas.
4. Capas 4 a 7 del lado del servidor o del programa: que el servicio esté corriendo, que el puerto esté abierto y que ningún firewall lo bloquee.

## Ejercicio 9

```
[ Ethernet: MAC destino = gateway o servidor DNS local, MAC origen = PC ]
  [ IP: origen = IP de la PC, destino = IP del servidor DNS ]
    [ UDP: puerto origen al azar (por ejemplo 53211), puerto destino 53 ]
      [ DNS: "¿cuál es la IP de ventas.interno.guayabo.example?" ]
[ FCS al final de la trama ]
```

Si el servidor DNS está en la misma red de la PC, la MAC de destino es la del servidor; si está en otra red, es la del gateway.

## Ejercicio 10

Un hub repite cada señal por todos sus puertos. Todas las PC comparten el mismo medio: si dos transmiten a la vez, chocan (colisión), las dos esperan y vuelven a intentar. Con seis PC trabajando, las colisiones se multiplican y todo se vuelve lento. Además cualquier PC recibe el tráfico de las demás.

Lo correcto es cambiarlo por un switch. El switch aprende qué MAC está en cada puerto y manda cada trama solo por el puerto del destino. Cada puerto es su propio dominio de colisión y trabaja en dúplex completo (enviar y recibir a la vez), así que las colisiones desaparecen y cada PC tiene su propio ancho de banda hacia el switch.
