import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Rutas fijas (modifícalas si cambian de ubicación)
ARCHIVO_TXT = r"C:\Users\hp\Documents\Ingenieria_Analítica_Datos_UM\reconocimiento-img\categorias_codigoV2.txt"
CARPETA_BASE = r"C:\Users\hp\Documents\Ingenieria_Analítica_Datos_UM\reconocimiento-img\clasificados"

# Extensiones de imagen válidas
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')

class VisorReferencias:
    def __init__(self, root):
        self.root = root
        self.root.title("Visor de modelos de tenis")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        # Variables de datos
        self.referencias = []            # Lista de todas las referencias del TXT
        self.imagenes = {}               # Diccionario: referencia -> ruta de imagen o None
        self.referencias_filtradas = []  # Lista que se muestra en el Listbox

        # Cargar datos desde el archivo y mapear imágenes
        self.cargar_datos()

        # Construir interfaz gráfica
        self.crear_interfaz()

        # Mostrar todas las referencias al inicio
        self.actualizar_lista()

    def cargar_datos(self):
        """Lee el archivo TXT y construye el diccionario de imágenes."""
        # Leer referencias del archivo
        try:
            with open(ARCHIVO_TXT, 'r', encoding='utf-8') as f:
                self.referencias = [linea.strip() for linea in f if linea.strip()]
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo:\n{ARCHIVO_TXT}")
            self.root.destroy()
            return

        # Mapear cada referencia a su imagen
        for ref in self.referencias:
            carpeta_ref = os.path.join(CARPETA_BASE, ref)
            imagen = None
            if os.path.isdir(carpeta_ref):
                # Buscar la primera imagen dentro de la carpeta
                archivos = os.listdir(carpeta_ref)
                # Filtrar por extensiones y ordenar alfabéticamente
                imagenes = sorted([
                    arch for arch in archivos
                    if arch.lower().endswith(EXTENSIONES_VALIDAS)
                ])
                if imagenes:
                    # Tomar la primera
                    imagen = os.path.join(carpeta_ref, imagenes[0])
            self.imagenes[ref] = imagen

    def crear_interfaz(self):
        """Diseña y coloca los widgets en la ventana."""
        # Contenedor superior: entrada de búsqueda
        frame_superior = ttk.Frame(self.root)
        frame_superior.pack(pady=10, padx=10, fill=tk.X)

        ttk.Label(frame_superior, text="Buscar (nombre o ID):", font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        self.entry_busqueda = ttk.Entry(frame_superior, width=40)
        self.entry_busqueda.pack(side=tk.LEFT, padx=(10, 0))
        self.entry_busqueda.bind('<KeyRelease>', self.filtrar_lista)

        # Contenedor central: lista de resultados con scrollbar
        frame_lista = ttk.Frame(self.root)
        frame_lista.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set, font=("Arial", 10))
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.mostrar_imagen)

        # Contenedor inferior: área de imagen
        frame_imagen = ttk.Frame(self.root, relief=tk.SUNKEN, borderwidth=2)
        frame_imagen.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.label_imagen = ttk.Label(frame_imagen, text="Seleccione una referencia para ver la imagen",
                                      font=("Arial", 11), anchor=tk.CENTER)
        self.label_imagen.pack(fill=tk.BOTH, expand=True)

    def actualizar_lista(self, texto_busqueda=""):
        """Actualiza el Listbox con las referencias que contengan el texto (case‑insensitive)."""
        self.listbox.delete(0, tk.END)
        texto_busqueda = texto_busqueda.lower().strip()
        self.referencias_filtradas = [
            ref for ref in self.referencias
            if texto_busqueda in ref.lower()
        ]
        for ref in self.referencias_filtradas:
            self.listbox.insert(tk.END, ref)

    def filtrar_lista(self, event=None):
        """Callback cuando se suelta una tecla en el Entry de búsqueda."""
        texto = self.entry_busqueda.get()
        self.actualizar_lista(texto)

    def mostrar_imagen(self, event=None):
        """Carga y muestra la imagen de la referencia seleccionada, o 'no encontrado' si no existe."""
        seleccion = self.listbox.curselection()
        if not seleccion:
            return
        indice = seleccion[0]
        referencia = self.referencias_filtradas[indice]
        ruta_imagen = self.imagenes.get(referencia)

        # Limpiar label actual
        self.label_imagen.config(image='', text='')

        if ruta_imagen and os.path.isfile(ruta_imagen):
            try:
                img = Image.open(ruta_imagen)
                # Redimensionar manteniendo la relación de aspecto, máximo 500x400
                img.thumbnail((500, 400))
                photo = ImageTk.PhotoImage(img)
                self.label_imagen.config(image=photo)
                self.label_imagen.image = photo  # Mantener una referencia para evitar que se recolecte
            except Exception as e:
                self.label_imagen.config(text=f"Error al cargar imagen: {e}")
        else:
            self.label_imagen.config(text="No encontrado", font=("Arial", 14, "italic"), foreground="gray")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisorReferencias(root)
    root.mainloop()