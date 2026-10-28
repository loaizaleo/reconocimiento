## reconocimiento
Programas para registrar, clasificar y visualizar productos. Está compuesto principalmente por tres programas
* clasificador
* Registrador
* Visualizador

# Clasificador_V2.py
clasificador_V2.py: ordena fotos por categoría

Qué hace: pide una carpeta de imágenes (jpg, jpeg, png, webp, sin subcarpetas), muestra cada foto y mueve el archivo a clasificados\<categoria>\. Las categorías salen del .txt y de las carpetas que ya existan en clasificados. Si escribe una categoría nueva, se crea la carpeta y se agrega al .txt.

Cómo se maneja:

Al escribir, la lista de la derecha filtra por coincidencia parcial y muestra hasta 20, con las más usadas primero.
Enter clasifica, Shift+Enter repite la última categoría, Ctrl+Z deshace, Espacio salta la foto.
Un clic en la lista copia la categoría al cuadro de texto y un doble clic clasifica.

# Registrador
registradorV3.py: registra ventas en un CSV

Qué hace: pide una carpeta, toma la fecha del nombre (si no encuentra AAAA-MM-DD, usa la de hoy) y muestra cada foto. Usted escribe la referencia y, opcionalmente, la cantidad, y el programa agrega una línea fecha,cantidad,modelos_id a ventas_log.csv. No mueve ni modifica las fotos.

Cómo interpreta lo que escribe:

Si el último número va del 1 al 20, es la cantidad (123 2 es modelo 123, dos unidades). Si no, la cantidad es 1.
La referencia se resuelve en este orden: coincidencia exacta, solo el ID numérico (busca una categoría que empiece con ID_), el elemento seleccionado en la lista, o el texto tal cual.
No avanza la foto al registrar, de modo que puede anotar varios productos de la misma imagen. Para pasar a la siguiente use la flecha derecha (o el botón Skip).
