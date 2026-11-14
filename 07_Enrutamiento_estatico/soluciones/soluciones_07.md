# Tema 07. Soluciones

## Ejercicio 1

C es una red conectada directamente. L es la dirección exacta de la interfaz del router (ruta local), con /32 porque es una sola dirección; le sirve al router para reconocer los paquetes que son para él. S es una ruta estática. S* es una ruta estática que además es la ruta por defecto (candidata a gateway de último recurso).

## Ejercicio 2

```
C    10.0.0.4/30 is directly connected, Serial0/0/0
L    10.0.0.6/32 is directly connected, Serial0/0/0
C    10.0.0.8/30 is directly connected, Serial0/0/1
L    10.0.0.10/32 is directly connected, Serial0/0/1
C    192.168.50.0/24 is directly connected, GigabitEthernet0/0
L    192.168.50.1/32 is directly connected, GigabitEthernet0/0
```

## Ejercicio 3

| Destino | Sale por | Por qué |
|---|---|---|
| 192.168.41.20 | 10.0.0.2 | Coincide con la /22 (de .40.0 a .43.255) |
| 192.168.50.20 | 10.0.0.6 | Coincide con la /24; la /25 cubre de .128 a .255 y .20 no entra |
| 192.168.50.200 | 10.0.0.2 | Coincide con la /24 y con la /25; gana la /25 por ser más larga |
| 192.168.44.1 | 203.0.113.1 | No entra en la /22 (llega a .43.255): solo la ruta por defecto |
| 8.8.4.4 | 203.0.113.1 | Ruta por defecto |

## Ejercicio 4

```
ip route 192.168.40.0 255.255.255.0 10.0.0.2
ip route 192.168.40.0 255.255.255.0 s0/0/0
ip route 192.168.40.0 255.255.255.0 s0/0/0 10.0.0.2
```

En Ethernet, la completa (interfaz y siguiente salto), o la de siguiente salto. La de interfaz sola hace que el router trate cada destino como si estuviera conectado y le pregunte por ARP.

## Ejercicio 5

1. 10.0.0.2 es la propia IP de R_SPS. El siguiente salto es el vecino: 10.0.0.1.
2. 192.168.50.1 tiene bits de host. La red es 192.168.50.0.
3. El siguiente salto está mal: 10.0.0.6 es La Ceiba. Para San Pedro Sula es 10.0.0.2.
4. La máscara de la ruta por defecto es 0.0.0.0. Con 255.255.255.255 sería una ruta a una sola dirección, 0.0.0.0.

## Ejercicio 6

Cuando el router R_SPS hace ping, el paquete sale con origen 10.0.0.2, la IP de su interfaz hacia Tegucigalpa. R_TGU tiene esa red conectada y sabe responder. Cuando hace ping una PC, el origen es 192.168.40.x, y R_TGU no tiene ruta hacia esa red: manda la respuesta por la ruta por defecto a internet y se pierde.

Falta en R_TGU:

```
ip route 192.168.40.0 255.255.255.0 10.0.0.2
```

## Ejercicio 7

R_CHO, de punta:

```
ip route 0.0.0.0 0.0.0.0 10.0.0.13
```

R_SPS necesita saber llegar a Choloma (su ruta por defecto va a Tegucigalpa y no la cubre):

```
ip route 192.168.60.0 255.255.255.0 10.0.0.14
```

R_TGU necesita saber que Choloma está detrás de San Pedro Sula. También conviene la ruta al enlace nuevo, para que los ping desde R_CHO a sí mismo y el diagnóstico funcionen:

```
ip route 192.168.60.0 255.255.255.0 10.0.0.2
ip route 10.0.0.12 255.255.255.252 10.0.0.2
```

R_LCE no cambia: su ruta por defecto ya manda todo a Tegucigalpa.

## Ejercicio 8

En R_SPS, respaldo hacia todo por La Ceiba:

```
ip route 0.0.0.0 0.0.0.0 10.0.0.1
ip route 0.0.0.0 0.0.0.0 10.0.0.10 10
```

En R_TGU, respaldo de vuelta a San Pedro Sula por La Ceiba:

```
ip route 192.168.40.0 255.255.255.0 10.0.0.2
ip route 192.168.40.0 255.255.255.0 10.0.0.6 10
```

En R_LCE, saber llegar a San Pedro Sula por el enlace directo:

```
ip route 192.168.40.0 255.255.255.0 10.0.0.9
```

Esa última ruta tiene un efecto que hay que saber: con ella, el tráfico de La Ceiba a San Pedro Sula va directo por el enlace de respaldo siempre, no por Tegucigalpa. Si se quiere que solo se use cuando falla el principal, también se puede poner flotante en R_LCE (con AD 10) y dejar que el tráfico normal pase por la ruta por defecto hacia Tegucigalpa.

## Ejercicio 9

1. R_TGU no tiene ruta de vuelta a 192.168.50.0/24. El paquete llega al servidor, pero la respuesta se va por la ruta por defecto. Comprobación: `show ip route 192.168.50.30` en R_TGU.
2. El servidor no responde a esa red: tiene un firewall que solo deja ICMP de su red local, o tiene mal el gateway (las PC de Tegucigalpa de la misma VLAN no necesitan gateway para llegarle). Comprobación: `ipconfig` en el servidor y revisar su firewall; probar ping desde una PC de otra VLAN de Tegucigalpa.

El tercer salto no responde porque el servidor no contesta o la respuesta no vuelve; en ninguno de los dos casos se puede saber cuál solo con el `tracert`.

## Ejercicio 10

Respuesta modelo: "Con cinco sucursales y enlaces de respaldo, las rutas estáticas empiezan a pesar: cada sucursal nueva obliga a tocar varios routers, y un respaldo con rutas flotantes no detecta todas las fallas (por ejemplo cuando el enlace del proveedor sigue encendido pero no pasa tráfico). OSPF se ajusta solo si un enlace se cae y no hay que reescribir rutas al crecer. Los riesgos de cambiar son que el equipo de TI necesita aprenderlo, que hay que proteger el protocolo con autenticación para que nadie anuncie rutas falsas, y que un error de configuración se propaga a toda la red. Recomiendo pasar a OSPF entre los routers de las sucursales, con una prueba previa en Packet Tracer y en una ventana de mantenimiento, y mantener la ruta estática por defecto hacia internet."
