==========================================================
Compras. Descuentos en las líneas de los pedidos de compra
==========================================================

Permite realizar descuentos en las líneas de los pedidos de compra.

A partir del "Descuento" y el "Precio unidad bruto" se calcula el campo
"Precio unidad" como:

Precio unidad = Precio unidad bruto * (1 - Descuento)

Por defecto el número de decimales del "Precio unidad bruto" y el "Descuento"
es 4. El número de decimales del "Precio unidad" es la suma de ambos, 8 por
defecto.
Si desea cambiar el número de decimales del "Precio unidad bruto" y/o el
"Descuento", por ejemplo 3 y 2 respectivamente, puede definir las siguientes
variables en el fichero de configuración de trytond:

unit_price_digits = 3
discount_digits = 2
