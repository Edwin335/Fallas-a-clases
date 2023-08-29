import tkinter as tk
from tkinter import ttk
import pymongo
from pymongo import MongoClient
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime
import tkinter.font as tkFont
from tkinter import PhotoImage
import cv2
from moviepy.editor import VideoFileClip
from threading import Thread

import socket

#configuracion de conexion
client = pymongo.MongoClient("mongodb+srv://edwin:12345@example.hpmkvfw.mongodb.net/")
db = client.estudiante
estudiante = db.estudiante
print(client.list_database_names())

materias = ['Naturales', 'Sociales', 'Matematicas', 'Ed Fisica', 'Español', 'Religion', 'Etica', 'Ingles', 'Informatica', 'Artistica']



#Para centrar las ventanas
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f'{width}x{height}+{x}+{y}') 

def entry_sin_bordes(entry_widget):
    entry_widget.config(
        bg="#D3D3D3",  # Color de fondo gris
        fg="#750b53",   # Color del texto blanco
        relief=tk.FLAT,  # Quita los bordes
        highlightthickness=0  # Quita el borde de resaltado al recibir foco
    )
def entry_sin_bordess(entry_widget, width):
    entry_widget.config(
        bg="#750b53",  # Color de fondo violeta
        fg="white",   # Color del texto blanco
        relief=tk.FLAT,  # Quita los bordes
        highlightthickness=0, # Quita el borde de resaltado al recibir foco
        width=width   
    )
def entry_sin_bordesss(entry_widget, width):
    entry_widget.config(
        bg="white",  # Color de fondo boton blanco
        fg="#750b53",   # Color del texto violeta
        relief=tk.FLAT,  # Quita los bordes
        highlightthickness=0, # Quita el borde de resaltado al recibir foco
        width=width   
    )    

def agregar_alumno():
# Crear una nueva ventana
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Agregar Alumno")
    nueva_ventana.geometry("300x800")

    #tipo de lectra
    fuente_personalizada = tkFont.Font(family="Century Gothic", size=4)

    # Crear los frames o separaciones de la ventana
    frame_izquierdo0 = tk.Frame(nueva_ventana, bg="#750b53")
    frame_izquierdo = tk.Frame(nueva_ventana)
    frame_derecho = tk.Frame(nueva_ventana, bg="#750b53")
    
    # Ubicar los frames en la ventana usando grid
    frame_izquierdo0.pack(side="left", fill="both")
    frame_izquierdo0.config(width=25)
    frame_izquierdo.pack(side="left", fill="both", expand=True)
    frame_derecho.pack(side="left", fill="both")
    frame_derecho.config(width=25)

    # Crear los campos de entrada en la nueva ventana
    id_label = tk.Label(frame_izquierdo, text="ID", font=fuente_personalizada)
    id_label.grid(row=0, column=3, sticky="w", padx=50, pady=1)
    id_entry = tk.Entry(frame_izquierdo)
    id_entry.grid(row=1, column=3, sticky="ew", padx=50, pady=1)  # Ampliamos el Entry a 3 columnas padx izquierdo y derecho, pady arriba y abajo
    entry_sin_bordes(id_entry)

    APELLIDOS_LABEL = tk.Label(frame_izquierdo, text="APELLIDOS", font=fuente_personalizada)
    APELLIDOS_LABEL.grid(row=2, column=3, columnspan=3, sticky="w", padx=50, pady=1)  # Ampliamos el Label a 3 columnas
    APELLIDOS_ENTRY = tk.Entry(frame_izquierdo)
    APELLIDOS_ENTRY.grid(row=3, column=3, columnspan=3, sticky="ew", padx=50, pady=1)  # Ampliamos el Entry a 3 columnas
    entry_sin_bordes(APELLIDOS_ENTRY)

    NOMBRES_LABEL = tk.Label(frame_izquierdo, text="NOMBRES", font=fuente_personalizada)
    NOMBRES_LABEL.grid(row=4, column=3, sticky="w", padx=50, pady=1)
    NOMBRES_ENTRY = tk.Entry(frame_izquierdo)
    NOMBRES_ENTRY.grid(row=5, column=3, columnspan=3, sticky="ew", padx=50, pady=1)  # Ampliamos el Entry a 3 columnas
    entry_sin_bordes(NOMBRES_ENTRY)

    GRADO_LABEL = tk.Label(frame_izquierdo, text="GRADO", font=fuente_personalizada)
    GRADO_LABEL.grid(row=6, column=3, sticky="w", padx=50, pady=1)
    GRADO_ENTRY = tk.Entry(frame_izquierdo)
    GRADO_ENTRY.grid(row=7, column=3, columnspan=3, sticky="ew", padx=50, pady=1)  # Ampliamos el Entry a 3 columnas
    entry_sin_bordes(GRADO_ENTRY)

    #FALLAS_LABEL = tk.Label(nueva_ventana, text="FALLAS:")
    #FALLAS_LABEL.pack()
    #FALLAS_ENTRY = tk.Entry(nueva_ventana)
    #FALLAS_ENTRY.pack()

    def insertar_alumno():
        # Obtener los valores ingresados por el usuario
        id = id_entry.get()
        APELLIDOS = APELLIDOS_ENTRY.get()
        NOMBRES = NOMBRES_ENTRY.get()
        GRADO = GRADO_ENTRY.get()
        #FALLAS = FALLAS_ENTRY.get()
        #cantidad = cantidad_entry.get()

        # Obtener el valor de cantidad como cadena
        #fallas_str = FALLAS_ENTRY.get()
        # Verificar si el ID ya existe en la base de datos

        materias_predeterminadas = [
            {"materia": "Naturales", "falla": 0},
            {"materia": "Sociales", "falla": 0},
            {"materia": "Matematicas", "falla": 0},
            {"materia": "Ed Fisica", "falla": 0},
            {"materia": "Español", "falla": 0},
            {"materia": "Religion", "falla": 0},
            {"materia": "Etica", "falla": 0},
            {"materia": "Ingles", "falla": 0},
            {"materia": "Informatica", "falla": 0},
            {"materia": "Artistica", "falla": 0},

        ]
        # Esto asegura que cada estudiante tenga su propia lista de materias con fallas en 0
        fallas_predeterminadas = [{"materia": materia["materia"], "falla": 0} for materia in materias_predeterminadas]
        
        if not id:
            print("El campo ID no puede estar vacío")
            messagebox.showerror("Error", "El campo ID no puede estar vacio.")
            return
        if estudiante.find_one({"_id": id}):
            print(f"El ID {id} ya existe en la base de datos")
            messagebox.showerror("Error", f"El ID {id} ya existe en la base de datos")
            return
        
        
        # Verificar si fallas_str se puede convertir a un número
        #try:
        #    FALLAS = int(fallas_str)  # Convertir a entero
        #except ValueError:
        #    print("El campo Cantidad debe ser un número entero")
        #    return

        # Crear un diccionario con los valores ingresados
        nuevo_estudiante = {
            "_id": id,
            "APELLIDOS": APELLIDOS,
            "NOMBRES": NOMBRES,
            "GRADO": GRADO,
            "FALLAS": fallas_predeterminadas
        }

        # Insertar el documento en la base de datos
        resultado = estudiante.insert_one(nuevo_estudiante)
        messagebox.showinfo("Excelente", "Alumno insertado correctamente")
        print("Documento insertado:", resultado.inserted_id)
        # Limpiar los campos de entrada
        id_entry.delete(0, 'end')
        APELLIDOS_ENTRY.delete(0, 'end')
        NOMBRES_ENTRY.delete(0, 'end')
        GRADO_ENTRY.delete(0, 'end')
        #FALLAS_ENTRY.delete(0, 'end')

    boton5 = tk.Button(frame_izquierdo, text="Agregar", command=insertar_alumno)
    boton5.grid(row=8,column=3, padx=50, pady=15)
    entry_sin_bordess(boton5, width=30)

    # Centrar la ventana en la pantalla <<<ancho/largo>>>
    center_window(nueva_ventana, 400, 250)
    # Deshabilitar el redimensionamiento de la ventana
    nueva_ventana.resizable(False, False)
    
def obtener_datos(tabla,grado):
    
    # Obtener todos los documentos de la base de datos
    resultados = estudiante.find()

    # Limpiar la tabla antes de agregar nuevos datos
    for item in tabla.get_children():
        tabla.delete(item)

    # Insertar los datos obtenidos en la tabla
    for resultado in resultados:
        if resultado.get('GRADO') == grado:
            # Calcular la suma de las fallas
            fallas = resultado.get('FALLAS', [])
            suma_fallas = sum(int(falla.get('falla', 0)) for falla in fallas)  # Convertir a entero

            tabla.insert('', tk.END, text='', values=(
                resultado.get('_id', ''),
                resultado.get('APELLIDOS', ''),
                resultado.get('NOMBRES', ''),
                resultado.get('GRADO', ''),
                #resultado.get('FALLAS', '')
                suma_fallas
            ))

def obtener_datos_totales(tabla, grado):
    # Obtener todos los documentos de la base de datos
    resultados = estudiante.find()

    # Limpiar la tabla antes de agregar nuevos datos
    for item in tabla.get_children():
        tabla.delete(item)

    # Insertar los datos obtenidos en la tabla
    for resultado in resultados:
        if resultado.get('GRADO') == grado:
            # Obtener las fallas por materia
            fallas = resultado.get('FALLAS', [])
            total_fallas = 0

            # Crear un diccionario temporal para las fallas por materia
            fallas_por_materia = {falla.get('materia'): int(falla.get('falla', 0)) for falla in fallas}

            for materia in materias:
                total_fallas += fallas_por_materia.get(materia, 0)

            tabla.insert('', tk.END, text='',
                         values=(resultado.get('_id', ''),
                                 resultado.get('APELLIDOS', ''),
                                 resultado.get('NOMBRES', ''),
                                 resultado.get('GRADO', ''),
                                 # Resultados de las fallas por materia
                                 fallas_por_materia.get('Naturales', 0),
                                 fallas_por_materia.get('Sociales', 0),
                                 fallas_por_materia.get('Matematicas', 0),
                                 fallas_por_materia.get('Ed Fisica', 0),
                                 fallas_por_materia.get('Español', 0),
                                 fallas_por_materia.get('Religion', 0),
                                 fallas_por_materia.get('Etica', 0),
                                 fallas_por_materia.get('Ingles', 0),
                                 fallas_por_materia.get('Informatica', 0),
                                 fallas_por_materia.get('Artistica', 0),
                                 # Total de fallas
                                 total_fallas
                                 ))
def eliminar_alumno():
    # Crear una nueva ventana
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Eliminar Alumno")
    nueva_ventana.geometry("300x200")

    #tipo de lectra
    fuente_personalizada = tkFont.Font(family="Century Gothic", size=4)

    # Crear los frames o separaciones de la ventana
    frame_izquierdo0 = tk.Frame(nueva_ventana, bg="#750b53")
    frame_izquierdo = tk.Frame(nueva_ventana)
    frame_derecho = tk.Frame(nueva_ventana, bg="#750b53")
    # Ubicar los frames en la ventana
    frame_izquierdo0.pack(side="left", fill="both")
    frame_izquierdo0.config(width=20)
    frame_izquierdo.pack(side="left", fill="both", expand=True)
    frame_derecho.pack(side="left", fill="both")
    frame_derecho.config(width=20)

    id_label = tk.Label(frame_izquierdo, text="ID", font=fuente_personalizada)
    id_label.grid(row=0, column=3, sticky="w", padx=25, pady=1)
    id_entry = tk.Entry(frame_izquierdo)
    id_entry.grid(row=1, column=3, sticky="ew", padx=25, pady=1) 
    entry_sin_bordes(id_entry)  

    def eliminar_alumno():
        # Obtener los valores ingresados por el usuario
        id = id_entry.get()

        if not id:
            print("El campo ID no puede estar vacío")
            return
        # Crear un diccionario con los valores ingresados
        nuevo_alumno = {
            "_id": id,
        }
        # Insertar el documento en la base de datos
        resultado =estudiante.delete_one(nuevo_alumno)
        #print("Documento eliminado:", resultado)
        # Limpiar los campos de entrada
        id_entry.delete(0, 'end')     
    boton5 = tk.Button(frame_izquierdo, text="Eliminar", command=eliminar_alumno)
    boton5.grid(row=8,column=3, padx=25, pady=15)
    entry_sin_bordess(boton5, width=30)

    # Centrar la ventana en la pantalla
    center_window(nueva_ventana, 325, 200)
    # Deshabilitar el redimensionamiento de la ventana
    nueva_ventana.resizable(False, False)

def agregar_falla():
    # Cerrar la ventana principal
    #ventana.destroy()
    
    #crear nueva ventana
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Agregar Falla")
    nueva_ventana.geometry("300x200")

    #tipo de lectra
    fuente_personalizada = tkFont.Font(family="Century Gothic", size=4)

    # Crear los frames o separaciones de la ventana
    frame_izquierdo0 = tk.Frame(nueva_ventana, bg="#750b53")
    frame_izquierdo = tk.Frame(nueva_ventana)
    frame_derecho = tk.Frame(nueva_ventana, bg="#750b53")
    # Ubicar los frames en la ventana
    frame_izquierdo0.pack(side="left", fill="both")
    frame_izquierdo0.config(width=20)
    frame_izquierdo.pack(side="left", fill="both", expand=True)
    frame_derecho.pack(side="left", fill="both")
    frame_derecho.config(width=20)

    id_label = tk.Label(frame_izquierdo, text="ID ALUMNO", font=fuente_personalizada)
    id_label.grid(row=0, column=3, sticky="w", padx=25, pady=1)
    id_entry = tk.Entry(frame_izquierdo)
    id_entry.grid(row=1, column=3, sticky="ew", padx=25, pady=1) 
    entry_sin_bordes(id_entry) 


    def agregra_fallas():
        # Obtener la fecha actual
        fecha_actual = datetime.utcnow()

        id = id_entry.get()
        if not id:
            print("El campo ID ALUMNO no puede estar vacío")
            messagebox.showerror("Error", "El campo ID ALUMNO no puede estar vacio.")
            return
          
        nueva_falla = {
            'fecha':fecha_actual,
        }
        if fecha_actual.weekday() == 0:  # 0: Lunes
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Sociales", "falla": 1},
                {"materia": "Naturales", "falla": 2},
                {"materia": "Matematicas", "falla": 2},
            ]
        elif fecha_actual.weekday() == 1:  # 1: Martes
            # Agregar una falla a las materias específicas para el martes
            materias_fallas = [
                {"materia": "Ed Fisica", "falla": 1},
                {"materia": "Matematicas", "falla": 1},
                {"materia": "Español", "falla": 1},
                {"materia": "Religion", "falla": 1},
                {"materia": "Etica", "falla": 1},
            ]
        elif fecha_actual.weekday() == 2:  # 2: Miercoles
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Naturales", "falla": 1},
                {"materia": "Español", "falla": 2},
                {"materia": "Sociales", "falla": 2},
            ]
        elif fecha_actual.weekday() == 3:  # 3: Jueves
            # Agregar una falla a las materias específicas para el martes
            materias_fallas = [
                {"materia": "Ingles", "falla": 1},
                {"materia": "Informatica", "falla": 1},
                {"materia": "Ed Fisica", "falla": 1},
                {"materia": "Matematicas", "falla": 2}
            ]        
        elif fecha_actual.weekday() == 4:  # 4: Viernes
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Naturales", "falla": 1},
                {"materia": "Español", "falla": 2},
                {"materia": "Artistica", "falla": 2},
            ]
        else:
            # Si no es lunes ni martes, no se agregan fallas
            print("Solo puedes agregar fallas de lunes a Viernes.")
            messagebox.showerror("Error", "Solo puedes agregar fallas de lunes a Viernes.")
            return
        # Verificar que el alumno exista en la base de datos
        alumno = estudiante.find_one({"_id": id})
        if not alumno:
            print("El ID ALUMNO ingresado no existe en la base de datos.")
            messagebox.showerror("Error","El ID ALUMNO ingresado no existe en la base de datos.")
            return
        
        # Agregar las fallas a las materias correspondientes
        for materia_falla in materias_fallas:
            # Verificar si la materia existe en el estudiante
            materia = materia_falla['materia']
            falla = materia_falla['falla']
            if not any(materia == materia_item['materia'] for materia_item in alumno['FALLAS']):
                # Si la materia no existe, se agrega al estudiante
                estudiante.update_one(
                    {"_id": id},
                    {"$push": {"FALLAS": {"materia": materia, "falla": falla}}}
                )
            else:
                # Si la materia ya existe, se actualiza la cantidad de fallas
                estudiante.update_one(
                    {"_id": id, "FALLAS.materia": materia},
                    {"$inc": {"FALLAS.$.falla": falla}}
                )
           

        print("Falla agregada correctamente")
        messagebox.showinfo("Excelente", "Falla Agregada correctamente")
        
        # Limpiar los campos de entrada
        id_entry.delete(0, 'end')
        # Botón para agregar la falla
    agregar_button = tk.Button(frame_izquierdo, text="Agregar Falla", command=agregra_fallas)
    agregar_button.grid(row=8,column=3, padx=25, pady=15)
    entry_sin_bordess(agregar_button, width=30)

    # Centrar la ventana en la pantalla
    center_window(nueva_ventana, 325, 200)
    # Deshabilitar el redimensionamiento de la ventana
    nueva_ventana.resizable(False, False)

def eliminar_falla():
    #crear ventana
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Eliminar falla")
    nueva_ventana.geometry("300x200")
    # Centrar la ventana en la pantalla
    center_window(nueva_ventana, 300, 300)
    # Deshabilitar el redimensionamiento de la ventana
    nueva_ventana.resizable(False, False)
def fallas_globales():
    #crear ventana
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Fallas Materias")
    nueva_ventana.geometry("900x500")

    #tipo de lectra
    fuente_personalizada = tkFont.Font(family="Century Gothic", size=4)

    # Crear los frames o separaciones de la ventana
    frame_superior = tk.Frame(nueva_ventana, bg="#750b53")
    frame_inferior = tk.Frame(nueva_ventana)

    # Ubicar los frames en la ventana
    frame_superior.grid(row=0, column=0, sticky="ew")
    frame_inferior.grid(row=1, column=0, sticky="nsew")

    # Configurar que el frame inferior se expanda con la ventana
    nueva_ventana.grid_rowconfigure(1, weight=1)
    nueva_ventana.grid_columnconfigure(0, weight=1)

    grado_label = tk.Label(frame_superior, text="GRADO", bg="#750b53", fg="#FFFFFF", font=fuente_personalizada)  # Color de texto blanco
    grado_label.grid(row=0, column=0, padx=10, pady=20)
    grado = tk.Entry(frame_superior, bg="#FFFFFF")  # Fondo blanco
    grado.grid(row=0, column=1, padx=10, pady=5) 
    entry_sin_bordes(grado)
    
    # Crear la tabla Treeview en el frame derecho
    tabla = ttk.Treeview(frame_inferior)  
    tabla['columns'] = ('ID', 'APELLIDOS', 'NOMBRES', 'GRADO', 'NATU', 'SOCI', 'MATE', 'ED.FIS', 'ESP', 'RELIG', 'ETI', 'INGL', 'INFOR', 'ART', 'FALLAS')    
    boton6 = tk.Button(frame_superior, text="Buscar", command=lambda tabla=tabla, grado=grado: obtener_datos_totales(tabla, grado.get()))
    boton6.grid(row=0, column=2, padx=2, pady=5, columnspan=2)
    entry_sin_bordesss(boton6, width=10)

    # Formatear las columnas
    tabla.column('#0', width=0, stretch=tk.NO)  # Columna oculta
    tabla.column('ID', anchor=tk.CENTER, width=2)
    tabla.column('APELLIDOS', anchor=tk.CENTER, width=100)
    tabla.column('NOMBRES', anchor=tk.CENTER, width=100)
    tabla.column('GRADO', anchor=tk.CENTER, width=20)
    tabla.column('NATU', anchor=tk.CENTER, width=10)
    tabla.column('SOCI', anchor=tk.CENTER, width=10)
    tabla.column('MATE', anchor=tk.CENTER, width=10)
    tabla.column('ED.FIS', anchor=tk.CENTER, width=10)
    tabla.column('ESP', anchor=tk.CENTER, width=10)
    tabla.column('RELIG', anchor=tk.CENTER, width=10)
    tabla.column('ETI', anchor=tk.CENTER, width=10)
    tabla.column('INGL', anchor=tk.CENTER, width=10)
    tabla.column('INFOR', anchor=tk.CENTER, width=10)
    tabla.column('ART', anchor=tk.CENTER, width=10)
    tabla.column('FALLAS', anchor=tk.CENTER, width=20)

    # Agregar encabezados de columna
    tabla.heading('#0', text='')
    tabla.heading('ID', text='ID')
    tabla.heading('APELLIDOS', text='APELLIDOS')
    tabla.heading('NOMBRES', text='NOMBRES')
    tabla.heading('GRADO', text='GRADO')
    tabla.heading('NATU', text='NATU')
    tabla.heading('SOCI', text='SOCI')
    tabla.heading('MATE', text='MATE')
    tabla.heading('ED.FIS', text='ED.FIS')
    tabla.heading('ESP', text='ESP')
    tabla.heading('RELIG', text='RELIG')
    tabla.heading('ETI', text='ETI')
    tabla.heading('INGL', text='INGL')
    tabla.heading('INFOR', text='INFOR')
    tabla.heading('ART', text='ART')
    tabla.heading('FALLAS', text='TOTAL')

    # Ubicar la tabla en el frame derecho
    tabla.pack(fill="both", expand=True)

    # Centrar la ventana en la pantalla
    center_window(nueva_ventana, 900, 500)
    nueva_ventana.resizable(False, False)

def fallas_manuales():
    nueva_ventana = tk.Tk()
    nueva_ventana.title("Fallas Manuales")
    nueva_ventana.geometry("300x200")

    #tipo de lectra
    fuente_personalizada = tkFont.Font(family="Century Gothic", size=4)

    # Crear los frames o separaciones de la ventana
    frame_izquierdo0 = tk.Frame(nueva_ventana, bg="#750b53")
    frame_izquierdo = tk.Frame(nueva_ventana)
    frame_derecho = tk.Frame(nueva_ventana, bg="#750b53")
    # Ubicar los frames en la ventana
    frame_izquierdo0.pack(side="left", fill="both")
    frame_izquierdo0.config(width=20)
    frame_izquierdo.pack(side="left", fill="both", expand=True)
    frame_derecho.pack(side="left", fill="both")
    frame_derecho.config(width=20)

    id_label = tk.Label(frame_izquierdo, text="ID", font=fuente_personalizada)
    id_label.grid(row=0, column=3, sticky="w", padx=25, pady=1)
    id_entry = tk.Entry(frame_izquierdo)
    id_entry.grid(row=1, column=3, sticky="ew", padx=25, pady=1) 
    entry_sin_bordes(id_entry) 

    # Agregar un Combobox para que el usuario seleccione el día de la semana
    dia_label = tk.Label(frame_izquierdo, text="Dia de Falla", font=fuente_personalizada)
    dia_label.grid(row=2, column=3, sticky="w", padx=25, pady=1)
    dia_var = tk.StringVar()
    dia_combobox = ttk.Combobox(frame_izquierdo, textvariable=dia_var, values=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'])
    dia_combobox.grid(row=3, column=3, sticky="ew", padx=25, pady=1)
    


    def agregra_fallas():
        dia_str = dia_combobox.current()  # Obtener el índice del día seleccionado
        if dia_str == -1:  # Si no se ha seleccionado ningún día
            print("Debes seleccionar un día de la semana")
            messagebox.showerror("Error", "Debes seleccionar un día de la semana")
            return 
        
        # Obtener el número correspondiente al día seleccionado
        dias_semana = {'Lunes': 1, 'Martes': 2, 'Miércoles': 3, 'Jueves': 4, 'Viernes': 5}
        dia_str = dia_combobox.get()  # Obtener el día seleccionado como cadena
        dia_fecha = dias_semana[dia_str]     
        id = id_entry.get()

        if not id:
            print("El campo ID ALUMNO no puede estar vacío")
            return

        if dia_fecha == 1:  # 1: Lunes
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Sociales", "falla": 1},
                {"materia": "Naturales", "falla": 2},
                {"materia": "Matematicas", "falla": 2},
            ]
        elif dia_fecha == 2:  # 2: Martes
            # Agregar una falla a las materias específicas para el martes
            materias_fallas = [
                {"materia": "Ed Fisica", "falla": 1},
                {"materia": "Matematicas", "falla": 1},
                {"materia": "Español", "falla": 1},
                {"materia": "Religion", "falla": 1},
                {"materia": "Etica", "falla": 1},
            ]
        elif dia_fecha == 3:  # 3: Miercoles
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Naturales", "falla": 1},
                {"materia": "Español", "falla": 2},
                {"materia": "Sociales", "falla": 2},
            ]
        elif dia_fecha == 4:  # 4: Jueves
            # Agregar una falla a las materias específicas para el martes
            materias_fallas = [
                {"materia": "Ingles", "falla": 1},
                {"materia": "Informatica", "falla": 1},
                {"materia": "Ed Fisica", "falla": 1},
                {"materia": "Matematicas", "falla": 2}
            ]        
        elif dia_fecha == 5:  # 5: Viernes
            # Agregar una falla a las materias específicas para el lunes
            materias_fallas = [
                {"materia": "Naturales", "falla": 1},
                {"materia": "Español", "falla": 2},
                {"materia": "Artistica", "falla": 2},
            ]
        else:
            # Si no es lunes ni martes, no se agregan fallas
            print("Solo puedes agregar fallas de lunes a Viernes.")
            messagebox.showerror("Error", "Solo puedes agregar fallas de lunes a Viernes.")
            return
        # Verificar que el alumno exista en la base de datos
        alumno = estudiante.find_one({"_id": id})
        if not alumno:
            print("El ID ALUMNO ingresado no existe en la base de datos.")
            messagebox.showerror("Error","El ID ALUMNO ingresado no existe en la base de datos.")
            return
        
        # Agregar las fallas a las materias correspondientes
        for materia_falla in materias_fallas:
            # Verificar si la materia existe en el estudiante
            materia = materia_falla['materia']
            falla = materia_falla['falla']
            if not any(materia == materia_item['materia'] for materia_item in alumno['FALLAS']):
                # Si la materia no existe, se agrega al estudiante
                estudiante.update_one(
                    {"_id": id},
                    {"$push": {"FALLAS": {"materia": materia, "falla": falla}}}
                )
            else:
                # Si la materia ya existe, se actualiza la cantidad de fallas
                estudiante.update_one(
                    {"_id": id, "FALLAS.materia": materia},
                    {"$inc": {"FALLAS.$.falla": falla}}
                )
           

        print("Falla agregada correctamente")
        messagebox.showinfo("Excelente", "Falla Agregada correctamente")
        
        # Limpiar los campos de entrada
        id_entry.delete(0, 'end')
        # Botón para agregar la falla
    agregar_button = tk.Button(frame_izquierdo, text="Agregar Falla", command=agregra_fallas)
    agregar_button.grid(row=8,column=3, padx=25, pady=15)
    entry_sin_bordess(agregar_button, width=30)

    center_window(nueva_ventana, 325, 200)
    nueva_ventana.resizable(False, False)
def salir():
    ventana.quit()  



 
ventana_video = None  # Variable global para almacenar la ventana de video
video_frames = []     # Lista global para mantener los frames del video

def mostrar_ventana_principal():
    ventana.deiconify()

def cerrar_ventana_video():
    global ventana_video
    ventana_video.destroy()
    mostrar_ventana_principal()

def reproducir_video():
    ruta_video = "vid.mp4"  # Reemplaza "ruta_del_video.mp4" con la ruta correcta del video
    global video, label_video, ventana_video, video_frames
    video = VideoFileClip(ruta_video)
    video_frames = list(video.iter_frames(fps=int(video.fps)))  # Convertir los frames del video en una lista

    ventana.withdraw()  # Ocultar la ventana principal mientras se muestra el video

    ventana_video = tk.Toplevel(ventana)
    ventana_video.title("Registro y Control")
    ventana_video.geometry("800x600")
    ventana_video.overrideredirect(True)  # Establecer la ventana sin botones de control

    label_video = tk.Label(ventana_video)
    label_video.pack()

    ventana_video.protocol("WM_DELETE_WINDOW", cerrar_ventana_video)

    center_window(ventana_video, 625, 600)
    ventana_video.resizable(False, False)

    mostrar_frame()  # Llamar a la función que muestra los frames

def mostrar_frame():
    global label_video, video_frames
    if video_frames:
        frame = video_frames.pop(0)  # Obtener el primer frame de la lista
        frame_img = ImageTk.PhotoImage(Image.fromarray(frame))
        label_video.config(image=frame_img)
        label_video.image = frame_img
        ventana.after(int(1000 // video.fps), mostrar_frame)  # Convertir el retardo a entero
    else:
        ventana.after(1000, cerrar_ventana_video)

def main():
    global ventana, video, label_video
       
    # Liberar el bloqueo modal y cerrar la ventana secundaria
    ventana = tk.Tk()   
    ventana.title("Registro y Control")
    ventana.geometry("800x600")

    reproducir_video() 

    # Crear los frames o separaciones de la ventana
    frame_superior = tk.Frame(ventana, bg="#750b53")
    frame_izquierdo = tk.Frame(ventana)
    frame_derecho = tk.Frame(ventana, bg="#750b53")
    # Ubicar los frames en la ventana
    frame_superior.pack(side="top", fill="both")
    frame_superior.config(height=20)
    frame_izquierdo.pack(side="left", fill="both", expand=True)
    frame_derecho.pack(side="left", fill="both", expand=True)

    def refrescar():
        ventana.destroy()
        main()

    #menu = tk.Menu(ventana)
    # Agregar opciones al menú
    #menu.add_command(label="Agregar Alumno", command=agregar_alumno)
    #menu.add_command(label="Eliminar Alumno", command=eliminar_alumno)
    #menu.add_command(label="Agregar Falla", command=agregar_falla)
    #menu.add_command(label="Agregar Falla Pasadas", command=fallas_manuales)
    #menu.add_command(label="Eliminar Falla", command=eliminar_falla)
    #menu.add_command(label="Fallas Globales", command=fallas_globales)
    #menu.add_command(label="Refrecar", command=refrescar)    
    #menu.add_command(label="Salir", command=salir)
    #ventana.config(menu=menu)

    # Crear la tabla Treeview en el frame derecho
    tabla = ttk.Treeview(frame_izquierdo)  
    tabla['columns'] = ('ID', 'APELLIDOS', 'NOMBRES', 'GRADO', 'FALLAS')
    # Formatear las columnas
    tabla.column('#0', width=0, stretch=tk.NO)  # Columna oculta
    tabla.column('ID', anchor=tk.CENTER, width=10)
    tabla.column('APELLIDOS', anchor=tk.CENTER, width=200)
    tabla.column('NOMBRES', anchor=tk.CENTER, width=200)
    tabla.column('GRADO', anchor=tk.CENTER, width=100)
    tabla.column('FALLAS', anchor=tk.CENTER, width=120)
    # Agregar encabezados de columna
    tabla.heading('#0', text='')
    tabla.heading('ID', text='ID')
    tabla.heading('APELLIDOS', text='APELLIDOS')
    tabla.heading('NOMBRES', text='NOMBRES')
    tabla.heading('GRADO', text='GRADO')
    tabla.heading('FALLAS', text='FALLAS TOTALES')
    # Ubicar la tabla en el frame derecho
    tabla.pack(fill="both", expand=True)

    # Utilizando grid en el frame_derecho
    #grado_label = tk.Label(frame_derecho, text="GRADO:", fg="white", bg=frame_derecho.cget('bg'))
    #grado_label.grid(row=0, column=0, padx=10, pady=10)

    #grado = tk.Entry(frame_derecho)
    #grado.grid(row=0, column=1, padx=10, pady=10)

    #boton6 = tk.Button(frame_derecho, text="Buscar", command=lambda: obtener_datos(tabla, grado.get()), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    #boton6.grid(row=0, column=2, padx=10, pady=10)

    
    grado = "1"
    obtener_datos(tabla, grado)

    # Carga la imagen que deseas utilizar en el botón
    imagen6 = PhotoImage(file="e-.png")
    label6_imagen = tk.Label(frame_derecho, image=imagen6, bg="#750b53", compound="right")
    label6_imagen.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

    imagen1 = PhotoImage(file="1.png")
    label1_imagen = tk.Label(frame_derecho, image=imagen1, bg="#750b53", compound="right")
    label1_imagen.grid(row=2, column=1, padx=5, pady=5)

    imagen2 = PhotoImage(file="2.png")
    label2_imagen = tk.Label(frame_derecho, image=imagen2, bg="#750b53", compound="right")
    label2_imagen.grid(row=3, column=1, padx=5, pady=5)

    imagen3 = PhotoImage(file="3.png")
    label3_imagen = tk.Label(frame_derecho, image=imagen3, bg="#750b53", compound="right")
    label3_imagen.grid(row=4, column=1, padx=5, pady=5)

    imagen4 = PhotoImage(file="4.png")
    label4_imagen = tk.Label(frame_derecho, image=imagen4, bg="#750b53", compound="right")
    label4_imagen.grid(row=5, column=1, padx=5, pady=5)

    imagen5 = PhotoImage(file="10.png")
    label5_imagen = tk.Label(frame_derecho, image=imagen5, bg="#750b53", compound="right")
    label5_imagen.grid(row=6, column=1, padx=5, pady=5)

    imagen = PhotoImage(file="6.png")
    label_imagen = tk.Label(frame_derecho, image=imagen, bg="#750b53", compound="right")
    label_imagen.grid(row=7, column=1, padx=5, pady=5)

    def cambiar_cursor(event):
        boton7.config(cursor="hand2")
        boton8.config(cursor="hand2")
        boton9.config(cursor="hand2")
        boton10.config(cursor="hand2")
        boton11.config(cursor="hand2")
        boton12.config(cursor="hand2")

    def restaurar_cursor(event):
        boton7.config(cursor="")
        boton8.config(cursor="")
        boton9.config(cursor="")
        boton10.config(cursor="")
        boton11.config(cursor="")
        boton12.config(cursor="")

    fuente_personalizada = tkFont.Font(family="Century Gothic", size=10)
    
    boton7 = tk.Button(frame_derecho, text="Agregar Alumno", command=lambda: agregar_alumno(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton7['font'] = fuente_personalizada
    boton7.grid(row=2, column=0, padx=10, pady=10, sticky='e')

    boton8 = tk.Button(frame_derecho, text="Eliminar Alumno", command=lambda: eliminar_alumno(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton8['font'] = fuente_personalizada
    boton8.grid(row=3, column=0, padx=10, pady=10, sticky='e')

    boton9 = tk.Button(frame_derecho, text="Agregar Falla", command=lambda: agregar_falla(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton9['font'] = fuente_personalizada
    boton9.grid(row=4, column=0, padx=10, pady=10, sticky='e')

    boton10 = tk.Button(frame_derecho, text="Agregar Falla Pasadas", command=lambda: fallas_manuales(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton10['font'] = fuente_personalizada
    boton10.grid(row=5, column=0, padx=10, pady=10, sticky='e')

    boton12 = tk.Button(frame_derecho, text="Fallas Globales", command=lambda: fallas_globales(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton12['font'] = fuente_personalizada
    boton12.grid(row=6, column=0, padx=5, pady=5, sticky='e')

    boton11 = tk.Button(frame_derecho, text="Refrescar", command=lambda: refrescar(), bg="#750b53", fg="white", borderwidth=0, highlightthickness=0)
    boton11['font'] = fuente_personalizada
    boton11.grid(row=7, column=0, padx=10, pady=10, sticky='e')    

    # Vincular eventos del cursor al botón
    boton7.bind("<Enter>", cambiar_cursor)
    boton7.bind("<Leave>", restaurar_cursor)
    boton8.bind("<Enter>", cambiar_cursor)
    boton8.bind("<Leave>", restaurar_cursor)
    boton9.bind("<Enter>", cambiar_cursor)
    boton9.bind("<Leave>", restaurar_cursor)
    boton10.bind("<Enter>", cambiar_cursor)
    boton10.bind("<Leave>", restaurar_cursor)
    boton11.bind("<Enter>", cambiar_cursor)
    boton11.bind("<Leave>", restaurar_cursor)
    boton12.bind("<Enter>", cambiar_cursor)
    boton12.bind("<Leave>", restaurar_cursor)



    # Centrar la ventana en la pantalla
    center_window(ventana, 900, 500)
    # Deshabilitar el redimensionamiento de la ventana
    ventana.resizable(False, False)
    # Iniciar el bucle de la aplicación
    ventana.mainloop()

    

if __name__ == "__main__":
    main()