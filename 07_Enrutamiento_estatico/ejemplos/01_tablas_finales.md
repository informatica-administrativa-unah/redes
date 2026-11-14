# Ejemplo: tablas de enrutamiento finales de la empresa

Así queda `show ip route` en los tres routers al terminar el [laboratorio 03](../../laboratorios/lab_03_enrutamiento_entre_sucursales.md), con las rutas flotantes ya configuradas y todos los enlaces funcionando. Se quitaron las líneas de leyenda.

## R_TGU

```
Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C       10.0.0.0/30 is directly connected, Serial0/0/0
L       10.0.0.1/32 is directly connected, Serial0/0/0
C       10.0.0.4/30 is directly connected, Serial0/0/1
L       10.0.0.5/32 is directly connected, Serial0/0/1
C    192.168.10.0/24 is directly connected, GigabitEthernet0/0.10
C    192.168.20.0/24 is directly connected, GigabitEthernet0/0.20
C    192.168.30.0/24 is directly connected, GigabitEthernet0/0.30
S    192.168.40.0/24 [1/0] via 10.0.0.2
S    192.168.50.0/24 [1/0] via 10.0.0.6
C    192.168.99.0/24 is directly connected, GigabitEthernet0/0.99
```

(También hay una línea L por cada subinterfaz; se omitieron para que se lea mejor.) La ruta flotante a La Ceiba por 10.0.0.2 con AD 10 no aparece: está esperando. Cuando agregás la salida a internet en el laboratorio 04, aparece `S* 0.0.0.0/0 [1/0] via 203.0.113.1` y "Gateway of last resort is 203.0.113.1".

## R_SPS

```
Gateway of last resort is 10.0.0.1 to network 0.0.0.0

C       10.0.0.0/30 is directly connected, Serial0/0/0
C       10.0.0.8/30 is directly connected, Serial0/0/1
C    192.168.40.0/24 is directly connected, GigabitEthernet0/0
S    192.168.50.0/24 [1/0] via 10.0.0.10
S*   0.0.0.0/0 [1/0] via 10.0.0.1
```

## R_LCE

```
Gateway of last resort is 10.0.0.5 to network 0.0.0.0

C       10.0.0.4/30 is directly connected, Serial0/0/0
C       10.0.0.8/30 is directly connected, Serial0/0/1
C    192.168.50.0/24 is directly connected, GigabitEthernet0/0
S*   0.0.0.0/0 [1/0] via 10.0.0.5
```

## Cómo leer [1/0]

El primer número es la distancia administrativa (1 para estáticas) y el segundo la métrica (en estáticas siempre 0). Una flotante activa se vería como `[10/0]`.

## Con el enlace de La Ceiba caído

R_LCE:

```
C       10.0.0.8/30 is directly connected, Serial0/0/1
C    192.168.50.0/24 is directly connected, GigabitEthernet0/0
S*   0.0.0.0/0 [10/0] via 10.0.0.9
```

R_TGU cambia la línea de La Ceiba por `S 192.168.50.0/24 [10/0] via 10.0.0.2`.
