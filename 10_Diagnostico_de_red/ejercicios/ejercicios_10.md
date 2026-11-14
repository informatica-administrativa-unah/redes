# Tema 10. Ejercicios

Para cada caso no basta con la respuesta: escribí qué comando correrías y qué esperarías ver.

## Ejercicio 1

Asociá cada pregunta con el comando que la contesta: ¿qué DNS tiene la PC?, ¿por dónde pasa el tráfico hasta un servidor?, ¿responde el puerto 443 del servidor?, ¿qué MAC tiene el gateway?, ¿a qué IP resuelve un nombre?, ¿qué puertos está escuchando esta PC? Comandos: `nslookup`, `arp -a`, `ipconfig /all`, `tracert`, `Test-NetConnection`, `netstat -ano`.

## Ejercicio 2

Explicá qué significa cada respuesta de ping:

1. "Respuesta desde 192.168.20.10: bytes=32 tiempo=3ms TTL=127"
2. "Tiempo de espera agotado para esta solicitud."
3. "Respuesta desde 10.0.0.1: Host de destino inaccesible."
4. "Respuesta desde 10.0.0.2: TTL expiró en tránsito."

## Ejercicio 3

Una PC muestra en `ipconfig`: "Adaptador de Ethernet: Estado de los medios: medios desconectados". ¿En qué capa está el problema y qué tres cosas revisás?

## Ejercicio 4

Hacé la escalera del ping para una PC de La Ceiba (192.168.50.30) que no llega al servidor 192.168.20.10. Escribí los siete escalones con las direcciones concretas de la empresa.

## Ejercicio 5

Interpretá este `tracert` desde una PC de La Ceiba:

```
  1     1 ms     1 ms     1 ms  192.168.50.1
  2    13 ms    12 ms    12 ms  10.0.0.5
  3    13 ms    13 ms    12 ms  10.0.0.6
  4    25 ms    24 ms    25 ms  10.0.0.5
  5    25 ms    26 ms    25 ms  10.0.0.6
```

¿Qué pasa y dónde buscás?

## Ejercicio 6

El servidor 192.168.20.10 no responde a ping desde ninguna PC, pero el sistema de ventas abre bien en todas. ¿Hay un problema de red? ¿Cómo comprobás que el servicio responde sin usar ping?

## Ejercicio 7

Un usuario dice que "el internet se cae cada rato". Proponé cómo medirlo durante una hora con herramientas de Windows y cómo presentarle la evidencia al proveedor.

## Ejercicio 8

Toda la VLAN de bodega de Tegucigalpa se quedó sin red a las 8:05 de la mañana. Las otras VLAN funcionan. A las 7:50 un técnico hizo un cambio en el switch. Escribí el plan de diagnóstico, con comandos del switch y del router, y lo que buscarías en cada uno.

## Ejercicio 9

Escribí el reporte para el proveedor del caso 4 del tema (lentitud en La Ceiba) siguiendo los cinco puntos de "cómo reportar un problema". Inventá horas y valores coherentes.

## Ejercicio 10

Armá una hoja de una página para la oficina de soporte de Comercial El Guayabo: los diez pasos que tiene que seguir alguien nuevo cuando le dicen "no hay internet", en orden, con el comando de cada paso y qué hacer según el resultado.
