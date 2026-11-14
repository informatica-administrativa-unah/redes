# 06. VLANs

En el tema 03 partimos la red de Tegucigalpa en ventas, administración y bodega. Pero en la oficina hay un solo switch de 24 puertos, y en el mismo piso se sientan cajeras, contadores y el encargado de bodega. ¿Compramos tres switches, uno por departamento, y tiramos cables separados? Con VLANs no hace falta: un solo switch se parte en varios switches lógicos, y cada uno es una red aparte.

## Qué es una VLAN

Una VLAN (red de área local virtual) es un grupo de puertos de uno o varios switches que se comportan como si estuvieran en su propio switch. Lo que se manda en una VLAN no llega a las demás: cada VLAN es su propio dominio de broadcast.

Lo que eso significa en la práctica:

1. Cada VLAN es una red IP distinta (en este curso, una subred por VLAN).
2. Dos equipos en VLANs distintas no se hablan directamente aunque estén en el mismo switch. Para comunicarse necesitan un router o un switch de capa 3, igual que si estuvieran en edificios distintos.
3. Mover a una persona de departamento es cambiar la VLAN de su puerto con un comando, sin tocar cables.

### Por qué usarlas

1. Menos broadcast: el ARP de la bodega no les llega a las cajas.
2. Seguridad: el tráfico entre VLANs pasa por un router o firewall donde se pueden poner reglas. Una PC de ventas no ve directamente el servidor de planilla.
3. Orden y flexibilidad: la red se organiza por función, no por dónde está el cable.
4. Costo: un switch con VLANs reemplaza varios switches.

Ojo con la idea de seguridad: una VLAN separa, pero no es un firewall. Si el router entre VLANs deja pasar todo, la separación sirve de poco. Las reglas entre VLANs (listas de acceso o firewall) son las que protegen.

## Plan de VLANs de Comercial El Guayabo en Tegucigalpa

| VLAN | Nombre | Red IPv4 | Gateway | Puertos del switch SW_TGU |
|---:|---|---|---|---|
| 10 | VENTAS | 192.168.10.0/24 | 192.168.10.1 | Fa0/1 a Fa0/8 |
| 20 | ADMINISTRACION | 192.168.20.0/24 | 192.168.20.1 | Fa0/9 a Fa0/14 |
| 30 | BODEGA | 192.168.30.0/24 | 192.168.30.1 | Fa0/15 a Fa0/20 |
| 99 | GESTION | 192.168.99.0/24 | 192.168.99.1 | Ninguno, es para administrar el switch |
| 999 | NATIVA_SIN_USO | Sin red | Sin gateway | Ninguno, solo como VLAN nativa del troncal |

Fijate que el número de VLAN coincide con el tercer octeto. No es obligatorio, pero ayuda a que cualquiera lea la red sin tabla.

## Puertos de acceso y puertos troncales

Un puerto de switch puede ser de dos tipos:

1. Acceso: pertenece a una sola VLAN. Ahí se conectan PC, impresoras, cámaras. El equipo no sabe nada de VLANs: manda tramas normales y el switch sabe de qué VLAN son por el puerto.
2. Troncal (trunk): lleva el tráfico de varias VLANs por un solo cable. Se usa entre switches y entre un switch y un router. Para que el otro extremo sepa de qué VLAN es cada trama, el switch le pone una etiqueta.

### La etiqueta 802.1Q

El estándar IEEE 802.1Q mete 4 bytes dentro de la trama Ethernet, entre la MAC de origen y el campo de tipo. Lo más importante de esos 4 bytes es el identificador de VLAN, de 12 bits: por eso las VLAN van del 1 al 4094 (el 0 y el 4095 están reservados).

```
Trama normal:    | MAC destino | MAC origen | Tipo | Datos | FCS |
Trama etiquetada:| MAC destino | MAC origen | 802.1Q (VLAN 20) | Tipo | Datos | FCS |
```

Cuando la trama sale por un puerto de acceso, el switch le quita la etiqueta. Las PC nunca ven etiquetas.

### La VLAN nativa

En un troncal, el tráfico de una VLAN especial, la nativa, viaja sin etiqueta. Por defecto es la VLAN 1. Las dos puntas del troncal tienen que tener la misma VLAN nativa; si no coinciden, el tráfico de una VLAN aparece en otra y los switches Cisco avisan con un mensaje de "native VLAN mismatch".

La recomendación de seguridad es poner como nativa una VLAN que no se use para nada (en nuestro plan la 999), para evitar un ataque llamado salto de VLAN con doble etiqueta.

### La VLAN 1

Todos los puertos de un switch nuevo están en la VLAN 1, y la VLAN 1 no se puede borrar. Dejar equipos de usuarios o la gestión del switch en la VLAN 1 es mala práctica: cualquier cosa que se conecte a un puerto sin configurar cae ahí. Lo correcto es mover los puertos usados a su VLAN, usar una VLAN de gestión aparte y apagar los puertos que no se usan.

## Comunicación entre VLANs

Como cada VLAN es una red distinta, hace falta enrutamiento. Hay tres formas, de la más vieja a la más usada hoy:

1. Un router con una interfaz física por VLAN. Funciona, pero con muchas VLANs se acaban las interfaces. Casi no se usa.
2. Router en un palo (router on a stick): un solo cable troncal entre el switch y el router, y en el router una subinterfaz por VLAN, cada una con su etiqueta y su IP de gateway. Es barato y es lo que se practica en Packet Tracer.
3. Switch de capa 3: el mismo switch enruta entre VLANs con interfaces virtuales (SVI), una por VLAN. Es más rápido porque no sale del switch. Es lo normal en una empresa mediana.

## Configuración paso a paso en Cisco

Lo que sigue es la configuración de SW_TGU y R_TGU para el plan de arriba con router en un palo. Los comandos se escriben en modo de configuración global (`configure terminal`). El laboratorio 02 trae la práctica completa en Packet Tracer.

### Paso 1. Crear y nombrar las VLANs en el switch

```
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
```

### Paso 2. Asignar los puertos de acceso

```
interface range fa0/1 - 8
 switchport mode access
 switchport access vlan 10
interface range fa0/9 - 14
 switchport mode access
 switchport access vlan 20
interface range fa0/15 - 20
 switchport mode access
 switchport access vlan 30
```

`switchport mode access` fija el puerto como acceso y evita que negocie un troncal solo si alguien conecta otro switch.

### Paso 3. Configurar el troncal hacia el router

```
interface g0/1
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,30,99
```

La lista de VLANs permitidas evita que pase por el troncal tráfico de VLANs que no tienen nada que hacer ahí.

### Paso 4. Apagar los puertos que no se usan

```
interface range fa0/21 - 24
 switchport mode access
 switchport access vlan 999
 shutdown
```

### Paso 5. Dirección de gestión del switch

```
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
 no shutdown
ip default-gateway 192.168.99.1
```

El switch de capa 2 no enruta; la IP es solo para entrar a administrarlo por SSH. `ip default-gateway` le dice cómo responder a quien lo administra desde otra red.

### Paso 6. Subinterfaces en el router

```
interface g0/0
 no shutdown
interface g0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface g0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
interface g0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
interface g0/0.99
 encapsulation dot1Q 99
 ip address 192.168.99.1 255.255.255.0
interface g0/0.999
 encapsulation dot1Q 999 native
```

La interfaz física g0/0 no lleva IP, solo se enciende. Cada subinterfaz es el gateway de su VLAN. El número después del punto puede ser cualquiera, pero ponerle el mismo de la VLAN evita confusiones.

### Paso 7. Verificar

| Comando | Dónde | Qué mirar |
|---|---|---|
| `show vlan brief` | Switch | Cada VLAN con sus puertos. Los troncales no aparecen aquí |
| `show interfaces trunk` | Switch | Qué puertos son troncales, su VLAN nativa y qué VLANs pasan |
| `show interfaces fa0/3 switchport` | Switch | Modo y VLAN de un puerto |
| `show ip interface brief` | Router | Que las subinterfaces estén up y con su IP |
| `show ip route` | Router | Una red conectada (C) por cada VLAN |

La prueba final: una PC de ventas hace ping a su gateway (192.168.10.1), después al gateway de bodega (192.168.30.1) y después a una PC de bodega.

### Con un switch de capa 3

Si en vez de router se usa un switch de capa 3, los pasos 1 a 4 son iguales y en lugar de subinterfaces se crean SVI:

```
ip routing
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
```

`ip routing` es el que enciende el enrutamiento; sin él el switch tiene las IP pero no pasa tráfico entre VLANs.

## VLANs en varios switches

Si la bodega está en otro piso con su propio switch, el enlace entre los dos switches es un troncal y las VLANs tienen que existir en los dos. Un puerto de la VLAN 30 en el switch del primer piso y otro de la VLAN 30 en el segundo piso están en la misma red, como si fuera un solo switch.

Cisco tiene un protocolo, VTP, que copia la lista de VLANs de un switch a los demás. Ahorra trabajo, pero un switch mal configurado que se conecta con un número de revisión más alto puede borrar las VLANs de toda la red. En redes chicas se recomienda dejarlo en modo transparente y crear las VLANs a mano.

## Caso resuelto: diagnosticar una falla

Síntoma: la PC de una contadora (puerto fa0/10) no puede hacer ping a su gateway 192.168.20.1. Las demás PC de administración sí.

1. ¿Tiene la IP correcta? `ipconfig` dice 192.168.20.35/24, gateway 192.168.20.1. Bien.
2. ¿El puerto está en la VLAN correcta? `show vlan brief` muestra fa0/10 en la VLAN 1. Ahí está el problema: alguien cambió el puerto o el switch se reinició sin guardar la configuración.
3. Arreglo: `interface fa0/10`, `switchport access vlan 20`. Después `copy running-config startup-config` para guardar.

Otros síntomas típicos y su causa más probable:

| Síntoma | Causa probable |
|---|---|
| Ninguna PC de una VLAN llega al gateway, las demás VLANs sí | Esa VLAN no está permitida en el troncal, o falta su subinterfaz, o el número de `encapsulation dot1Q` no coincide |
| Ninguna VLAN llega al gateway | El troncal no está formado (el puerto quedó en acceso) o la interfaz física del router está apagada |
| PC de VLAN distintas se hablan sin pasar por el router | Puertos en la misma VLAN por error, o VLAN nativa distinta en las dos puntas |
| La PC llega al gateway pero no a otra VLAN | Falta una ruta, el otro equipo tiene mal su gateway, o una lista de acceso lo bloquea |

## Errores comunes

1. Crear la VLAN en un switch y olvidarla en el otro extremo del troncal.
2. Poner IP a la interfaz física del router en un router en un palo. La IP va en las subinterfaces.
3. Usar números de VLAN distintos entre la subinterfaz y el switch.
4. Dejar todo en VLAN 1 o usar la VLAN 1 para gestión.
5. Olvidar `no shutdown` en la interfaz física del router.
6. Olvidar `ip routing` en un switch de capa 3.
7. No guardar la configuración y perderla con el primer apagón.
8. Pensar que las VLANs bastan como seguridad sin reglas entre ellas.

## Preguntas de repaso

1. ¿Qué es un dominio de broadcast y qué tiene que ver con las VLANs?
2. ¿Qué diferencia hay entre un puerto de acceso y uno troncal?
3. ¿Qué lleva la etiqueta 802.1Q y por qué hay como máximo 4094 VLANs?
4. ¿Qué es la VLAN nativa y por qué se cambia?
5. Compará router en un palo con un switch de capa 3: ventajas de cada uno.
6. ¿Por qué no hay que dejar equipos en la VLAN 1?
7. ¿Qué hace `switchport trunk allowed vlan`?
8. Una PC de bodega llega a su gateway pero no a una PC de ventas. Nombrá tres cosas que revisarías.

## Fuentes

1. [Networking Basics de Cisco NetAcad](https://www.netacad.com/courses/networking-basics) (en), curso gratuito con cuenta
2. [Cisco Packet Tracer en NetAcad](https://www.netacad.com/cisco-packet-tracer) (en), descarga gratuita con cuenta
3. El estándar IEEE 802.1Q define la etiqueta de VLAN. Es un documento de IEEE; para estudiar alcanza con lo que explican el curso de NetAcad y la documentación de tu switch
