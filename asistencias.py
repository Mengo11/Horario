import tkinter as tk
from tkinter import *
from tkinter import messagebox
from CompletarAU import AutocompleteEntry
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import re, os, sys
from ttkthemes import ThemedStyle
import Ver_asistencia2# Importamos el archivo Ver_asistencia2.py
import cargar_asistencia

class clase_asistencias:
    def __init__(self, tk, menuFunc, tipoCuenta, nombreCuenta):
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

        self.ventana_asistencias = tk
        tk.title("Administrar Asistencias")
        self.path = resource_path("Imagenes/Colegio_logo.ico")
        self.ventana_asistencias.iconbitmap(self.path)
        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.menuFunc = menuFunc

        BGcolor = "#98c1d9"  # Color de fondo
        BG2color = "#4A90E2"  # Color de fondo del footer
        BG3color = "#1b284f"
        color_fondo = self.ventana_asistencias.cget("bg")
        new_color = BGcolor if color_fondo != BG3color else BG3color
        color_label = BGcolor if new_color == BGcolor else BG3color
        nuevo_color = BG2color if new_color == BGcolor else "black"

        self.ventana_asistencias.grid_columnconfigure(0, weight=1)
        self.ventana_asistencias.grid_rowconfigure(0, weight=1)
        self.imagen_ver_path = resource_path("imagenes/ver_asistencia.png")
        imagen_volver_path = resource_path("imagenes/volver.png")
        self.imagen_cargar_m_path = resource_path("imagenes/cargar_asistencia_m.png")
        self.imagen_cargar_a_path = resource_path("imagenes/carga_auto.png")

        self.imagen_ver_asistencia = ImageTk.PhotoImage(Image.open(self.imagen_ver_path).resize((20, 20)))
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        self.imagen_cargar_m = ImageTk.PhotoImage(Image.open(self.imagen_cargar_m_path).resize((20, 20), Image.LANCZOS))
        self.imagen_cargar_a = ImageTk.PhotoImage(Image.open(self.imagen_cargar_a_path).resize((20, 20), Image.LANCZOS))

        BG2 = Frame(self.ventana_asistencias, bg=nuevo_color, width=512, height=32)
        BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
        self.etiqueta_bienvenida = Label(self.ventana_asistencias, text="Pestaña de administrar asistencias", bg=color_label, fg="white" if color_label == BG3color else "black", font=("Monaco", 24, "bold"))
        self.etiqueta_bienvenida.place(relx=0.5, rely=0.1, anchor='n')

        # Botón para ver la asistencia de los alumnos
        self.ver_asistencia = Button(self.ventana_asistencias, text="Ver asistencia de alumnos", image=self.imagen_ver_asistencia, compound="left", relief="solid", borderwidth=0, height=35, width=430, font=("Helvetica", 16),
                                     command=self.abrir_ver_asistencias)  # Cambiado aquí para abrir Ver_asistencia2.py
        self.ver_asistencia.grid(row=5, column=3, columnspan=2, padx=(0, 10), pady=(0, 0), sticky="E")

        self.cargar_asistencia = Button(self.ventana_asistencias, text="Cargar asistencias de alumnos manual", image=self.imagen_cargar_m, compound="left", borderwidth=0, relief="solid", height=35, width=430, font=("Helvetica", 16), command=self.abrir_cargar_asistencia)
        self.cargar_asistencia.grid(row=3, column=3, columnspan=2, padx=(0, 10), pady=(0, 0), sticky="E")
        
        self.boton_volver = Button(self.ventana_asistencias, text="Volver", image=self.imagen_volver, compound="left", height=30, width=430, borderwidth=0, relief="solid", command=lambda: self.volver_al_menu(menuFunc, tipoCuenta, nombreCuenta))
        self.boton_volver.grid(row=8, column=4, columnspan=2, padx=(0, 10), pady=(0, 0))

        etiqueta_derecha = Label(BG2, text="©6°5 - 2024", fg="white", bg=nuevo_color, font=("Helvetica", 16))
        etiqueta_derecha.place(relx=1.0, rely=0.5, anchor='e')

        etiqueta_izquierda = Label(BG2, text="", bg=nuevo_color, fg="white", font=("Helvetica", 16))
        etiqueta_izquierda.place(relx=0.0, rely=0.5, anchor='w')

        for elemento in self.ventana_asistencias.winfo_children():
            if isinstance(elemento, Button):
                elemento['bg'] = "white"
                elemento["borderwidth"] = 0
                changeOnHover(elemento, "#A2AEE0", "white")
        if tipoCuenta == 1:
            etiqueta_izquierda.config(text="Profesor")
        elif tipoCuenta == 2:
            etiqueta_izquierda.config(text="Preceptor")
        elif tipoCuenta == 3:
            etiqueta_izquierda.config(text="Administrador")
    
    def abrir_ver_asistencias(self):
        # Llamamos a la función del otro archivo Ver_asistencia2.py
        ventana_ver_asistencias = tk.Tk()  # Creamos una nueva ventana
        Ver_asistencia2.ver_asistencias(ventana_ver_asistencias, eliminar_b=1)
        ventana_ver_asistencias.mainloop()
    
    def abrir_cargar_asistencia(self):
        # Aquí importamos el archivo y creamos una nueva ventana para cargar la asistencia
          # Asegúrate de que la ruta del archivo sea correcta
        ventana_cargar_asistencia = tk.Toplevel(self.ventana_asistencias)  # Crea una ventana secundaria
        cargar_asistencia.ventana = ventana_cargar_asistencia  # Usa la ventana creada por Toplevel
        cargar_asistencia.ventana.mainloop()

    def eliminar(self):
        for elemento in self.ventana_asistencias.winfo_children():
            elemento.destroy()

    def volver_al_menu(self, menuFunc, tipoCuenta, nombreCuenta):
        self.eliminar()
        self.menuFunc(tipoCuenta, nombreCuenta)

if __name__ == "__main__":
    ventana_asistencias = tk.Tk()
    app = clase_asistencias(ventana_asistencias, None, 1, "Nombre")
    ventana_asistencias.mainloop()
