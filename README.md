# Redes

Curso práctico de redes armado por estudiantes de Informática Administrativa de la UNAH para estudiantes. Cubre lo que se ve en redes básico y en el segundo curso de redes: modelos por capas, direccionamiento, subneteo, VLSM, IPv6, VLANs, enrutamiento estático, DHCP, DNS, NAT y diagnóstico. Cada tema trae teoría a fondo con casos resueltos, ejercicios con solución aparte y, para el subneteo, ejercicios que se revisan solos.

Todos los ejemplos usan la red de Comercial El Guayabo, una empresa hondureña inventada con sucursales en Tegucigalpa, San Pedro Sula y La Ceiba. Es la misma empresa del curso de SQL de la organización.

Este repo es de una comunidad estudiantil. No es material oficial de la UNAH ni de ninguna clase. El texto es propio; las fuentes que usamos son públicas y están citadas al final de cada tema.

## Información del curso

| | |
|---|---|
| Carrera | Informática Administrativa, UNAH |
| Nivel | Desde cero. Sirve para redes básico, el segundo curso de redes o para preparar una certificación de entrada |
| Lo que necesitás | Cuaderno y lápiz para el subneteo, Python 3.10 o más nuevo para el revisor, y Cisco Packet Tracer para los laboratorios |
| Simulador | [Cisco Packet Tracer](https://www.netacad.com/cisco-packet-tracer), gratis con una cuenta de NetAcad |

## Contenido

| Tema | De qué trata |
|---|---|
| [01 Modelo OSI y TCP/IP](01_Modelo_OSI_y_TCP_IP/teoria.md) | Capas, encapsulamiento, TCP y UDP, qué equipo trabaja en qué capa, diagnosticar por capas |
| [02 Direccionamiento IPv4 y máscaras](02_Direccionamiento_IPv4_y_mascaras/teoria.md) | Binario, red y host, máscaras, red y broadcast, privadas y especiales, gateway |
| [03 Subneteo](03_Subneteo/teoria.md) | Bits prestados, el método en seis pasos, seis casos resueltos, wildcard |
| [04 VLSM y sumarización](04_VLSM/teoria.md) | Máscaras de largo variable, cuando no cabe, rutas resumidas |
| [05 IPv6 básico](05_IPv6_basico/teoria.md) | Formato, abreviar y expandir, tipos de direcciones, SLAAC, subneteo IPv6 |
| [06 VLANs](06_VLANs/teoria.md) | Puertos de acceso y troncales, 802.1Q, router en un palo, switch de capa 3 |
| [07 Enrutamiento estático](07_Enrutamiento_estatico/teoria.md) | Tabla de rutas, coincidencia más larga, ruta por defecto, rutas flotantes |
| [08 DHCP y DNS](08_DHCP_y_DNS/teoria.md) | DORA, pools, agente de retransmisión, registros DNS, cómo se resuelve un nombre |
| [09 NAT](09_NAT/teoria.md) | Estática, dinámica, PAT, publicar un servidor, CGNAT |
| [10 Diagnóstico de red](10_Diagnostico_de_red/teoria.md) | Método, escalera del ping, ipconfig, ping, tracert, nslookup, casos reales |

Cada carpeta tiene lo mismo:

```
03_Subneteo/
├── teoria.md          el capítulo: explicación, casos resueltos, errores comunes y preguntas de repaso
├── ejemplos/          casos extra o scripts para comprobar tus cuentas
├── ejercicios/        10 ejercicios de dificultad creciente
└── soluciones/        una forma de resolverlos, con el paso a paso
```

Y en la raíz:

| Carpeta | Qué tiene |
|---|---|
| [`laboratorios/`](laboratorios/) | Cuatro guías paso a paso para Packet Tracer que arman la red completa de la empresa |
| [`ejercicios/subneteo.yml`](ejercicios/subneteo.yml) | 26 ejercicios de subneteo, VLSM, sumarización e IPv6 para llenar |
| [`herramientas/revisar.py`](herramientas/revisar.py) | El revisor automático de esos ejercicios |
| [`soluciones/subneteo.yml`](soluciones/subneteo.yml) | Las respuestas, para cuando ya lo intentaste |

## Laboratorios

| Lab | Qué armás | Temas |
|---|---|---|
| [01 La red de una sucursal](laboratorios/lab_01_red_de_una_sucursal.md) | La Ceiba con direcciones fijas | 01, 02, 10 |
| [02 VLANs y router en un palo](laboratorios/lab_02_vlans_y_router_en_un_palo.md) | Tegucigalpa partida en VLANs | 06, 10 |
| [03 Enrutamiento entre sucursales](laboratorios/lab_03_enrutamiento_entre_sucursales.md) | Las tres sucursales unidas, con respaldo | 07, 10 |
| [04 DHCP, DNS y NAT](laboratorios/lab_04_dhcp_dns_y_nat.md) | Servicios centrales y salida a internet | 08, 09, 10 |

Los laboratorios son guías en texto; el repo no trae archivos `.pkt`. Armar la red vos es la mitad del aprendizaje. Cada lab termina con una sección "romperlo a propósito", que es la más importante.

## Ejercicios de subneteo que se revisan solos

1. Hacé tu propia copia con el botón verde "Use this template" y "Create a new repository" (o con fork). Si solo querés practicar en tu compu, también podés clonar o bajar el ZIP.
2. Abrí `ejercicios/subneteo.yml`. Cada ejercicio tiene el enunciado en comentarios y campos vacíos:

   ```
   # Una impresora de la bodega de La Ceiba tiene 192.168.20.77/26.
   e03:
     red: 192.168.20.64
     mascara: /26
     broadcast:
   ```

3. Resolvé en papel y escribí cada respuesta después de los dos puntos. Las máscaras se aceptan como 255.255.255.192, /26 o 26.
4. Revisá desde la carpeta del repo:

   ```
   python herramientas/revisar.py
   ```

   Te dice qué ejercicios están bien y, para cada campo que no cuadra, una pista de qué revisar sin darte el número.
5. Hacé commit y push. GitHub corre el mismo revisor en cada push y en cada pull request (está en `.github/workflows/revisar.yml`). En la pestaña "Actions", o en el círculo junto a tu último commit, ves verde si todo está bien y rojo si falta algo. Es normal que esté rojo mientras vas avanzando.

El revisor no guarda las respuestas: las calcula con el módulo `ipaddress` de Python a partir de los datos de cada ejercicio. Solo usa la biblioteca estándar, no hay que instalar nada.

## Usalo en Codespaces, sin instalar nada

Si no tenés Python en tu compu, abrí tu copia en GitHub Codespaces: botón "Code", pestaña "Codespaces", "Create codespace on main". Se abre un VS Code en el navegador con Python listo, y ahí corrés el revisor. Las cuentas personales traen horas gratis al mes y los estudiantes verificados en GitHub Education tienen más ([detalle de la cuota](https://docs.github.com/es/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces)). Abrilo en tu copia y no en el repo de la organización, así el uso cuenta en tu cuota personal. Packet Tracer no corre en Codespaces; para los laboratorios necesitás instalarlo en tu compu.

## Cómo estudiar con esto

1. Leé la teoría de un tema con cuaderno al lado y hacé los casos resueltos vos, sin mirar la solución del texto.
2. Contestá las preguntas de repaso del final. Si alguna no te sale, volvé a esa sección.
3. Hacé los ejercicios del tema en papel y compará con las soluciones.
4. Para subneteo, VLSM e IPv6, completá también los niveles de `subneteo.yml` que corresponden.
5. Cuando terminés los temas 01, 02 y 10, hacé el laboratorio 01; con el 06, el 02; con el 07, el 03; con el 08 y 09, el 04.
6. Los scripts de `ejemplos/` sirven para comprobar, no para resolver. En el examen no vas a tener Python.

## Cómo contribuir

Encontraste un error, se te ocurrió un ejercicio mejor o querés agregar un tema (OSPF, listas de acceso, wifi). Dale:

1. Hacé fork del repo y creá una rama: `git checkout -b tema-04-ejercicio-nuevo`
2. Si agregás ejercicios a `subneteo.yml`, agregá también la pregunta en `PREGUNTAS` dentro de `herramientas/revisar.py` y su respuesta en `soluciones/subneteo.yml`, y corré `python herramientas/revisar.py --soluciones`. Es lo que revisa GitHub en cada pull request.
3. Si agregás teoría, escribila con tus palabras y citá fuentes públicas (RFC, documentación oficial). No copiés presentaciones de docentes ni libros con derechos de autor.
4. Abrí un pull request contando qué cambiaste y por qué.

Para dudas sobre el material, usá Discussions de la organización. Para errores, abrí un issue.

## Licencia

[MIT](LICENSE). Podés usar, copiar y adaptar el material, también en tus clases o tutorías, siempre que dejés el aviso de la licencia.
