# Tema 08. Soluciones

## Ejercicio 1

Discover, Offer, Request, Acknowledge. Discover y Request van siempre por broadcast. Offer y Acknowledge pueden ir por unicast o broadcast según lo que pida el cliente. El servidor usa UDP 67 y el cliente UDP 68.

## Ejercicio 2

Sí: IP, máscara, gateway, DNS, tiempo de préstamo, nombre de dominio. No: la MAC (es de la tarjeta; el cliente la manda, no la recibe) ni el usuario de Windows.

## Ejercicio 3

```
ip dhcp excluded-address 192.168.50.1 192.168.50.15
ip dhcp pool LCE_LAN
 network 192.168.50.0 255.255.255.0
 default-router 192.168.50.1
 dns-server 192.168.20.10
 domain-name interno.guayabo.example
 lease 0 12
```

## Ejercicio 4

En R_SPS y R_LCE, en la interfaz que da a las PC:

```
interface g0/0
 ip helper-address 192.168.20.10
```

Y quitar los pools locales si los había, para que no respondan dos servidores.

En el servidor: un ámbito por cada red (192.168.40.0/24 con gateway 192.168.40.1 y 192.168.50.0/24 con gateway 192.168.50.1), con sus exclusiones. Además el servidor tiene que poder responder: su gateway (192.168.20.1) y R_TGU tienen que tener ruta a las redes de las sucursales, y ningún firewall debe bloquear UDP 67 y 68 entre ellas.

## Ejercicio 5

1. APIPA: la PC no recibió respuesta de ningún servidor DHCP. Revisar enlace, VLAN del puerto, helper y servidor.
2. La IP es de San Pedro Sula pero el gateway no está en su red: alguien la configuró a mano, o hay un servidor DHCP falso o mal configurado. No va a salir de su red.
3. Va a navegar por internet, pero no va a resolver nombres internos como `ventas.interno.guayabo.example`. Hay que darle el DNS 192.168.20.10.

## Ejercicio 6

Casi seguro hay un servidor DHCP falso, por ejemplo un router wifi de casa que alguien conectó en el piso con su DHCP activo. Las PC que reciben primero su oferta toman su gateway (192.168.0.1 es típico de esos routers).

Cómo encontrarlo: en una PC afectada, `ipconfig /all` muestra la línea "Servidor DHCP" con la IP del que respondió. Con esa IP y la tabla ARP o la tabla MAC del switch se ubica en qué puerto está.

Cómo evitarlo: DHCP snooping en los switches, con solo el puerto hacia el router o servidor como confiable, y una política que prohíba conectar equipos de red personales.

## Ejercicio 7

```
srv01        A      192.168.20.10
srv01        AAAA   2001:db8:acad:20::10
ventas       CNAME  srv01.interno.guayabo.example.
inventario   CNAME  srv01.interno.guayabo.example.
impbodega    A      192.168.30.15
```

Registro inverso, en la zona `20.168.192.in-addr.arpa`:

```
10           PTR    srv01.interno.guayabo.example.
```

El nombre del registro inverso son los octetos al revés, por eso 192.168.20.10 queda como 10 dentro de `20.168.192.in-addr.arpa`.

## Ejercicio 8

Primera vez:

1. La PC revisa su caché: no lo tiene.
2. Le pregunta al recursivo 192.168.20.10 (consulta recursiva).
3. El recursivo no lo tiene en caché. Pregunta a un servidor raíz, que lo manda a los de `.hn`.
4. Los de `.hn` lo mandan a los autoritativos de `ejemplo.hn`.
5. El autoritativo responde con la IP y el TTL.
6. El recursivo guarda en caché y responde a la PC, que también lo guarda.

Segunda vez (antes de que venza el TTL): si es la misma PC, responde su propia caché sin salir a la red. Si es otra PC, el recursivo responde de su caché sin preguntar a nadie más. Es mucho más rápido.

## Ejercicio 9

La PC usa 8.8.8.8 como DNS. Ese servidor público no conoce la zona interna, por eso dice que el dominio no existe. Hay que ponerle 192.168.20.10 como DNS (mejor corregirlo en el pool DHCP que a mano), y después `ipconfig /renew` y `ipconfig /flushdns`.

"UnKnown" aparece porque `nslookup` intenta resolver el nombre del propio servidor DNS con un registro inverso (PTR) y no lo encuentra. No es un error.

## Ejercicio 10

1. Miércoles: bajar el TTL del registro A a 5 minutos. Como el TTL viejo es de un día, a más tardar el jueves todas las cachés ya tienen el TTL nuevo.
2. Jueves y viernes: preparar el servidor nuevo en 192.168.20.12 y probarlo por IP.
3. Sábado: apagar o congelar el servicio viejo, copiar los datos finales, cambiar el registro A a 192.168.20.12. En 5 minutos todos apuntan al nuevo.
4. Sábado: probar desde una PC de cada sucursal con `nslookup` y abriendo el sistema. Si algo falla, volver el registro a .10.
5. Domingo o lunes temprano: revisar que ningún equipo tenga la IP vieja escrita a mano (archivos hosts, configuraciones de programas).
6. Lunes, si todo anda: subir el TTL otra vez a un valor normal. Dejar el servidor viejo apagado unos días antes de borrarlo.
