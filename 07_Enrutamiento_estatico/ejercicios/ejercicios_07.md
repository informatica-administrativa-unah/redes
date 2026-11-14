# Tema 07. Ejercicios

Usá la topología del tema. Si podés, armala en Packet Tracer con el [laboratorio 03](../../laboratorios/lab_03_enrutamiento_entre_sucursales.md).

## Ejercicio 1

¿Qué significan las letras C, L, S y S* en `show ip route`? ¿Por qué aparece una ruta L con /32 por cada interfaz?

## Ejercicio 2

Escribí la tabla de enrutamiento que tendría R_LCE solo con sus redes conectadas (sin rutas estáticas), con letra, red e interfaz.

## Ejercicio 3

R_TGU tiene estas rutas. ¿Por dónde sale un paquete hacia cada destino?

```
S    0.0.0.0/0 via 203.0.113.1
S    192.168.40.0/22 via 10.0.0.2
S    192.168.50.0/24 via 10.0.0.6
S    192.168.50.128/25 via 10.0.0.2
```

Destinos: 192.168.41.20, 192.168.50.20, 192.168.50.200, 192.168.44.1, 8.8.4.4.

## Ejercicio 4

Escribí la ruta estática en sus tres formas (siguiente salto, interfaz de salida y completa) para que R_TGU llegue a 192.168.40.0/24 por s0/0/0 con siguiente salto 10.0.0.2. ¿Cuál usarías si el enlace fuera Ethernet?

## Ejercicio 5

Cada una de estas rutas tiene un error. Encontralo.

1. En R_SPS: `ip route 0.0.0.0 0.0.0.0 10.0.0.2`
2. En R_TGU: `ip route 192.168.50.1 255.255.255.0 10.0.0.6`
3. En R_TGU: `ip route 192.168.40.0 255.255.255.0 10.0.0.6`
4. En R_LCE: `ip route 0.0.0.0 255.255.255.255 10.0.0.5`

## Ejercicio 6

Un técnico configura solo esto y dice que "el ping de San Pedro Sula al servidor funciona a medias: el router de San Pedro Sula sí llega, las PC no".

```
R_SPS: ip route 192.168.20.0 255.255.255.0 10.0.0.1
R_TGU: (ninguna ruta hacia San Pedro Sula)
```

Explicá por qué el router sí llega y las PC no. Escribí lo que falta.

## Ejercicio 7

Abren una bodega en Choloma con un router R_CHO conectado solo a R_SPS por el enlace 10.0.0.12/30 (R_SPS .13, R_CHO .14). La LAN de Choloma es 192.168.60.0/24. Escribí todas las rutas que hay que agregar o cambiar en R_CHO, R_SPS y R_TGU para que Choloma llegue a todas las sucursales y a internet, y todas lleguen a Choloma.

## Ejercicio 8

Configurá rutas flotantes para que San Pedro Sula use el enlace de La Ceiba como respaldo si se cae el enlace con Tegucigalpa. Pensá en las tres direcciones del tráfico: de San Pedro Sula a Tegucigalpa, de Tegucigalpa a San Pedro Sula y lo que tiene que saber La Ceiba.

## Ejercicio 9

Un ping de una PC de La Ceiba a 192.168.20.10 falla. El `tracert` desde la PC muestra:

```
  1    1 ms   192.168.50.1
  2   12 ms   10.0.0.5
  3    *       *       *     Tiempo de espera agotado.
```

R_TGU tiene la red 192.168.20.0/24 conectada y el servidor responde a pings de las PC de Tegucigalpa. Dá dos causas posibles y cómo comprobarías cada una.

## Ejercicio 10

El gerente pregunta si conviene pasar a OSPF ahora que la empresa tiene tres sucursales y va a abrir dos más el próximo año. Escribí una recomendación de un párrafo con ventajas y riesgos de quedarse con rutas estáticas y de cambiar a dinámico.
