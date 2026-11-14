# Laboratorio 04. DHCP, DNS y salida a internet con NAT

Temas que practica: 08, 09 y 10. Tiempo estimado: 2 horas.

Partís del laboratorio 03. Vas a centralizar DHCP y DNS en el servidor de Tegucigalpa, agregar un "internet" de práctica y dar salida con PAT. Al final publicás el catálogo web.

## Lo que se agrega

| Equipo | Dirección | Qué hace |
|---|---|---|
| SRV01 (ya existe) | 192.168.20.10 | DHCP para todas las LAN y DNS interno |
| SRV_CATALOGO, nuevo, en la VLAN 20 | 192.168.20.30 | Servidor web interno que se va a publicar |
| ISP, router 2911 nuevo | g0/0 203.0.113.1/30 hacia R_TGU, g0/1 198.51.100.1/24 | El proveedor |
| WEB_EXTERNA, servidor nuevo | 198.51.100.80/24, gateway 198.51.100.1 | Un sitio "de internet" |
| PC_CASA, PC nueva | 198.51.100.50/24, gateway 198.51.100.1 | Un cliente desde su casa |

R_TGU usa su g0/1 hacia el ISP con 203.0.113.2/30. Todas estas direcciones son de documentación (RFC 5737): no existen en internet.

## Paso 1. DHCP en SRV01

En SRV01, "Services", "DHCP". Encendé el servicio y creá un pool por red (botón "Add"):

| Nombre del pool | Gateway | DNS | Primera IP | Máscara | Máximo de usuarios |
|---|---|---|---|---|---:|
| VENTAS | 192.168.10.1 | 192.168.20.10 | 192.168.10.21 | 255.255.255.0 | 200 |
| BODEGA | 192.168.30.1 | 192.168.20.10 | 192.168.30.21 | 255.255.255.0 | 200 |
| SPS | 192.168.40.1 | 192.168.20.10 | 192.168.40.21 | 255.255.255.0 | 200 |
| LCE | 192.168.50.1 | 192.168.20.10 | 192.168.50.21 | 255.255.255.0 | 200 |

Empezar en .21 deja las primeras 20 de cada red para equipos fijos. El pool de la propia VLAN 20 lo podés crear también si querés PC de administración con DHCP; el servidor sigue con IP fija.

## Paso 2. Agentes de retransmisión

El servidor está en la VLAN 20. Las demás redes necesitan `ip helper-address` en su gateway:

R_TGU:

```
interface g0/0.10
 ip helper-address 192.168.20.10
interface g0/0.30
 ip helper-address 192.168.20.10
```

R_SPS y R_LCE, en su g0/0:

```
interface g0/0
 ip helper-address 192.168.20.10
```

Cambiá todas las PC (menos SRV01 y SRV_CATALOGO) a DHCP en "IP Configuration". Cada una tiene que recibir una dirección de su red, desde .21. Si alguna recibe 169.254, revisá su VLAN, el helper y que el servidor tenga ruta de vuelta (su gateway es R_TGU, que conoce todas las redes desde el laboratorio 03).

## Paso 3. DNS en SRV01

En SRV01, "Services", "DNS". Encendé el servicio y agregá registros tipo "A Record":

| Nombre | Dirección |
|---|---|
| srv01.interno.guayabo.example | 192.168.20.10 |
| ventas.interno.guayabo.example | 192.168.20.10 |
| catalogo.guayabo.example | 192.168.20.30 |
| www.ejemplo.example | 198.51.100.80 |

El último simula un sitio de internet. En la vida real el DNS interno lo resolvería preguntando a otros servidores; en Packet Tracer lo cargamos a mano.

Probá desde PC_SPS: `nslookup ventas.interno.guayabo.example` y `ping ventas.interno.guayabo.example`.

## Paso 4. El proveedor

ISP:

```
hostname ISP
interface g0/0
 ip address 203.0.113.1 255.255.255.252
 no shutdown
interface g0/1
 ip address 198.51.100.1 255.255.255.0
 no shutdown
```

Fijate que ISP no tiene ninguna ruta hacia las redes 192.168.x.x de la empresa. Así se comporta internet: no enruta direcciones privadas.

R_TGU:

```
interface g0/1
 description Enlace al proveedor
 ip address 203.0.113.2 255.255.255.252
 no shutdown
ip route 0.0.0.0 0.0.0.0 203.0.113.1
```

Probá desde PC_V1: `ping 198.51.100.80`. Falla. Desde R_TGU, `ping 198.51.100.80`: funciona, porque el router sale con su IP pública 203.0.113.2. La diferencia es justamente lo que resuelve NAT.

## Paso 5. PAT

R_TGU:

```
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
interface g0/1
 ip nat outside
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface g0/1 overload
```

Probá desde PC_V1, PC_SPS y PC_LCE: `ping 198.51.100.80` y, en "Web Browser", `http://www.ejemplo.example`. Después, en R_TGU, `show ip nat translations`: vas a ver cada conversación con su puerto.

## Paso 6. Publicar el catálogo

En SRV_CATALOGO, "Services", "HTTP": dejá el servicio encendido y cambiá el texto de `index.html` para reconocerlo ("Catálogo de Comercial El Guayabo").

R_TGU:

```
ip nat inside source static tcp 192.168.20.30 80 interface g0/1 80
```

Desde PC_CASA, navegador: `http://203.0.113.2`. Tiene que aparecer el catálogo. PC_CASA no sabe nada de 192.168.20.30.

## Paso 7. Romperlo a propósito

1. Quitá `ip nat inside` de s0/0/0. ¿Quién deja de navegar?
2. Cambiá la lista de acceso a `access-list 1 permit 192.168.10.0 0.0.0.255` (borrá la anterior con `no access-list 1` primero). ¿Quién navega ahora?
3. Apagá el servicio DNS de SRV01. ¿Qué funciona y qué no? Probá por nombre y por IP.
4. Quitá el `ip helper-address` de R_LCE y renová la IP de PC_LCE con `ipconfig /release` y `ipconfig /renew`. ¿Qué dirección recibe?

## Lista de comprobación

1. Todas las PC reciben dirección por DHCP desde SRV01, cada una en su red.
2. Los nombres internos resuelven desde las tres sucursales.
3. Todas las sucursales navegan a `www.ejemplo.example` y `show ip nat translations` lo muestra.
4. PC_CASA ve el catálogo por 203.0.113.2.
5. Contestaste las cuatro preguntas del paso 7.

Con esto tenés la red completa de la empresa del curso. Si querés más: agregá IPv6 con el plan del tema 05, o reemplazá las rutas estáticas por OSPF y compará.
