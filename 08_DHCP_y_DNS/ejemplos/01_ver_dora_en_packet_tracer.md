# Ejemplo: ver DORA y una consulta DNS en Packet Tracer

Con la red del [laboratorio 04](../../laboratorios/lab_04_dhcp_dns_y_nat.md) ya funcionando.

## DORA paso a paso

1. Modo "Simulation", filtros solo DHCP.
2. En PC_LCE, "IP Configuration": cambiá a "Static" y otra vez a "DHCP". Eso dispara el pedido.
3. Avanzá con "Capture / Forward" y mirá los cuatro mensajes. Hacé clic en cada sobre:
   1. El Discover sale de 0.0.0.0 hacia 255.255.255.255.
   2. En R_LCE, el agente de retransmisión lo convierte en un paquete unicast hacia 192.168.20.10. En los detalles aparece el campo con la dirección del gateway (GIADDR) puesto en 192.168.50.1: así sabe el servidor qué pool usar.
   3. Vuelven la Offer y, después del Request, el ACK.
4. Al terminar, `ipconfig /all` en PC_LCE muestra el servidor DHCP 192.168.20.10.

## Una consulta DNS

1. Filtros solo DNS.
2. En PC_LCE, `nslookup ventas.interno.guayabo.example`.
3. Mirá el sobre: UDP, puerto de destino 53, destino 192.168.20.10. La respuesta trae el registro A.
4. Repetí el `ping` por nombre dos veces. La segunda no sale consulta DNS porque la PC usa su caché.

## Lo que conviene anotar

1. Qué mensajes van por broadcast y cuáles por unicast.
2. Qué hace el router con el broadcast cuando tiene `ip helper-address` y qué hace cuando no lo tiene (probalo quitándolo).
