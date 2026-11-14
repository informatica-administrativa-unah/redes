# Ejemplo: la configuración de NAT de R_TGU, comentada

Es la del [laboratorio 04](../../laboratorios/lab_04_dhcp_dns_y_nat.md), con un comentario por línea. En Cisco, una línea que empieza con `!` es un comentario.

```
! Lo que da hacia adentro: las tres VLAN de usuarios y los enlaces a las sucursales
interface g0/0.10
 ip nat inside
interface g0/0.20
 ip nat inside
interface g0/0.30
 ip nat inside
interface s0/0/0
 ip nat inside
interface s0/0/1
 ip nat inside
!
! Lo que da hacia el proveedor
interface g0/1
 ip address 203.0.113.2 255.255.255.252
 ip nat outside
!
! Qué se traduce: todo 192.168.0.0/16 (todas las LAN de la empresa)
access-list 1 permit 192.168.0.0 0.0.255.255
!
! PAT: todo lo de la lista 1 sale con la IP de g0/1
ip nat inside source list 1 interface g0/1 overload
!
! El catálogo: lo que llega a la pública por TCP 80 va al servidor interno
ip nat inside source static tcp 192.168.20.30 80 interface g0/1 80
!
! Sin esto no sale nada a internet
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

## show ip nat statistics, bien configurado

```
Total translations: 4 (1 static, 3 dynamic, 3 extended)
Outside Interfaces: GigabitEthernet0/1
Inside Interfaces: GigabitEthernet0/0.10 , GigabitEthernet0/0.20 , GigabitEthernet0/0.30 , Serial0/0/0 , Serial0/0/1
Hits: 120  Misses: 8
```

Si en "Inside Interfaces" falta alguna, esa red no navega. Si "Hits" no sube mientras una PC intenta salir, la lista de acceso no la cubre o el tráfico no está llegando al router.
