# Tema 06. Soluciones

## Ejercicio 1

1. Falso. Necesitan un router o un switch de capa 3.
2. Verdadero.
3. Falso. La pone el switch al mandar por un troncal; las PC mandan tramas sin etiqueta.
4. Falso. La VLAN 1 existe siempre y no se puede borrar.
5. Verdadero.

## Ejercicio 2

```
vlan 40
 name VENTAS
vlan 41
 name BODEGA
vlan 42
 name ADMINISTRACION
vlan 999
 name NATIVA_SIN_USO
interface range fa0/1 - 10
 switchport mode access
 switchport access vlan 40
interface range fa0/11 - 16
 switchport mode access
 switchport access vlan 41
interface range fa0/17 - 20
 switchport mode access
 switchport access vlan 42
interface range fa0/21 - 23
 switchport mode access
 switchport access vlan 999
 shutdown
interface g0/1
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 40,41,42
```

El puerto fa0/24 no se mencionó en el enunciado; lo correcto es apagarlo también.

## Ejercicio 3

```
interface g0/0
 no shutdown
interface g0/0.40
 encapsulation dot1Q 40
 ip address 192.168.40.1 255.255.255.192
interface g0/0.41
 encapsulation dot1Q 41
 ip address 192.168.40.65 255.255.255.192
interface g0/0.42
 encapsulation dot1Q 42
 ip address 192.168.40.129 255.255.255.192
interface g0/0.999
 encapsulation dot1Q 999 native
```

## Ejercicio 4

1. La PC manda una trama normal a la MAC de su gateway (192.168.10.1), porque el destino está en otra red.
2. El switch la recibe por fa0/3, sabe que es VLAN 10 y la manda por el troncal g0/1 con etiqueta 10.
3. El router la recibe en la subinterfaz g0/0.10, quita la trama, mira la IP de destino (192.168.30.x), ve que esa red está conectada en g0/0.30 y arma una trama nueva con etiqueta 30.
4. El switch recibe la trama con etiqueta 30 por el troncal, le quita la etiqueta y la entrega por fa0/16.

La trama cruza el mismo cable entre switch y router dos veces, una por VLAN.

## Ejercicio 5

1. Fa0/10 está en la VLAN 1 y según el plan va en la 20.
2. Fa0/21 a Fa0/24 están en la VLAN 1; deberían estar en la 999 y apagados.
3. No existen la VLAN 99 (gestión) ni la 999 (nativa sin uso).

El g0/1 no aparece porque `show vlan brief` solo lista puertos de acceso; los troncales se ven con `show interfaces trunk`.

## Ejercicio 6

La VLAN 30 no está en la lista de permitidas del troncal: solo pasan 10, 20 y 99. Arreglo:

```
interface g0/1
 switchport trunk allowed vlan add 30
```

`add` agrega a la lista sin borrar las que ya estaban. Si se escribe `switchport trunk allowed vlan 30` sin `add`, queda solo la 30 y se caen las demás.

## Ejercicio 7

La subinterfaz espera tramas con etiqueta 3, pero el switch manda las de bodega con etiqueta 30. Las tramas no coinciden y las PC de bodega no llegan al gateway. Hay que cambiarlo a `encapsulation dot1Q 30`. El nombre `.30` no importa para el funcionamiento; lo que manda es el número de `encapsulation`. Se usa el mismo número por orden.

## Ejercicio 8

```
ip routing
interface vlan 10
 ip address 192.168.10.1 255.255.255.0
 no shutdown
interface vlan 20
 ip address 192.168.20.1 255.255.255.0
 no shutdown
interface vlan 30
 ip address 192.168.30.1 255.255.255.0
 no shutdown
interface vlan 99
 ip address 192.168.99.1 255.255.255.0
 no shutdown
```

El comando que no se puede olvidar es `ip routing`. Para salir a otras redes o a internet, el switch además necesita un puerto o una SVI hacia el router y una ruta por defecto.

## Ejercicio 9

Fa0/20 es un puerto de acceso de la VLAN 30. Todo lo que entra por ahí sin etiqueta queda en la VLAN 30, sin importar en qué VLAN esté cada equipo en el switch nuevo. Un enlace entre switches que tiene que llevar varias VLANs debe ser troncal en las dos puntas, con la misma VLAN nativa y con las VLANs creadas en los dos switches.

## Ejercicio 10

Respuesta modelo:

1. VLANs: 10 ventas, 20 administración y servidores, 30 bodega, 40 cámaras, 50 wifi de clientes, 99 gestión de equipos de red, 999 nativa sin uso.
2. El número de VLAN coincide con el tercer octeto de su red.
3. Los nombres van en mayúsculas, sin tildes ni espacios.
4. Ningún equipo de usuario va en la VLAN 1.
5. Los puertos sin uso se ponen en la VLAN 999 y se apagan.
6. La VLAN nativa de todos los troncales es la 999, y cada troncal permite solo las VLANs que necesita.
7. La VLAN de gestión solo es accesible desde las PC de TI.
8. El wifi de clientes solo puede salir a internet: no llega a ninguna otra VLAN.
9. Las cámaras solo hablan con el grabador de video; nadie más llega a ellas salvo TI.
10. Ventas llega a los servidores solo en los puertos del sistema de ventas.
11. Todo cambio de VLAN se anota en la bitácora de la red con fecha, responsable y motivo.
