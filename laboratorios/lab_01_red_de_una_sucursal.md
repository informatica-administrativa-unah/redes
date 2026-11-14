# Laboratorio 01. La red de una sucursal

Temas que practica: 01, 02 y 10. Tiempo estimado: 1 hora.

Vas a armar la red de la sucursal de La Ceiba de Comercial El Guayabo: un router, un switch, tres PC y una impresora, con direcciones fijas. Al final vas a seguir un paquete en modo simulación.

## Lo que necesitás

Cisco Packet Tracer, que es gratis con una cuenta de NetAcad: [descarga en NetAcad](https://www.netacad.com/cisco-packet-tracer). Las guías se probaron pensando en la versión 8; los nombres de los modelos pueden cambiar un poco en otras versiones.

## Plan de direcciones

| Equipo | Interfaz | Dirección | Máscara | Gateway |
|---|---|---|---|---|
| R_LCE | g0/0 | 192.168.50.1 | 255.255.255.0 | No aplica |
| PC_CAJA1 | Fa0 | 192.168.50.21 | 255.255.255.0 | 192.168.50.1 |
| PC_CAJA2 | Fa0 | 192.168.50.22 | 255.255.255.0 | 192.168.50.1 |
| PC_BODEGA | Fa0 | 192.168.50.23 | 255.255.255.0 | 192.168.50.1 |
| IMPRESORA | Fa0 | 192.168.50.10 | 255.255.255.0 | 192.168.50.1 |

## Paso 1. Poner los equipos

1. Abajo a la izquierda, en "Network Devices", elegí "Routers" y arrastrá un 2911 al área de trabajo.
2. En "Switches", arrastrá un 2960.
3. En "End Devices", arrastrá tres PC y una impresora.
4. Hacé clic en cada equipo, pestaña "Config", y cambiá el "Display Name" por el de la tabla.

## Paso 2. Cablear

1. En "Connections" (el ícono del rayo) elegí "Copper Straight Through".
2. Router g0/0 al switch g0/1.
3. Cada PC y la impresora a un puerto Fa del switch: PC_CAJA1 a Fa0/1, PC_CAJA2 a Fa0/2, PC_BODEGA a Fa0/3, IMPRESORA a Fa0/10.
4. Los puntos del cable quedan rojos o naranjas un rato. En el router van a seguir rojos hasta que enciendas la interfaz.

## Paso 3. Configurar el router

Hacé clic en R_LCE, pestaña "CLI". Si pregunta por el diálogo de configuración inicial, respondé `no`.

```
enable
configure terminal
hostname R_LCE
no ip domain-lookup
interface g0/0
 description LAN La Ceiba
 ip address 192.168.50.1 255.255.255.0
 no shutdown
end
copy running-config startup-config
```

1. `no ip domain-lookup` evita que el router se quede trabado intentando resolver como nombre cualquier palabra mal escrita.
2. `description` no cambia nada técnico, pero documenta.
3. `copy running-config startup-config` guarda. Si no, al apagar se pierde.

Comprobá con `show ip interface brief`: g0/0 tiene que decir `up up`.

## Paso 4. Configurar las PC y la impresora

En cada PC: pestaña "Desktop", "IP Configuration", opción "Static", y escribí IP, máscara y gateway de la tabla. En la impresora es en "Config", "FastEthernet0".

## Paso 5. Probar

Desde PC_CAJA1, "Desktop", "Command Prompt":

1. `ipconfig`: comprobá que la configuración es la que pusiste.
2. `ping 192.168.50.1`: el gateway. El primer ping puede fallar mientras se resuelve el ARP; los demás tienen que responder.
3. `ping 192.168.50.22` y `ping 192.168.50.10`: otra PC y la impresora.
4. `arp -a`: ahora aparecen las MAC de los equipos a los que hiciste ping.

## Paso 6. Seguir un paquete

Seguí el [ejemplo del tema 01](../01_Modelo_OSI_y_TCP_IP/ejemplos/01_seguir_un_paquete.md): modo "Simulation", filtros ICMP y ARP, ping de PC_CAJA1 a PC_BODEGA, y mirá las capas en cada equipo.

## Paso 7. Romperlo a propósito

Estas pruebas te enseñan más que la configuración. Hacé una a la vez y volvé todo a como estaba después de cada una:

1. Cambiá la máscara de PC_CAJA2 a 255.255.255.128. ¿Llega al gateway? ¿Por qué sí o por qué no? (Pista: hacé la cuenta del AND.)
2. Cambiá la IP de PC_CAJA2 a 192.168.50.200 con máscara 255.255.255.128. ¿Ahora llega? ¿Llega al gateway?
3. Poné en PC_BODEGA el gateway 192.168.51.1. ¿Le hace ping a las otras PC? ¿Por qué eso sí funciona?
4. En el router, `interface g0/0` y `shutdown`. ¿Qué le pasa al ping al gateway? ¿Y entre PC?
5. Poné a PC_CAJA2 la misma IP que PC_CAJA1. ¿Qué te avisa Packet Tracer?

## Lista de comprobación

1. Todas las PC hacen ping al gateway y entre ellas.
2. `show ip interface brief` en el router muestra g0/0 `up up` con 192.168.50.1.
3. Guardaste la configuración del router.
4. Contestaste las cinco preguntas del paso 7 en tu cuaderno.

Guardá el archivo como `lab01_tu_nombre.pkt` en tu compu. Los archivos `.pkt` no se suben al repo.
