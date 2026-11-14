# Laboratorio 02. VLANs y router en un palo en Tegucigalpa

Temas que practica: 06 y 10. Tiempo estimado: 1 hora y media.

Vas a partir la oficina de Tegucigalpa en las VLANs del plan de la empresa y a enrutar entre ellas con un solo cable troncal hacia el router.

## Topología

```
              R_TGU
               | g0/0 (troncal)
               | g0/1
             SW_TGU
   +-----------+-----------+
 Fa0/1 a 2   Fa0/9 a 10  Fa0/15 a 16
 VLAN 10     VLAN 20     VLAN 30
 ventas      admin       bodega
```

## Plan

| VLAN | Nombre | Red | Gateway (subinterfaz) | Puertos | PC |
|---:|---|---|---|---|---|
| 10 | VENTAS | 192.168.10.0/24 | g0/0.10, 192.168.10.1 | Fa0/1 a Fa0/8 | PC_V1 .10.21, PC_V2 .10.22 |
| 20 | ADMINISTRACION | 192.168.20.0/24 | g0/0.20, 192.168.20.1 | Fa0/9 a Fa0/14 | PC_A1 .20.21, SRV01 .20.10 |
| 30 | BODEGA | 192.168.30.0/24 | g0/0.30, 192.168.30.1 | Fa0/15 a Fa0/20 | PC_B1 .30.21, PC_B2 .30.22 |
| 99 | GESTION | 192.168.99.0/24 | g0/0.99, 192.168.99.1 | Ninguno | El switch: 192.168.99.2 |
| 999 | NATIVA_SIN_USO | Sin red | g0/0.999, nativa | Fa0/21 a Fa0/24, apagados | |

SRV01 es un "Server" de Packet Tracer con IP fija. Todas las máscaras son 255.255.255.0.

## Paso 1. Equipos y cables

1. Un router 2911 (R_TGU), un switch 2960 (SW_TGU), cinco PC y un servidor.
2. R_TGU g0/0 a SW_TGU g0/1 con cable directo.
3. PC_V1 a Fa0/1, PC_V2 a Fa0/2, PC_A1 a Fa0/9, SRV01 a Fa0/10, PC_B1 a Fa0/15, PC_B2 a Fa0/16.
4. Configurá IP, máscara y gateway en cada PC y en el servidor según el plan.

## Paso 2. Probar antes de configurar

Desde PC_V1, `ping 192.168.10.22` (la otra PC de ventas) y `ping 192.168.30.21` (bodega). El primero funciona: todos los puertos están todavía en la VLAN 1 y las dos PC están en la misma red. El segundo no, porque son redes distintas y no hay router configurado. Anotá los resultados para compararlos al final.

## Paso 3. VLANs y puertos en el switch

En SW_TGU, CLI:

```
enable
configure terminal
hostname SW_TGU
no ip domain-lookup
vlan 10
 name VENTAS
vlan 20
 name ADMINISTRACION
vlan 30
 name BODEGA
vlan 99
 name GESTION
vlan 999
 name NATIVA_SIN_USO
interface range fa0/1 - 8
 switchport mode access
 switchport access vlan 10
interface range fa0/9 - 14
 switchport mode access
 switchport access vlan 20
interface range fa0/15 - 20
 switchport mode access
 switchport access vlan 30
interface range fa0/21 - 24
 switchport mode access
 switchport access vlan 999
 shutdown
interface g0/1
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30,99
interface g0/2
 shutdown
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
end
copy running-config startup-config
```

Comprobá con `show vlan brief` y `show interfaces trunk`. Puede que el troncal no aparezca como activo hasta que el router esté configurado.

## Paso 4. Subinterfaces en el router

```
enable
configure terminal
hostname R_TGU
no ip domain-lookup
interface g0/0
 no shutdown
interface g0/0.10
 description Gateway VLAN 10 ventas
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface g0/0.20
 description Gateway VLAN 20 administracion
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
interface g0/0.30
 description Gateway VLAN 30 bodega
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
interface g0/0.99
 description Gestion
 encapsulation dot1Q 99
 ip address 192.168.99.1 255.255.255.0
interface g0/0.999
 encapsulation dot1Q 999 native
end
copy running-config startup-config
```

Comprobá con `show ip interface brief` (todas las subinterfaces `up up`) y `show ip route` (cuatro redes C).

## Paso 5. Probar

1. Desde PC_V1: `ping 192.168.10.1`, `ping 192.168.30.1`, `ping 192.168.30.21`, `ping 192.168.20.10`.
2. Desde PC_V1: `tracert 192.168.30.21`. Tiene que mostrar dos saltos: 192.168.10.1 y la PC de bodega.
3. Desde PC_A1: `ping 192.168.99.2` para llegar al switch por la VLAN de gestión.
4. En modo simulación, seguí un ping de PC_V1 a PC_B1 y mirá en el troncal la etiqueta 802.1Q: en "Outbound PDU Details" del switch aparece el campo con el número de VLAN.

## Paso 6. Romperlo a propósito

1. Poné Fa0/2 en la VLAN 30 sin cambiar la IP de PC_V2. ¿Qué le pasa? ¿Llega a su gateway?
2. En el troncal, cambiá la lista permitida a `switchport trunk allowed vlan 10,20,99` (sin `add`). ¿Qué VLAN se queda sin gateway? Volvé a ponerla con `switchport trunk allowed vlan add 30`.
3. Cambiá `encapsulation dot1Q 30` por `encapsulation dot1Q 3` en g0/0.30. ¿Qué pasa con bodega?
4. Apagá g0/0 con `shutdown`. ¿Se cae una VLAN o todas? ¿Por qué?

## Lista de comprobación

1. Cada PC llega a su gateway y a las PC de las otras VLANs.
2. `show vlan brief` coincide con el plan, sin equipos en la VLAN 1.
3. `show interfaces trunk` muestra g0/1 como troncal con nativa 999.
4. Desde administración se llega al switch por 192.168.99.2.
5. Respondiste las cuatro preguntas del paso 6.
6. Guardaste el archivo; lo vas a usar en el laboratorio 03.
