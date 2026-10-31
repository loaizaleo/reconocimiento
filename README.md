# reconocimiento

Herramientas de escritorio para **clasificar fotos de productos (tenis), registrar ventas a partir de esas fotos y consultar el catálogo de modelos**.

## Objetivo

Pasar de un montón de fotos de ventas sin organizar a datos estructurados:

1. Ordenar las fotos por modelo (una carpeta por referencia).
2. Convertir cada venta fotografiada en una fila de un CSV (`fecha, cantidad, modelos_id`).
3. Tener un catálogo visual para buscar rápidamente una referencia y ver su foto.

El CSV resultante está pensado para cargarse en la base de datos de ventas (ver el repositorio [DBVentas](https://github.com/loaizaleo/DBVentas)).

## Lenguaje y tecnologías

- **Python 3**
- **Tkinter** para las ventanas (viene con Python en Windows)
- **Pillow** (`PIL`) para abrir y mostrar imágenes

## Archivos

| Archivo | Descripción |
|---|---|
| `clasificador_V2.py` | Muestra fotos una por una y las mueve a `clasificados/<categoria>/`. |
| `registradorV3.py` | Muestra fotos y registra ventas en `ventas_log.csv`. |
| `visor.py` | Catálogo: busca una referencia y muestra su imagen. |
| `categorias_codigoV2.txt` | Lista de referencias (una por línea). |
| `marcas.txt` | Tabla de códigos de marca (`1 NIKE`, `2 ADIDAS`, ...). |

### Formato de las referencias

Cada línea de `categorias_codigoV2.txt` sigue el patrón:

```
<modelos_id>_<marcas_id>_<modelo>_<colores>
```

Ejemplo: `29_2_adistarcs_negra_blanca_chispas` → modelo 29, marca 2 (ADIDAS), modelo *adistarcs*, colores negra/blanca/chispas.

## Instalación

```bash
pip install pillow
```

## Uso

Ejecute los programas desde la carpeta del proyecto (las rutas de `categorias_codigoV2.txt`, `clasificados/` y `ventas_log.csv` son relativas a la carpeta actual):

```bash
python clasificador_V2.py
python registradorV3.py
python visor.py
```

### clasificador_V2.py — ordena fotos por categoría

Pide una carpeta de imágenes (`jpg`, `jpeg`, `png`, `webp`, sin subcarpetas), muestra cada foto y mueve el archivo a `clasificados/<categoria>/`. Las categorías salen del `.txt` y de las carpetas que ya existan en `clasificados`. Si escribe una categoría nueva, se crea la carpeta y se agrega al `.txt`.

- Al escribir, la lista de la derecha filtra por coincidencia parcial y muestra hasta 20, con las más usadas primero.
- **Enter** clasifica, **Shift+Enter** repite la última categoría, **Ctrl+Z** deshace, **Espacio** salta la foto.
- Un clic en la lista copia la categoría al cuadro de texto y un doble clic clasifica.

### registradorV3.py — registra ventas en un CSV

Pide una carpeta, toma la fecha del nombre de la carpeta (si no encuentra `AAAA-MM-DD`, usa la de hoy) y muestra cada foto. Usted escribe la referencia y, opcionalmente, la cantidad, y el programa agrega una línea `fecha,cantidad,modelos_id` a `ventas_log.csv`. **No mueve ni modifica las fotos.**

- Si el último número va del 1 al 20, es la cantidad (`123 2` es modelo 123, dos unidades). Si no, la cantidad es 1.
- La referencia se resuelve en este orden: coincidencia exacta, solo el ID numérico (busca una categoría que empiece con `ID_`), el elemento seleccionado en la lista, o el texto tal cual.
- No avanza la foto al registrar, de modo que puede anotar varios productos de la misma imagen. Para pasar a la siguiente use la **flecha derecha** (o el botón *Skip*).

### visor.py — catálogo de modelos

Carga todas las referencias de `categorias_codigoV2.txt`, permite buscarlas por nombre o ID y, al seleccionar una, muestra la primera imagen encontrada en `clasificados/<referencia>/`.

## Flujo de trabajo recomendado

```
fotos sin ordenar ──► clasificador_V2.py ──► clasificados/<referencia>/
fotos de ventas  ──► registradorV3.py  ──► ventas_log.csv ──► base de datos (DBVentas)
clasificados/    ──► visor.py          ──► consulta del catálogo
```

## Notas

- `visor.py` tiene **rutas absolutas de Windows** escritas en el código (`ARCHIVO_TXT` y `CARPETA_BASE`, al inicio del archivo). Ajústelas a su equipo antes de usarlo.
- `clasificador_V2.py` **mueve** las fotos (no las copia). Conviene trabajar sobre una copia si quiere conservar la carpeta original.
