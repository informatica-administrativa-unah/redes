# Tema 01. Ejercicios

Respondé en tu cuaderno o en una copia de este archivo. Van de más fácil a más difícil. Las soluciones están en `../soluciones/soluciones_01.md`, pero intentalo primero.

## Ejercicio 1

Ordená estas capas OSI de abajo hacia arriba: transporte, física, aplicación, red, sesión, enlace de datos, presentación.

## Ejercicio 2

¿En qué capa OSI trabaja cada uno? Cable UTP, switch, router, ARP, HTTP, TCP, dirección MAC, dirección IP, fibra óptica, TLS.

## Ejercicio 3

Para cada servicio, decí si usa TCP o UDP y en qué puerto escucha normalmente: HTTPS, DNS (consulta normal), SSH, DHCP del lado del servidor, SMTP, escritorio remoto de Windows.

## Ejercicio 4

Completá la tabla con el nombre de la unidad de datos en cada capa: aplicación, transporte con TCP, red, enlace, física.

## Ejercicio 5

Explicá con tus palabras por qué una videollamada entre gerencia en Tegucigalpa y la sucursal de La Ceiba usa UDP, pero el envío de la planilla al banco usa TCP.

## Ejercicio 6

Relacioná cada capa de TCP/IP con las de OSI que cubre. Después explicá por qué TCP/IP junta en una sola las capas 5, 6 y 7.

## Ejercicio 7

Una cajera de La Ceiba (192.168.50.30, gateway 192.168.50.1) abre una página del servidor web interno 192.168.20.10 en Tegucigalpa. Contestá:

1. ¿A qué MAC de destino manda la PC la primera trama?
2. ¿Cuál es la IP de destino del paquete en ese momento?
3. Cuando el paquete sale del router de Tegucigalpa hacia el servidor, ¿cuál es la IP de origen y cuál la MAC de origen de la trama?

## Ejercicio 8

Para cada síntoma, decí en qué capa empezarías a buscar y qué revisarías primero:

1. La PC dice "cable de red desconectado".
2. La PC tiene IP, hace ping al servidor por IP, pero no abre `ventas.interno.guayabo.example`.
3. Dos PC conectadas al mismo switch no se ven, y cada una tiene IP de una red distinta.
4. Todo funciona, pero el sistema de inventario no abre y los demás programas sí.

## Ejercicio 9

Dibujá el encapsulamiento de una consulta DNS que hace una PC: qué encabezados lleva, en qué orden y qué dato importante va en cada uno (puertos, IP, MAC).

## Ejercicio 10

En la bodega de San Pedro Sula hay un hub viejo de 8 puertos con 6 PC conectadas. El encargado se queja de que la red "se pone lenta cuando todos trabajan". Explicá qué pasa por la forma en que trabaja un hub, qué equipo pondrías en su lugar y por qué eso mejora la situación.
