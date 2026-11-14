# Tema 02. Ejercicios

Hacelos en papel, sin calculadora de subredes. La idea es que la cuenta te salga sola. Van de más fácil a más difícil. Los del nivel 1 del archivo [`ejercicios/subneteo.yml`](../../ejercicios/subneteo.yml) también son de este tema y se revisan solos.

## Ejercicio 1

Convertí a binario de 8 bits: 10, 172, 192, 224, 255, 99.

## Ejercicio 2

Convertí a decimal con puntos:

1. `11000000.10101000.00000001.00001010`
2. `00001010.11111111.10000000.00000001`

## Ejercicio 3

Completá: /19 en máscara decimal, /27 en máscara decimal, 255.255.255.248 en prefijo, 255.255.240.0 en prefijo, /12 en máscara decimal.

## Ejercicio 4

Clasificá cada dirección como privada, pública, especial (decí cuál) o inválida: 10.200.3.4, 172.31.255.1, 172.32.0.1, 192.168.300.1, 127.0.0.53, 169.254.10.10, 100.70.1.1, 8.8.8.8, 203.0.113.5.

## Ejercicio 5

¿Cuántos hosts útiles tiene cada red? /29, /25, /22, /18, /30.

## Ejercicio 6

Para cada dirección sacá la red, el broadcast, el primer y último host y la cantidad de hosts útiles. Mostrá el octeto interesante y el tamaño de bloque.

1. 192.168.50.130/25
2. 172.16.77.9/20
3. 10.45.200.17/12

## Ejercicio 7

¿Cuáles de estas direcciones se le pueden poner a un equipo en la red 172.16.32.0/22? Explicá cada una: 172.16.32.0, 172.16.33.255, 172.16.35.255, 172.16.36.1, 172.16.34.0.

## Ejercicio 8

¿Cuáles de estas máscaras son válidas? Para las que no, explicá por qué: 255.255.255.100, 255.255.0.255, 255.255.254.0, 255.0.255.0, 255.255.255.252.

## Ejercicio 9

En San Pedro Sula configuraron una PC así: IP 192.168.40.25, máscara 255.255.255.192, gateway 192.168.40.65. La PC ve a las demás de su oficina pero no sale a ninguna otra red. Explicá el problema con la cuenta del AND y proponé dos formas de arreglarlo.

## Ejercicio 10

Revisá estas tres configuraciones de PC de La Ceiba y decí qué está mal en cada una, si algo lo está. La red de la sucursal es 192.168.50.0/24 con gateway 192.168.50.1.

1. IP 192.168.50.0, máscara 255.255.255.0, gateway 192.168.50.1.
2. IP 192.168.50.44, máscara 255.255.0.0, gateway 192.168.50.1.
3. IP 192.168.50.255, máscara 255.255.255.0, gateway 192.168.50.1.
