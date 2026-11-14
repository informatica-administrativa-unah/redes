# Tema 09. Soluciones

## Ejercicio 1

Inside local: 192.168.30.14. Inside global: 203.0.113.2. Outside global: 198.51.100.80.

## Ejercicio 2

1. PAT: muchas privadas a una pública.
2. NAT estática completa: el servidor necesita recibir conexiones en todos sus puertos con una dirección fija.
3. NAT estática de puerto (redirección): solo ese puerto, compartiendo la pública con el PAT del resto.

## Ejercicio 3

1. `access-list 1 permit 192.168.10.0 0.0.0.255`
2. Tres líneas, o una que cubra más:

   ```
   access-list 1 permit 192.168.10.0 0.0.0.255
   access-list 1 permit 192.168.20.0 0.0.0.255
   access-list 1 permit 192.168.30.0 0.0.0.255
   ```

   `192.168.0.0 0.0.31.255` cubriría de .0 a .31, que incluye las tres pero también otras redes; solo vale si nadie más las usa.
3. `access-list 1 permit 192.168.40.0 0.0.3.255`

## Ejercicio 4

| Inside local | Inside global | Outside global |
|---|---|---|
| 192.168.10.5:49200 | 203.0.113.2:49200 | 198.51.100.80:443 |
| 192.168.40.9:49200 | 203.0.113.2, otro puerto (por ejemplo 1024) | 198.51.100.80:443 |
| 192.168.50.7:51515 | 203.0.113.2:51515 | 192.0.2.53:53 |

La segunda no puede quedarse con 49200 porque chocaría con la primera hacia el mismo destino.

## Ejercicio 5

1. Las interfaces están al revés: g0/0.10 (la LAN) es inside y g0/1 (internet) es outside.
2. La wildcard está mal: `255.255.255.0` es una máscara. Va `0.0.0.255`.
3. Faltan las demás interfaces internas (las otras VLAN y los enlaces a sucursales), si también tienen que navegar. Con solo esos dos errores corregidos, navega ventas.

## Ejercicio 6

Faltan dos cosas: marcar como inside los enlaces hacia las sucursales y que la lista de acceso cubra sus redes.

```
interface s0/0/0
 ip nat inside
interface s0/0/1
 ip nat inside
access-list 1 permit 192.168.40.0 0.0.0.255
access-list 1 permit 192.168.50.0 0.0.0.255
```

Si la lista ya era `192.168.0.0 0.0.255.255`, solo faltan las interfaces.

## Ejercicio 7

```
ip nat inside source static tcp 192.168.20.30 443 interface g0/1 443
ip nat inside source static tcp 192.168.99.10 22 interface g0/1 2222
```

Riesgos del SSH publicado: queda expuesto a todo internet, y hay programas que prueban contraseñas contra cualquier puerto abierto todo el día. Cambiar el puerto a 2222 reduce el ruido pero no protege. También da acceso directo a la red de gestión, que es la más sensible. En lugar de eso: una VPN para el personal de TI, con autenticación de varios factores, y el SSH solo accesible desde adentro de la VPN. Si de todos modos se publica, permitir solo desde direcciones conocidas, solo con llaves y nunca con contraseña.

## Ejercicio 8

1. Traducción estática de puerto: lo que llegue a 203.0.113.2:443 va a 192.168.20.30:443. No tiene direcciones externas porque es permanente y no pertenece a ninguna conversación en particular.
2. Una PC de ventas abrió una página HTTPS en 198.51.100.80. Su puerto 51000 se tradujo a 1025.
3. Una consulta DNS de 192.168.20.40 a 192.0.2.53, que mantuvo su puerto de origen.

## Ejercicio 9

Desde adentro, el paquete va a 203.0.113.2, el router lo traduce hacia 192.168.20.30, pero el servidor ve el origen privado de la PC y le responde directo por la red interna, sin pasar por la traducción inversa. La PC recibe una respuesta de una dirección que no esperaba y la descarta. Algunos routers lo resuelven con una función especial (NAT loopback o hairpin), pero no todos.

La solución limpia es con DNS dividido: el nombre del catálogo resuelve a 203.0.113.2 para los de afuera (DNS público) y a 192.168.20.30 para los de adentro (DNS interno). Así cada uno va por el camino correcto.

Para el cliente que no entra desde su casa hay que revisar aparte: la regla de redirección, el firewall y si la pública es de verdad pública (ejercicio 10).

## Ejercicio 10

100.72.14.9 está en 100.64.0.0/10, el espacio de CGNAT. El proveedor ahora pone a la empresa detrás de su propio NAT, y las conexiones que llegan desde internet a la "pública" del proveedor nunca llegan al router de la empresa. Opciones:

1. Pedirle al proveedor una IP pública fija (normalmente con costo).
2. Usar IPv6 si el proveedor lo entrega, publicando el catálogo con dirección global y reglas de firewall.
3. Alojar el catálogo fuera de la empresa (un hosting o la nube), que es lo más común para un sitio público.
