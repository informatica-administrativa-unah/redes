# Ejemplo: seguir un paquete en Packet Tracer

Este ejemplo te deja ver con tus propios ojos el encapsulamiento del tema. Usá la red del [laboratorio 01](../../laboratorios/lab_01_red_de_una_sucursal.md) o armá una mínima: dos PC, un switch y un router.

## Modo simulación

1. Abajo a la derecha de Packet Tracer cambiá de "Realtime" a "Simulation".
2. En "Edit Filters" dejá marcados solo ICMP y ARP, así no te distrae otro tráfico.
3. Desde una PC, en "Desktop" y luego "Command Prompt", escribí `ping 192.168.10.1`.
4. Dale a "Capture / Forward" una vez por paso. Vas a ver un sobrecito moverse por la red.
5. Hacé clic en el sobre: Packet Tracer te muestra las capas OSI de entrada y de salida en ese equipo.

## Qué fijarte

1. El primer sobre que sale no es el ping, es un ARP. La PC todavía no conoce la MAC del destino.
2. El ARP sale con MAC de destino `FFFF.FFFF.FFFF` (broadcast) y el switch lo manda por todos sus puertos.
3. Cuando llega la respuesta ARP, recién sale el ICMP.
4. Si hacés ping a una PC de otra red, mirá las MAC del paquete antes y después del router: cambian. Las IP no.
5. En la pestaña "Inbound PDU Details" están los encabezados con todos sus campos, igual que en Wireshark.

## Para practicar

1. Hacé el mismo ping dos veces seguidas. ¿Por qué la segunda vez no aparece ARP? (La PC guardó la MAC en su tabla ARP.)
2. Desconectá el cable de una PC y repetí. ¿En qué equipo se queda el sobre y qué capa falló?
