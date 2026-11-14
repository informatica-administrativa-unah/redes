# Tema 06. Ejercicios

Para los de configuración, si podés, probalos en Packet Tracer con la red del [laboratorio 02](../../laboratorios/lab_02_vlans_y_router_en_un_palo.md).

## Ejercicio 1

Contestá verdadero o falso y corregí los falsos:

1. Dos PC en VLANs distintas del mismo switch se pueden hacer ping sin router.
2. Cada VLAN es un dominio de broadcast.
3. Las PC ponen la etiqueta 802.1Q en sus tramas.
4. La VLAN 1 se puede borrar.
5. Un puerto troncal puede llevar varias VLANs.

## Ejercicio 2

La sucursal de San Pedro Sula tiene un switch de 24 puertos y quiere tres VLANs: 40 ventas (puertos 1 a 10), 41 bodega (11 a 16) y 42 administración (17 a 20). Los puertos 21 a 23 no se usan y el g0/1 va al router. Escribí la configuración del switch, incluyendo una VLAN nativa sin uso.

## Ejercicio 3

Con las redes 192.168.40.0/26 (VLAN 40), 192.168.40.64/26 (VLAN 41) y 192.168.40.128/26 (VLAN 42), escribí la configuración del router R_SPS como router en un palo por su g0/0.

## Ejercicio 4

Explicá qué pasa con una trama que manda una PC del puerto fa0/3 (VLAN 10) hacia una PC del fa0/16 (VLAN 30) en SW_TGU, paso a paso: dónde se le pone etiqueta, dónde se le quita y quién la enruta.

## Ejercicio 5

Este es el resultado de `show vlan brief` en SW_TGU:

```
VLAN Name                Status    Ports
1    default             active    Fa0/10, Fa0/21, Fa0/22, Fa0/23, Fa0/24
10   VENTAS              active    Fa0/1, Fa0/2, Fa0/3, Fa0/4, Fa0/5, Fa0/6, Fa0/7, Fa0/8
20   ADMINISTRACION      active    Fa0/9, Fa0/11, Fa0/12, Fa0/13, Fa0/14
30   BODEGA              active    Fa0/15, Fa0/16, Fa0/17, Fa0/18, Fa0/19, Fa0/20
```

Compará con el plan del tema y anotá todo lo que está mal o falta. ¿Por qué no aparece el puerto g0/1?

## Ejercicio 6

Las PC de la VLAN 30 no llegan a su gateway. Las de la 10 y la 20 sí. `show interfaces trunk` muestra:

```
Port   Mode  Encapsulation  Status    Native vlan
Gi0/1  on    802.1q         trunking  999

Port   Vlans allowed on trunk
Gi0/1  10,20,99
```

¿Cuál es el problema y cómo se arregla?

## Ejercicio 7

En el router está configurado:

```
interface g0/0.30
 encapsulation dot1Q 3
 ip address 192.168.30.1 255.255.255.0
```

¿Qué falla y por qué? ¿Importa que la subinterfaz se llame `.30`?

## Ejercicio 8

La empresa compra un switch de capa 3 para Tegucigalpa. Reescribí la parte de enrutamiento entre VLANs del tema (router en un palo) para hacerlo con SVI en el switch. ¿Qué comando no se puede olvidar?

## Ejercicio 9

Un técnico conecta un switch nuevo de la bodega al puerto fa0/20 de SW_TGU con un cable. Las PC del switch nuevo quedan en la VLAN 30, pero las cámaras que conectó en ese switch, que tenían que ir en otra VLAN, también quedan en la 30. Explicá por qué y cómo debería haberse conectado.

## Ejercicio 10

Escribí una política de una página (en lista numerada) para la red de Comercial El Guayabo sobre VLANs: qué VLANs hay, qué va en cada una, qué se hace con los puertos sin uso, qué VLAN nativa se usa, cómo se nombra cada VLAN y qué tráfico se permite entre VLANs. Pensá en el wifi de clientes y en las cámaras.
