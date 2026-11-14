# Tema 08. Ejercicios

## Ejercicio 1

Ordená los mensajes DHCP y decí cuáles van por broadcast: Request, Offer, Acknowledge, Discover. ¿Qué puertos UDP usan cliente y servidor?

## Ejercicio 2

Para cada dato, decí si lo entrega DHCP normalmente: dirección IP, máscara, MAC de la PC, gateway, servidor DNS, nombre de usuario de Windows, tiempo de préstamo, nombre de dominio.

## Ejercicio 3

Configurá DHCP en R_LCE para la red 192.168.50.0/24: gateway .1, las primeras 15 direcciones fuera del pool, DNS 192.168.20.10, dominio `interno.guayabo.example`, préstamo de 12 horas. Pista: `lease 0 12` es 0 días y 12 horas.

## Ejercicio 4

La empresa decide que el único servidor DHCP sea un Windows Server en 192.168.20.10, en Tegucigalpa. Escribí lo que hay que configurar en R_SPS y en R_LCE, y lo que tiene que tener el servidor para que las sucursales reciban direcciones.

## Ejercicio 5

Tres PC muestran esto en `ipconfig`. Para cada una, ¿qué te dice?

1. IP 169.254.88.12, máscara 255.255.0.0, sin puerta de enlace.
2. IP 192.168.40.55, máscara 255.255.255.0, puerta de enlace 192.168.1.1.
3. IP 192.168.50.33, máscara 255.255.255.0, puerta de enlace 192.168.50.1, DNS 8.8.8.8 solamente.

## Ejercicio 6

Varias PC de ventas en Tegucigalpa reciben como gateway 192.168.0.1, una dirección que la empresa no usa, y no salen a ningún lado. Otras PC del mismo piso funcionan bien. ¿Qué pudo pasar, cómo lo encontrás y cómo se evita que se repita?

## Ejercicio 7

Escribí los registros DNS de la zona `interno.guayabo.example`:

1. El servidor `srv01` en 192.168.20.10 y 2001:db8:acad:20::10.
2. `ventas` e `inventario` son apodos de `srv01`.
3. La impresora `impbodega` en 192.168.30.15.
4. El registro inverso de 192.168.20.10.

## Ejercicio 8

Contá paso a paso cómo se resuelve `www.ejemplo.hn` desde una PC de San Pedro Sula cuyo DNS es 192.168.20.10, la primera vez y la segunda vez que se pregunta. ¿Qué cambia?

## Ejercicio 9

Interpretá esta salida:

```
C:\> nslookup ventas.interno.guayabo.example
Servidor:  UnKnown
Address:  8.8.8.8

*** UnKnown no encuentra ventas.interno.guayabo.example: Non-existent domain
```

¿Qué está mal en la PC y cómo lo arreglás? ¿Por qué el servidor sale como "UnKnown"?

## Ejercicio 10

TI va a mover el servidor de ventas de 192.168.20.10 a 192.168.20.12 el sábado. El registro A tiene un TTL de un día. Escribí el plan de pasos para que el lunes nadie se quede apuntando a la IP vieja, desde el miércoles anterior hasta el lunes.
