# ===============================
#      PARTE DECLARATIVA
# =============================

import tkinter as tk
#Llama a las herramientas gráficas y con la palabra reservada 'as' se le asigna un nombre más corto por practicidad
from tkinter import messagebox, ttk
# esto se lee como :
#" de esta caja de herramientas(tkinter), llamemos a:
#  'messagebox'(ventanas emergentes, por ejemplo: ¡guardado con exito)"
#'ttk' significa "themed tkinter", 'tk.button' le da un aspecto de windows95, mientras que 'ttk' se ve como windows10/11
import json # Trae la herramienta para leer y escribir texto en formato de diccionario#
import os # Trae las herramientas del sistema operativo. Nos permite hablar con windows para:
# * CREAR carpetas, BUSCAR rutas y ABRIR ARCHIVOS.
from datetime import datetime

# --- CONFIGURACIÓN DE ARCHIVO --- #
CARPETA = os.path.dirname(os.path.abspath(__file__))

ARCHIVO_DB = os.path.join(CARPETA, "veterinaria_db.json")

class SistemaVeterinaria:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema de Gestión Veterinaria")
        self.root.geometry("800x600")
       # carpeta donde estan las imágenes
        carpeta_imagenes = r"C:\Users\PC\Desktop\seba\Tec.DesarrolloSoftware\PYTHON\Sistema_veterinaria\imagenes"
        # Unimos la carpeta con el nombre de tu archivo (asegúrate que se llame así)
        ruta_icono = os.path.join(carpeta_imagenes, "patas.ico")
        if os.path.exists(ruta_icono):
            try:
                self.root.iconbitmap(ruta_icono)
            except Exception as e:
                print(f"Error al cargar ícono: {e}")
        else:
            print(f"No se encontró el ícono en: {ruta_icono}")
        # Variable para saber con qué paciente estamos trabajando
        self.paciente_actual = None
        # Cargar base de datos
        self.db = self.cargar_datos()

        
        #--- ESTILO DE LAS PESTAÑAS ---#
        style = ttk.Style()
        # Le decimos al estilista: "Busca todas las pestañas (TNotebook.Tab)
        # y ponles esta fuente y este relleno"
        style.configure("TNotebook.Tab",
         font=("Arial", 12, "bold"), padding=[10, 5])
        # padding=[ancho, alto] para que el texto no quede apretado

        # -------------------------------------#
        # ---: ENCABEZADO CON IMAGEN Y TÍTULO---
        # --- BANNER  CON SOMBRA Y CENTRADO ---
        # 1. Creamos el Lienzo (Canvas)
        # height=140: Una altura elegante, ni muy fina ni muy gruesa.
        self.canvas_banner = tk.Canvas(root, height=140, bg="#2c3e50", highlightthickness=0)
        self.canvas_banner.pack(fill="x", side="top")

        # 2. Cargamos la Imagen
        ruta_banner = os.path.join(carpeta_imagenes, "banner_vet_2.png") # O .jpg
        if os.path.exists(ruta_banner):
            # Cargar imagen. Juega con el numero de subsample si la foto es muy grande.
            # Si la foto es GIGANTE (4k), usa subsample(3) o (4). Si es normal, usa (1) o (2).
            self.img_banner_obj = tk.PhotoImage(file=ruta_banner).subsample(2)
            # Dibujamos la imagen
            # La ponemos en el centro aproximado (450) y mitad de altura (70)
            self.banner_id = self.canvas_banner.create_image(
                450, 70,
                image=self.img_banner_obj,
                anchor="center"
            )
        # 3. TEXTO CON SOMBRA 
        # Primero dibujamos el texto negro un poquito movido (+2 pixels)
        self.sombra_id = self.canvas_banner.create_text(
            452, 72,
            text="SISTEMA DE GESTIÓN VETERINARIA",
            fill="black",
            font=("Segoe UI", 24, "bold"),
            anchor="center"
        )
        # Luego dibujamos el texto blanco encima
        self.texto_id = self.canvas_banner.create_text(
            450, 70,
            text="SISTEMA DE GESTIÓN VETERINARIA",
            fill="white",
            font=("Segoe UI", 24, "bold"),
            anchor="center"
        )

        # Activamos el "Sticky" para que todo se mueva al cambiar el tamaño
        self.root.bind("<Configure>", self.actualizar_centro_banner)
      

        #--------------------------------------------------------------#


        # --- SISTEMA DE PESTAÑAS (NOTEBOOK) ---#   


        # El Notebook es el gestor que contiene las pestañas
        self.notebook = ttk.Notebook(root) # crea  un sistema de pestañas(notebook) y lo pone en la ventana principal(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        # Creamos los 4 paneles (Pestañas) #

        self.tab_paciente = ttk.Frame(self.notebook) # creamos un marco(frame) para cada una de las pestañas
        self.tab_vacunas = ttk.Frame(self.notebook)
        self.tab_desparasitacion = ttk.Frame(self.notebook)
        self.tab_historia = ttk.Frame(self.notebook)
        # Añadimos los paneles al Notebook con sus títulos #
        self.notebook.add(self.tab_paciente, text=" 🐕 Gestión Pacientes")
        self.notebook.add(self.tab_vacunas, text=" 💉 Vacunas")
        self.notebook.add(self.tab_desparasitacion, text=" 💊 Desparasitaciones")
        self.notebook.add(self.tab_historia, text=" 📋 Historia Clínica")

        # --- CONSTRUIMOS LOS MÉTODOS ---
        self.crear_interfaz_paciente()
        self.crear_interfaz_vacunas()
        self.crear_interfaz_desparasitacion()
        self.crear_interfaz_historia()

    # -----------------------------------------------------------

    # PESTAÑA 1: GESTIÓN DE PACIENTES (BUSCAR / REGISTRAR)

    # -----------------------------------------------------------

    def crear_interfaz_paciente(self):
        frame = tk.LabelFrame(self.tab_paciente, text="Datos del Cliente y Paciente", padx=20, pady=20,font=("Arial",12))
        frame.pack(fill="x", padx=30, pady=30)
        # frame.columnconfigure(1,weight=1)
        # Campos según croquis
        tk.Label(frame, text="DNI Dueño:",font=("Arial",12)).grid(row=0, column=0, sticky="e")
        self.ent_dni = tk.Entry(frame) # entry es un cuadro en blanco para escribir
        self.ent_dni.grid(row=0, column=1, padx=5, pady=5)
        btn_buscar = tk.Button(frame, text="🔍 BUSCAR / CARGAR", bg="orange", command=self.buscar_paciente)
        btn_buscar.grid(row=0, column=2, padx=10)
        tk.Label(frame, text="Nombre Dueño:",font=("Arial",12)).grid(row=1, column=0, sticky="e")
        self.ent_dueno = tk.Entry(frame)
        self.ent_dueno.grid(row=1, column=1, padx=7, pady=7)
        tk.Label(frame, text="Nombre Mascota:",font=("Arial",12)).grid(row=2, column=0, sticky="e")
        self.ent_mascota = tk.Entry(frame)
        self.ent_mascota.grid(row=2, column=1, padx=7, pady=7)
        tk.Label(frame, text="Especie:",font=("Arial",12)).grid(row=3, column=0, sticky="e")
        self.cbo_especie = ttk.Combobox(frame, values=["Canino", "Felino", "Otro"],state="readonly")
        # combobox= LISTA DESPLEGABLE // state=readonly, hace que
        #el usuario deba elegir si o si una opcion y no tenga la posibilidad de escritura.
        self.cbo_especie.grid(row=3, column=1, padx=7, pady=7)
        btn_guardar_paciente = tk.Button(frame, text="GUARDAR PACIENTE", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.guardar_paciente)
        btn_guardar_paciente.grid(row=4, column=0, columnspan=3,sticky="we", pady=15,padx=40)

        # Etiqueta para saber a quién estamos atendiendo
        self.lbl_estado = tk.Label(self.tab_paciente, text="PACIENTE ACTUAL: Ninguno seleccionado", font=("Arial", 14), fg="red")
        self.lbl_estado.pack(pady=20)

    # -----------------------------------------------------------

    # PESTAÑA 2: CARNET DE VACUNAS

    # -----------------------------------------------------------

    def crear_interfaz_vacunas(self):
        # Formulario
        frame_form = tk.LabelFrame(self.tab_vacunas, text="Nueva Vacuna", padx=10, pady=10,font=("Arial",12))
        frame_form.pack(fill="x", padx=30, pady=30)
        frame_form.columnconfigure(1, weight=1)# Hacemos que la columna de entrada se estire
        tk.Label(frame_form, text="Nombre Vacuna:",font=("Arial",12)).grid(row=0, column=0)
        self.v_nombre = tk.Entry(frame_form)
        self.v_nombre.grid(row=0, column=1,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Fecha Aplicación:",font=("Arial",12)).grid(row=0, column=2)
        self.v_fecha = tk.Entry(frame_form)
        self.v_fecha.insert(0, datetime.now().strftime("%d/%m/%Y")) # Fecha hoy por defecto
        self.v_fecha.grid(row=0, column=3,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Revacunar (dd/mm/aaaa):",font=("Arial",12)).grid(row=1, column=0)
        self.v_prox = tk.Entry(frame_form)
        self.v_prox.grid(row=1, column=1,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Atendido/a Por:",font=("Arial",12)).grid(row=1, column=2)
        self.v_vet = tk.Entry(frame_form)
        self.v_vet.grid(row=1, column=3,pady=5,padx=5,sticky="we")

        tk.Button(frame_form, text="GUARDAR VACUNA", bg="#4CAF50", fg="white", command=lambda: self.guardar_evento("vacunas")).grid(row=2, column=0, columnspan=4, sticky="we", pady=10)
        # Tabla
        self.tree_vacunas = self.crear_tabla(self.tab_vacunas, ["Fecha", "Vacuna", "Revacunación", "Veterinario"])

    # -----------------------------------------------------------

    # PESTAÑA 3: DESPARASITACIONES

    # -----------------------------------------------------------

    def crear_interfaz_desparasitacion(self):
        frame_form = tk.LabelFrame(self.tab_desparasitacion, text="Nueva Desparasitación", padx=10, pady=10,font=("Arial",12))
        frame_form.pack(fill="x", padx=30, pady=30)
        frame_form.columnconfigure(1, weight=1)# Hacemos que la columna de entrada se estire
        tk.Label(frame_form, text="Tipo (Pastilla/Inyec):",font=("Arial",12)).grid(row=0, column=0)
        self.d_tipo = ttk.Combobox(frame_form, values=["Pastilla", "Inyectable", "Pipeta"],state="readonly")
        self.d_tipo.grid(row=0, column=1,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Fecha:",font=("Arial",12)).grid(row=0, column=2)
        self.d_fecha = tk.Entry(frame_form)
        self.d_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.d_fecha.grid(row=0, column=3,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Volver a aplicar(dd/mm/aaaa):",font=("Arial",12)).grid(row=1, column=0)
        self.d_prox = tk.Entry(frame_form)
        self.d_prox.grid(row=1, column=1,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Atendido/a Por:",font=("Arial",12)).grid(row=1, column=2)
        self.d_vet = tk.Entry(frame_form)
        self.d_vet.grid(row=1, column=3,pady=5,padx=5,sticky="we")
        tk.Label(frame_form, text="Observaciones",font=("Arial",12)).grid(row=2, column=0,sticky="we")
        self.d_obs = tk.Entry(frame_form)
        self.d_obs.grid(row=2, column=1,pady=5,padx=5,sticky="we")

        tk.Button(frame_form, text="GUARDAR DESPARASITACIÓN", bg="#2196F3", fg="white", command=lambda: self.guardar_evento("desparasitaciones")).grid(row=3, column=0, columnspan=4, sticky="we", pady=10)
        self.tree_desparasitacion = self.crear_tabla(self.tab_desparasitacion, ["Fecha", "Tipo", "Próxima Dosis","Veterinario","Observaciones"])

    # -----------------------------------------------------------

    # PESTAÑA 4: HISTORIA CLÍNICA (SÍNTOMAS Y TRATAMIENTO)

    # -----------------------------------------------------------
    def crear_interfaz_historia(self):
        frame_form = tk.LabelFrame(self.tab_historia, text="Consulta General", padx=10, pady=10, font=("Arial",12))
        frame_form.pack(fill="x", padx=30, pady=30)

        # Configuración de la columna
        frame_form.columnconfigure(1, weight=1)

        # --- CAMPOS DEL FORMULARIO ---
        tk.Label(frame_form, text="Peso (Kg):", font=("Arial",12)).grid(row=0, column=0, sticky="e")
        self.h_peso = tk.Entry(frame_form, width=10)
        self.h_peso.grid(row=0, column=1, sticky="w", padx=7, pady=4)

        tk.Label(frame_form, text="Diagnóstico:", font=("Arial",12)).grid(row=1, column=0, sticky="e")
        self.h_diag = tk.Entry(frame_form)
        self.h_diag.grid(row=1, column=1, sticky="we", padx=7, pady=4)

        tk.Label(frame_form, text="Medicación:", font=("Arial",12)).grid(row=2, column=0, sticky="e")
        self.h_med = tk.Entry(frame_form)
        self.h_med.grid(row=2, column=1, sticky="we", padx=7, pady=4)
        
        # --- AQUÍ ESTABA EL ERROR (Conflictos de filas y variables) ---
        
       
        tk.Label(frame_form, text="Observaciones:", font=("Arial",12)).grid(row=3, column=0, sticky="e")
        self.h_obs = tk.Entry(frame_form)
        self.h_obs.grid(row=3, column=1, sticky="we", padx=7, pady=4)

        
        tk.Label(frame_form, text="Atendido/a por:", font=("Arial",12)).grid(row=4, column=0, sticky="e")
        self.h_vet = tk.Entry(frame_form) # <--- Variable Corregida
        self.h_vet.grid(row=4, column=1, sticky="we", padx=7, pady=4)

        # ---------------------------------------------------------------

        # Fila 5: BOTONES (Los bajamos una fila)
        frame_botones = tk.Frame(frame_form)
        frame_botones.grid(row=5, column=0, columnspan=2, sticky="we", pady=15) # <--- Ahora row=5
        
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)

        # btn_guardar = tk.Button(frame_botones, text="GUARDAR VISITA", bg="#9C27B0", fg="white", 
        #                         font=("Arial", 10, "bold"),
        #                         command=lambda: self.guardar_evento("historia"))
        # btn_guardar.grid(row=0, column=0, sticky="we", padx=5)

        btn_salir = tk.Button(frame_botones, text="💾 GUARDAR Y SALIR (RESET)", bg="#4CAF50", fg="white", 
                              font=("Arial", 10, "bold"),
                              command=self.guardar_y_salir)
        btn_salir.grid(row=0, column=0, sticky="we", padx=5)

        # Tabla (Asegúrate de que tenga todas las columnas)
        self.tree_historia = self.crear_tabla(self.tab_historia, 
                                              ["Fecha", "Peso", "Diagnóstico", "Medicación", "Observaciones", "Veterinario"])

    # =========================================================================================================================#
    #             ------------------------------- F U N C I O N E S ------------------------------------ 
    # =========================================================================================================================#

    def crear_tabla(self, parent, columnas):
        tree = ttk.Treeview(parent, columns=columnas, show="headings", height=8)
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=100) # Ancho por defecto
            
        # Agregamos Scrollbars (Barras de desplazamiento) por si acaso
        scroll_y = tk.Scrollbar(parent, orient="vertical", command=tree.yview)
        scroll_y.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scroll_y.set)
        
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- invocamos a la clase con la funcion ---#

        ToolTipTabla(tree) 
        
        
        return tree

    def cargar_datos(self):
        if os.path.exists(ARCHIVO_DB):
            with open(ARCHIVO_DB, "r") as f:
                return json.load(f)
        return {}
    def guardar_db(self):
        with open(ARCHIVO_DB, "w") as f:
            json.dump(self.db, f, indent=4)
             
    # --- LÓGICA PRINCIPAL ---

    def buscar_paciente(self):
        dni = self.ent_dni.get().strip()
        mascota_buscada = self.ent_mascota.get().strip().lower() # Lo que escribió el usuario (opcional)

        if not dni:
            messagebox.showwarning("Error", "Ingresa un DNI para buscar.")
            return

        # 1. Buscamos TODAS las claves que empiecen con ese DNI (ej: "123_rex", "123_lola")
        pacientes_encontrados = []
        
        for key in self.db:
            if key.startswith(f"{dni}_"):
                # Si la clave empieza con el DNI, guardamos el nombre de la mascota
                nombre_mascota = self.db[key]["datos"]["mascota"]
                pacientes_encontrados.append(nombre_mascota)

        # 2. Análisis de resultados
        if len(pacientes_encontrados) == 0:
            self.paciente_actual = None
            self.limpiar_tablas_visuales()
            self.lbl_estado.config(text="PACIENTE NO ENCONTRADO", fg="red")
            messagebox.showinfo("Resultado", "No se encontraron mascotas registradas con este DNI.")
            return

        # CASO A: El usuario escribió DNI y también el NOMBRE de la mascota
        if mascota_buscada and (mascota_buscada in [m.lower() for m in pacientes_encontrados]):
            id_unico = f"{dni}_{mascota_buscada}"
            self.cargar_datos_en_interfaz(id_unico)
            messagebox.showinfo("Éxito", f"Paciente {mascota_buscada} cargado.")
        
        # CASO B: Solo hay UNA mascota registrada con ese DNI (Carga automática)
        elif len(pacientes_encontrados) == 1:
            mascota_unica = pacientes_encontrados[0]
            id_unico = f"{dni}_{mascota_unica.lower()}"
            self.cargar_datos_en_interfaz(id_unico)
            messagebox.showinfo("Encontrado", f"Se cargó la única mascota encontrada: {mascota_unica}")

        # CASO C: Hay VARIAS mascotas y el usuario no especificó cuál
        else:
            lista_nombres = ", ".join(pacientes_encontrados)
            messagebox.showinfo("Multiples Mascotas", 
                f"Este dueño tiene varias mascotas registradas: {lista_nombres}.\n\n"
                "Por favor, escribe el nombre de la mascota en el cuadro 'Nombre Mascota' y dale a Buscar de nuevo para cargar la correcta.")

    def guardar_paciente(self):
        # 1. Limpieza de datos
        dni = self.ent_dni.get().strip()
        dueno = self.ent_dueno.get().strip()
        mascota = self.ent_mascota.get().strip()
        especie = self.cbo_especie.get()

        # --- VALIDACIONES ---#
        if not dni or not dueno or not mascota:
            messagebox.showwarning("Faltan Datos", "Completa DNI, Nombre y Mascota.")
            return
        if not dni.isdigit() or len(dni) not in [7, 8]:
            messagebox.showerror("Error DNI", "El DNI debe ser numérico de 7 u 8 dígitos.")
            return

        # --- AQUÍ ESTÁ EL CAMBIO CLAVE (GENERAR ID ÚNICO) ---
        # Convertimos mascota a minúscula para que "Rex" y "rex" sean lo mismo
        id_unico = f"{dni}_{mascota.lower()}"
        
        if id_unico not in self.db:
            # CASO A: Mascota Nueva (Creamos historial vacío)
            self.db[id_unico] = {
                "datos": {
                    "dni": dni, # Guardamos el DNI adentro también por seguridad
                    "dueno": dueno,
                    "mascota": mascota,
                    "especie": especie
                },
                "vacunas": [],
                "desparasitaciones": [],
                "historia": []
            }
            mensaje = f"Se registró a {mascota} correctamente."
        else:
            # CASO B: Mascota Existente (Solo actualizamos nombre dueño/especie)
            self.db[id_unico]["datos"]["dueno"] = dueno
            self.db[id_unico]["datos"]["especie"] = especie
            mensaje = f"Datos de {mascota} actualizados (Historial conservado)."

        # Guardar y actualizar interfaz
        self.guardar_db()
        self.paciente_actual = id_unico # <--- IMPORTANTE: Ahora el paciente actual es el ID compuesto
        self.lbl_estado.config(text=f"PACIENTE ACTUAL: {mascota} ({dni})", fg="green")
        messagebox.showinfo("Éxito", mensaje)

    def guardar_evento(self, tipo):

        if not self.paciente_actual:
            messagebox.showwarning("Error", "Primero debes buscar o seleccionar un paciente en la primera pestaña.")
            return
        # Lógica para VACUNAS
        if tipo == "vacunas":
            nueva_data = {
                "fecha": self.v_fecha.get(),
                "nombre": self.v_nombre.get(),
                "prox": self.v_prox.get(),
                "vet": self.v_vet.get()
            }
            self.db[self.paciente_actual]["vacunas"].append(nueva_data)
            messagebox.showinfo("Guardado", "Vacuna registrada correctamente")

        # Lógica para DESPARASITACIONES

        elif tipo == "desparasitaciones":
            nueva_data = {
                "fecha": self.d_fecha.get(),
                "tipo": self.d_tipo.get(),
                "prox": self.d_prox.get(),
                "vet": self.d_vet.get(),
                "obs":self.d_obs.get()
            }
            self.db[self.paciente_actual]["desparasitaciones"].append(nueva_data)
            messagebox.showinfo("Guardado", "Desparasitación registrada correctamente")

        # Lógica para HISTORIA CLÍNICA

        elif tipo == "historia":
            nueva_data = {
                "fecha": datetime.now().strftime("%d/%m/%Y"),
                "peso": self.h_peso.get(),
                "diag": self.h_diag.get(),
                "med": self.h_med.get(),
                "obs":self.h_obs.get(),
                "vet": self.h_vet.get()
            }
            self.db[self.paciente_actual]["historia"].append(nueva_data)
            messagebox.showinfo("Guardado", "Consulta clínica guardada")
        # AL FINAL: Guardamos en el archivo y refrescamos la vista
        self.guardar_db()
        self.actualizar_todas_las_tablas()

    #-----------------------------------------------------------#

    def actualizar_todas_las_tablas(self):
        ###### # Usamos .get("clave", "-") para que si es un registro viejo y no tiene veterinario, ponga un guion "-"
        # y no rompa el programa.######

        # 1. Primero limpiamos lo que se ve actualmente
        self.limpiar_tablas_visuales()
        # 2. Obtenemos los datos del paciente actual
        datos = self.db[self.paciente_actual]
        # 3. Llenamos la tabla de VACUNAS
        # (Fíjate que el orden de values coincida con las columnas que creaste)
        for v in datos["vacunas"]:
            self.tree_vacunas.insert("", "end", values=(
             v.get("fecha","-"),
             v.get("nombre","-"), 
             v.get("prox","-"),
             v.get("vet","-")))
        # 4. Llenamos la tabla de DESPARASITACIONES
        for d in datos["desparasitaciones"]:
            self.tree_desparasitacion.insert("", "end", values=(
            d.get("fecha", "-"), 
            d.get("tipo", "-"), 
            d.get("prox", "-"), 
            d.get("vet", "-"), 
            d.get("obs", "-")
             ))
        # 5. Llenamos la tabla de HISTORIA
        for h in datos["historia"]:
            self.tree_historia.insert("","end",values=(
                h.get("fecha","-"),
                h.get("peso","-"),
                h.get("diag","-"),
                h.get("med","-"),
                h.get("obs","-"),
                h.get("vet","-")
            ))


    #---------------------------------------------------------#

    def limpiar_tablas_visuales(self):
        # Borra todos los renglones de las 3 tablas
        for item in self.tree_vacunas.get_children():
            self.tree_vacunas.delete(item)
        for item in self.tree_desparasitacion.get_children():
            self.tree_desparasitacion.delete(item)
        for item in self.tree_historia.get_children():
            self.tree_historia.delete(item)

    #-----------------------------------------------------------#

    def guardar_y_salir(self):
        # 1. Primero guardamos la consulta actual
        # (Si los campos están vacíos, guardar_evento ya se encarga de avisar o guardar vacío según tu lógica)
        if self.paciente_actual:
             self.guardar_evento("historia")
        # 2. Si se guardó (o si decidimos salir igual), limpiamos todo
        self.resetear_sistema()

    #----------------------------------------------------------------------#

    def resetear_sistema(self):
        # --- 1. Limpiar Variables de Estado ---
        self.paciente_actual = None
        self.lbl_estado.config(text="PACIENTE ACTUAL: Ninguno seleccionado", fg="red")
        # --- 2. Limpiar Campos de Texto (Pestaña 1) ---
        self.ent_dni.delete(0, tk.END)
        self.ent_dueno.delete(0, tk.END)
        self.ent_mascota.delete(0, tk.END)
        self.cbo_especie.set("")
        # --- 3. Limpiar Campos de Vacunas (Pestaña 2) ---
        self.v_nombre.delete(0, tk.END)
        self.v_prox.delete(0, tk.END)
        self.v_vet.delete(0, tk.END)
        # Opcional: Resetear fecha a hoy
        self.v_fecha.delete(0, tk.END)
        self.v_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        # --- 4. Limpiar Campos de Desparasitación (Pestaña 3) ---
        self.d_tipo.set("")
        self.d_prox.delete(0, tk.END)
        self.d_vet.delete(0, tk.END)
        self.d_fecha.delete(0, tk.END)
        self.d_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))
        # --- 5. Limpiar Campos de Historia (Pestaña 4) ---
        self.h_peso.delete(0, tk.END)
        self.h_diag.delete(0, tk.END)
        self.h_med.delete(0, tk.END)
        self.h_obs.delete(0, tk.END)
        # --- 6. Limpiar Tablas Visuales ---
        self.limpiar_tablas_visuales()
        # --- 7. Volver a la primera pestaña automáticamente ---
        self.notebook.select(self.tab_paciente)

        # Mensaje opcional (a veces es molesto, puedes quitarlo si quieres fluidez)

        # messagebox.showinfo("Listo", "Sistema reiniciado para nuevo paciente.")

    #---------------------------------------------------------------------------------------------#

    def cargar_datos_en_interfaz(self, id_unico):
        # 1. Recuperamos los datos del diccionario usando la clave compuesta
        datos = self.db[id_unico]["datos"]
        
        # 2. Limpiamos los campos visuales
        self.ent_dni.delete(0, tk.END)
        self.ent_dueno.delete(0, tk.END)
        self.ent_mascota.delete(0, tk.END)
        
        # 3. Rellenamos con la info
        self.ent_dni.insert(0, datos["dni"])
        self.ent_dueno.insert(0, datos["dueno"])
        self.ent_mascota.insert(0, datos["mascota"])
        self.cbo_especie.set(datos["especie"])

        # 4. Establecemos el paciente actual en memoria
        self.paciente_actual = id_unico
        # 5. Actualizamos tablas y cartel
        self.actualizar_todas_las_tablas()
        self.lbl_estado.config(text=f"PACIENTE ACTUAL: {datos['mascota']} ({datos['dni']})", fg="green")
        #--funcion que actualiza el banner--#

    def actualizar_centro_banner(self, event):
        # Calculamos el centro exacto de la ventana actual
        nuevo_ancho = self.root.winfo_width()
        centro_x = nuevo_ancho / 2
        centro_y = 70 # La mitad de la altura del canvas (140 / 2)
        # 1. Movemos la imagen
        if hasattr(self, 'banner_id'):
            self.canvas_banner.coords(self.banner_id, centro_x, centro_y)
        # 2. Movemos la sombra (siempre 2 pixeles más allá del centro)
        self.canvas_banner.coords(self.sombra_id, centro_x + 2, centro_y + 2)
        # 3. Movemos el texto principal
        self.canvas_banner.coords(self.texto_id, centro_x, centro_y)

    #---------------------------------------------------------------------------------------------------------#


class ToolTipTabla:
    
    #Clase para mostrar el texto completo de una celda al pasar el mouse por encima.
    
    def __init__(self, tree):
        self.tree = tree
        self.tooltip_window = None
        self.row_id = None
        self.col_id = None
        
        # Escuchamos el movimiento del mouse sobre la tabla
        self.tree.bind("<Motion>", self.check_tooltip)

    def check_tooltip(self, event):
        # Averiguamos en qué fila y columna está el mouse
        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)

        # Si el mouse se movió a una celda diferente, borramos el tooltip anterior
        if row_id != self.row_id or col_id != self.col_id:
            self.hide_tooltip()
            self.row_id = row_id
            self.col_id = col_id

            if row_id and col_id:
                # Obtenemos el texto de la celda
                try:
                    # col_id viene como "#1", "#2". Lo convertimos a índice (0, 1...)
                    col_index = int(col_id.replace("#", "")) - 1
                    
                    # Obtenemos los valores de la fila
                    values = self.tree.item(row_id, "values")
                    
                    if col_index < len(values):
                        texto = values[col_index]
                        # Solo mostramos tooltip si hay texto
                        if texto and str(texto).strip() != "-" and str(texto).strip() != "": 
                            self.show_tooltip(event.x_root, event.y_root, texto)
                except Exception:
                    pass # Si hay error (ej: mouse en borde), no hacemos nada

    def show_tooltip(self, x, y, text):
        if self.tooltip_window:
            return
            
        # ventana flotante (sin bordes)
        self.tooltip_window = tk.Toplevel(self.tree)
        self.tooltip_window.wm_overrideredirect(True) 
        self.tooltip_window.wm_geometry(f"+{x+15}+{y+10}")

        #en la etiqueta se utiliza wraplength como la longitud en pixeles para que existan saltos de linea
        label = tk.Label(self.tooltip_window, 
                         text=text, 
                         background="#ffffe0", 
                         relief="solid", 
                         borderwidth=1, 
                         font=("Arial", 10),
                         wraplength=400,  # <--Ancho máximo en píxeles antes de saltar
                          justify="left")  # <--- Alinea el texto a la izquierda)
        label.pack()

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVeterinaria(root)
    root.mainloop()