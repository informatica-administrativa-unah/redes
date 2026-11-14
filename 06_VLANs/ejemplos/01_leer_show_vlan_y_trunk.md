# Ejemplo: leer show vlan brief y show interfaces trunk

Así se ven las salidas de SW_TGU cuando el [laboratorio 02](../../laboratorios/lab_02_vlans_y_router_en_un_palo.md) está bien terminado. Compará las tuyas con estas.

## show vlan brief

```
VLAN Name                Status    Ports
1    default             active
10   VENTAS              active    Fa0/1, Fa0/2, Fa0/3, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8
20   ADMINISTRACION      active    Fa0/9, Fa0/10, Fa0/11, Fa0/12, Fa0/13, Fa0/14
30   BODEGA              active    Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20
99   GESTION             active
999  NATIVA_SIN_USO      active    Fa0/21, Fa0/22, Fa0/23, Fa0/24
```

Qué mirar:

1. La VLAN 1 no tiene puertos. Si aparece alguno, quedó sin configurar.
2. La 99 no tiene puertos porque solo la usa la interfaz de gestión del switch.
3. Los puertos troncales (g0/1) no aparecen en esta lista. Eso no es un error.
4. Los puertos apagados siguen apareciendo en su VLAN.

## show interfaces trunk

```
Port        Mode         Encapsulation  Status        Native vlan
Gig0/1      on           802.1q         trunking      999

Port        Vlans allowed on trunk
Gig0/1      10,20,30,99

Port        Vlans allowed and active in management domain
Gig0/1      10,20,30,99

Port        Vlans in spanning tree forwarding state and not pruned
Gig0/1      10,20,30,99
```

Qué mirar:

1. Status `trunking`: el troncal está formado.
2. Native vlan 999 en las dos puntas.
3. La lista permitida tiene todas las VLANs que necesitan llegar al router. Si falta una, sus equipos no llegan al gateway.
4. Si una VLAN está permitida pero no aparece en "allowed and active", no existe en este switch: hay que crearla.
