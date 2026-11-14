# Tema 10. Soluciones

## Ejercicio 1

| Pregunta | Comando |
|---|---|
| ¿Qué DNS tiene la PC? | `ipconfig /all` |
| ¿Por dónde pasa el tráfico? | `tracert` |
| ¿Responde el puerto 443? | `Test-NetConnection 192.168.20.10 -Port 443` |
| ¿Qué MAC tiene el gateway? | `arp -a` |
| ¿A qué IP resuelve un nombre? | `nslookup` |
| ¿Qué puertos escucha esta PC? | `netstat -ano` |

## Ejercicio 2

1. Llegó y volvió en 3 ms. TTL=127 indica que la respuesta salió de un equipo Windows (128) y cruzó un router.
2. No volvió respuesta. Puede ser que no llegue, que la respuesta no vuelva o que un firewall bloquee ICMP.
3. El router 10.0.0.1 (R_TGU) recibió el paquete pero no sabe cómo llegar al destino, o nadie contestó al ARP en la red final.
4. El paquete se quedó dando vueltas hasta que se le acabó el TTL, y 10.0.0.2 fue quien lo descartó. Hay un bucle de rutas.

## Ejercicio 3

Capa 1. Revisar que el cable esté conectado en las dos puntas, cambiar el cable por uno que funcione y probar otro puerto del switch (o ver si el puerto está apagado con `shutdown` en el switch). Si es una laptop, también que la tarjeta no esté desactivada.

## Ejercicio 4

1. `ping 127.0.0.1`
2. `ping 192.168.50.30`
3. `ping 192.168.50.1` (gateway de La Ceiba)
4. `ping 10.0.0.5` (R_TGU por el enlace)
5. `ping 192.168.20.1` (gateway de la VLAN del servidor)
6. `ping 192.168.20.10` (el servidor)
7. `ping ventas.interno.guayabo.example` (por nombre)

En este caso los escalones intermedios son internos porque el destino es interno. Para internet se sigue con el router del proveedor y una dirección externa.

## Ejercicio 5

Bucle de rutas entre R_TGU (10.0.0.5) y R_LCE (10.0.0.6): el paquete va y vuelve entre los dos hasta que se acabe el TTL. Probablemente R_TGU manda el destino a La Ceiba y R_LCE lo devuelve por su ruta por defecto. Buscar con `show ip route` en los dos routers qué entrada usan para el destino; normalmente una ruta estática mal escrita en R_TGU (red equivocada o siguiente salto equivocado).

## Ejercicio 6

No hay problema de red: el servidor bloquea ICMP (es común en Windows Server). Para comprobar el servicio: `Test-NetConnection 192.168.20.10 -Port 443` debe decir `TcpTestSucceeded : True`. También abrir el sistema y mirar con `netstat -ano` en el servidor que el puerto está en escucha.

## Ejercicio 7

1. `ping -t 8.8.8.8` en una ventana y `ping -t 192.168.50.1` en otra, durante una hora. Si el ping al gateway nunca falla y el de internet sí, la falla está fuera de la LAN.
2. Para guardar la evidencia con hora, en PowerShell: `Test-Connection 8.8.8.8 -Count 3600 | Select-Object Status, Latency` exportado a un archivo, o `ping -n 3600 8.8.8.8 > ping.txt` anotando la hora de inicio.
3. `pathping 8.8.8.8` en uno de los momentos malos para ver en qué salto empieza la pérdida.
4. Al proveedor: período medido, porcentaje de pérdida, latencia normal y en los picos, en qué salto empieza el problema, y la prueba de que la LAN está bien (ping al gateway sin pérdida).

## Ejercicio 8

1. Preguntar exactamente qué cambió a las 7:50 y tener a mano la configuración anterior si existe.
2. En el switch: `show vlan brief` para ver que la VLAN 30 existe y tiene sus puertos; `show interfaces trunk` para ver que el troncal está activo y que la VLAN 30 está permitida; `show running-config` y compararla con la copia anterior.
3. En el router: `show ip interface brief` para ver que la subinterfaz g0/0.30 está up; `show running-config interface g0/0.30` para el `encapsulation dot1Q 30`.
4. Desde una PC de bodega: `ipconfig` (si tiene 169.254, no llega al DHCP: VLAN o troncal), y ping al gateway 192.168.30.1.
5. Lo más probable, por el horario: el cambio quitó la VLAN 30 de la lista permitida del troncal (por ejemplo un `switchport trunk allowed vlan` sin `add`), o borró la VLAN.
6. Al corregir, guardar y anotar en la bitácora qué pasó.

## Ejercicio 9

Reporte modelo:

1. Qué pasa: desde las 8:10 del martes, el enlace entre nuestra sucursal de La Ceiba y Tegucigalpa tiene pérdida de paquetes y latencia alta.
2. A quién: toda la sucursal de La Ceiba, unos 25 equipos.
3. Qué probamos: a las 9:00, 50 pings a 10.0.0.5 (extremo de Tegucigalpa): 20 % de pérdida, latencia promedio 310 ms (lo normal es 15 ms y 0 %). Ping a la LAN local 192.168.50.1: 1 ms, 0 % de pérdida. `pathping` a las 9:10 muestra que la pérdida empieza en el primer salto del enlace. Adjuntamos las salidas.
4. Qué cambió: nada de nuestro lado desde la semana pasada.
5. Qué descartamos: LAN de La Ceiba, router R_LCE (sin errores en la interfaz LAN, CPU normal) y el lado de Tegucigalpa (sin problemas con San Pedro Sula).

## Ejercicio 10

Hoja modelo:

1. Preguntá qué no funciona exactamente, desde cuándo y qué cambió.
2. Preguntá si les pasa a otros. Si es a varios, avisá a TI de redes y seguí con un equipo afectado.
3. `ipconfig`: si dice medios desconectados, revisá cable o wifi.
4. Si la IP es 169.254: probá `ipconfig /renew`; si sigue, revisá el puerto y la VLAN o escalá.
5. Si la IP o el gateway no son de la oficina: configuración a mano o DHCP falso; poné la tarjeta en automático.
6. `ping` al gateway. Si falla: cable, puerto o VLAN.
7. `ping 192.168.20.10`. Si falla y el gateway responde: escalá a redes con la salida de `tracert`.
8. `ping 8.8.8.8`. Si falla y lo interno anda: problema de salida a internet; escalá.
9. `ping` a un sitio por nombre. Si falla y el 8.8.8.8 anda: DNS; revisá `ipconfig /all` y `ipconfig /flushdns`.
10. Si todo responde y el programa no abre: es el programa o el servidor; escalá a sistemas. Anotá siempre lo que hiciste y el resultado.
