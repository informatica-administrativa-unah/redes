# Laboratorio 03. Enrutamiento estático entre las tres sucursales

Temas que practica: 07 y 10. Tiempo estimado: 2 horas.

Partís del laboratorio 02 (Tegucigalpa con VLANs) y le agregás San Pedro Sula, La Ceiba, los enlaces WAN y un enlace de respaldo. Al final vas a probar una ruta flotante.

## Topología y direcciones

Es la del [tema 07](../07_Enrutamiento_estatico/teoria.md).

| Enlace | Red | Un extremo | Otro extremo |
|---|---|---|---|
| Tegucigalpa y San Pedro Sula | 10.0.0.0/30 | R_TGU s0/0/0, 10.0.0.1 | R_SPS s0/0/0, 10.0.0.2 |
| Tegucigalpa y La Ceiba | 10.0.0.4/30 | R_TGU s0/0/1, 10.0.0.5 | R_LCE s0/0/0, 10.0.0.6 |
| San Pedro Sula y La Ceiba (respaldo) | 10.0.0.8/30 | R_SPS s0/0/1, 10.0.0.9 | R_LCE s0/0/1, 10.0.0.10 |

| LAN | Red | Gateway | PC de prueba |
|---|---|---|---|
| San Pedro Sula | 192.168.40.0/24 | R_SPS g0/0, .1 | PC_SPS 192.168.40.21 |
| La Ceiba | 192.168.50.0/24 | R_LCE g0/0, .1 | PC_LCE 192.168.50.21 |

## Paso 1. Agregar puertos seriales

El 2911 no trae puertos seriales. En cada router (R_TGU, R_SPS y R_LCE):

1. Pestaña "Physical", apagá el router con el botón de encendido.
2. Arrastrá el módulo `HWIC-2T` a una ranura libre.
3. Encendelo otra vez. Ahora tiene Serial0/0/0 y Serial0/0/1.

Si tu versión de Packet Tracer no tiene ese módulo, usá enlaces Gigabit (g0/1 y g0/2) con cable cruzado y cambiá los nombres de interfaz en los comandos; lo demás es igual.

## Paso 2. Cablear

Usá "Serial DCE" para los tres enlaces WAN. El extremo donde hacés clic primero queda como DCE (el que da el reloj). Conectá de Tegucigalpa hacia las sucursales y de San Pedro Sula hacia La Ceiba. Después agregá un switch y una PC en cada sucursal.

## Paso 3. Interfaces

R_TGU (además de lo del laboratorio 02):

```
interface s0/0/0
 description WAN a San Pedro Sula
 ip address 10.0.0.1 255.255.255.252
 clock rate 2000000
 no shutdown
interface s0/0/1
 description WAN a La Ceiba
 ip address 10.0.0.5 255.255.255.252
 clock rate 2000000
 no shutdown
```

`clock rate` solo hace falta en el extremo DCE. Si lo ponés en el DTE, el router lo ignora con un aviso. Con `show controllers s0/0/0` ves cuál extremo es DCE.

R_SPS:

```
hostname R_SPS
interface g0/0
 ip address 192.168.40.1 255.255.255.0
 no shutdown
interface s0/0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
interface s0/0/1
 description Respaldo a La Ceiba
 ip address 10.0.0.9 255.255.255.252
 clock rate 2000000
 no shutdown
```

R_LCE:

```
hostname R_LCE
interface g0/0
 ip address 192.168.50.1 255.255.255.0
 no shutdown
interface s0/0/0
 ip address 10.0.0.6 255.255.255.252
 no shutdown
interface s0/0/1
 description Respaldo a San Pedro Sula
 ip address 10.0.0.10 255.255.255.252
 no shutdown
```

Antes de seguir: desde cada router, ping al otro extremo de cada enlace (por ejemplo, desde R_SPS `ping 10.0.0.1` y `ping 10.0.0.10`). Si un enlace no responde, no tiene sentido configurar rutas todavía.

## Paso 4. Probar sin rutas

Desde PC_SPS, `ping 192.168.20.10` (el servidor de Tegucigalpa). Falla. En R_SPS, `show ip route`: solo hay redes C y L. Este es el punto de partida del tema 07.

## Paso 5. Rutas estáticas

R_TGU:

```
ip route 192.168.40.0 255.255.255.0 10.0.0.2
ip route 192.168.50.0 255.255.255.0 10.0.0.6
```

R_SPS y R_LCE, de punta:

```
R_SPS: ip route 0.0.0.0 0.0.0.0 10.0.0.1
R_LCE: ip route 0.0.0.0 0.0.0.0 10.0.0.5
```

(Escribí cada línea en el router que corresponde, sin el nombre del router adelante.)

Probá desde PC_SPS: `ping 192.168.20.10`, `ping 192.168.50.21`, `tracert 192.168.50.21`. El `tracert` hacia La Ceiba tiene que pasar por Tegucigalpa: 192.168.40.1, 10.0.0.1, 10.0.0.6 y la PC.

## Paso 6. Olvidar la vuelta, a propósito

En R_TGU, `no ip route 192.168.50.0 255.255.255.0 10.0.0.6`. Desde PC_LCE, `ping 192.168.20.10`: falla. Pero desde R_LCE, `ping 192.168.20.10` sí funciona. Explicá por qué en tu cuaderno (lo resolviste en el ejercicio 6 del tema 07). Volvé a poner la ruta.

## Paso 7. Respaldo con rutas flotantes

R_LCE:

```
ip route 0.0.0.0 0.0.0.0 10.0.0.9 10
```

R_TGU:

```
ip route 192.168.50.0 255.255.255.0 10.0.0.2 10
```

R_SPS:

```
ip route 192.168.50.0 255.255.255.0 10.0.0.10
```

Ahora `show ip route` en R_LCE muestra solo la ruta por defecto por 10.0.0.5: la flotante no aparece porque tiene AD 10.

Prueba: en R_TGU, `interface s0/0/1` y `shutdown`. Esperá unos segundos y mirá otra vez `show ip route` en R_LCE y en R_TGU: entraron las flotantes. Desde PC_LCE, `tracert 192.168.20.10`: ahora pasa por 10.0.0.9 (San Pedro Sula). Encendé la interfaz con `no shutdown` y comprobá que todo vuelve al camino principal.

## Lista de comprobación

1. Todas las PC de las tres sucursales se hacen ping entre ellas y llegan a SRV01.
2. El `tracert` normal de La Ceiba a Tegucigalpa va directo por 10.0.0.5.
3. Con el enlace de La Ceiba caído, el tráfico pasa por San Pedro Sula, y vuelve solo al encenderlo.
4. Guardaste la configuración de los tres routers.
5. Guardaste el archivo; lo vas a usar en el laboratorio 04.
