import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import re, os, sys
from Generar_qr_alumnos import Generar_Qr
from Ingresar_Asistencias_qr import Ingresar_Asistencias_qr
from ingresar_horario_entrada import horario_entrada_class

class clase_qr:
    def __init__(self, tk, menuFunc, tipoCuenta, nombreCuenta):
        def resource_path(relative_path):
            try:
                # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                # Si no se encuentra _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta del script
                base_path = os.path.abspath(".")
            # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
            return os.path.join(base_path, relative_path)

        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(
                background=colorOnHover))
        
            # background color on leaving widget
            button.bind("<Leave>", func=lambda e: button.config(
                background=colorOnLeave))

        self.ventana_qr = tk
        tk.title("QR")
        self.path = resource_path("Imagenes/Colegio_logo.ico")
        self.ventana_qr.iconbitmap(self.path)
        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.menuFunc = menuFunc

        BGcolor = "#98c1d9" #fondo de la palabra "qr"
        BG2color = "#4A90E2" #footer
        BG3color = "#1b284f"
        color_fondo = self.ventana_qr.cget("bg")
        new_color = BGcolor if color_fondo != BG3color else BG3color
        color_label = BGcolor if new_color == BGcolor else BG3color
        nuevo_color = BG2color if new_color == BGcolor else "black"  # Color de fondo de la pestaña

        self.ventana_qr.grid_columnconfigure(0, weight=1)
        self.ventana_qr.grid_rowconfigure(0, weight=1)
        self.imagen_ver_path = resource_path("imagenes/ver_asistencia.png")
        imagen_volver_path = resource_path("imagenes/volver.png")
        self.imagen_cargar_m_path = resource_path("imagenes/cargar_asistencia_m.png")
        self.imagen_cargar_a_path = resource_path("imagenes/carga_auto.png")
        self.imagen_horario_path = resource_path("imagenes/horario.png")

        self.imagen_horario=ImageTk.PhotoImage(Image.open(self.imagen_horario_path).resize((20, 20), Image.LANCZOS))
        self.imagen_ver_asistencia = ImageTk.PhotoImage(Image.open(self.imagen_ver_path).resize((20, 20)))
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        self.imagen_cargar_m = ImageTk.PhotoImage(Image.open(self.imagen_cargar_m_path).resize((20, 20), Image.LANCZOS))
        self.imagen_cargar_a = ImageTk.PhotoImage(Image.open(self.imagen_cargar_a_path).resize((20,20),Image.LANCZOS))

        BG2 = Frame(self.ventana_qr, bg=nuevo_color, width=512, height=32)
        BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
        self.etiqueta_bienvenida = Label(self.ventana_qr, text="Pestaña de QR",bg=color_label,fg="white" if color_label == BG3color else "black",  font=("Monaco", 24, "bold"))
        self.etiqueta_bienvenida.place(relx=0.5, rely=0.1, anchor='n')

        self.ver_asistencia = Button(self.ventana_qr, text="Generar QR alumnos", image=self.imagen_ver_asistencia,command= self.Generar_qr_alumno, compound="left", relief="solid",borderwidth=0, height=30, width=250, font=("Helvetica", 12))
        self.ver_asistencia.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="E")

        Button(self.ventana_qr,text="Ingresar horarios de llegada",image=self.imagen_horario,compound="left",command=self.ingresar_horarios_llegada, relief="solid",borderwidth=0, height=30, width=250, font=("Helvetica", 12)).grid(row=3, column=2,columnspan=2, padx=5, pady=5, sticky="E")
        self.cargar_asistencia = Button(self.ventana_qr, text="Cargar asistencia de alumnos(Manual)", image=self.imagen_cargar_m, compound="left",state="disabled",borderwidth=0, relief="solid", height=30, width=350, font=("Helvetica", 12))
        self.cargar_asistencia.grid(row=3, column=4, padx=5, pady=5, sticky="E")
        self.cargar_asistencia_a = Button(self.ventana_qr, text="Cargar asistencia de alumnos(Automatico)", image=self.imagen_cargar_a, command= self.cargar_asistencia_automatica,borderwidth=0, compound="left", relief="solid", height=30, width=350, font=("Helvetica", 12))
        self.cargar_asistencia_a.grid(row=5, column=4, padx=5, pady=5, sticky="E")
        self.boton_volver = Button(self.ventana_qr, text="Volver", image=self.imagen_volver, compound="left", height=25, width=200, borderwidth=0, relief="solid", command=lambda: self.volver_al_menu(menuFunc, tipoCuenta, nombreCuenta))
        self.boton_volver.grid(row=8, column=3, columnspan=2, padx=5, pady=5)

        etiqueta_derecha = Label(BG2, text="©6°5 - 2024",fg="white", bg=nuevo_color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=nuevo_color,fg="white",font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')

        for elemento in self.ventana_qr.winfo_children():
            if isinstance(elemento, Button):
                elemento['bg'] = "white"
                elemento["borderwidth"] = 0
                changeOnHover(elemento, "#A2AEE0", "white")

        if tipoCuenta==1:
            etiqueta_izquierda.config(text="Profesor")
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text="Preceptor")
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text="Administrador")
            
#----------------------------         [iNTERFAZ MENGONI Y SICILIANOS]         ----------------------------#
    def ingresar_horarios_llegada(self): 
        self.ventana_cursos = Toplevel(self.ventana_qr)
        
        # FONDO VENTANA QR COLOR #98c1d9
        self.ventana_cursos.geometry("850x400")  # Mantener tamaño fijo
        self.ventana_cursos.resizable(False, False)  # Deshabilitar el redimensionado
        self.ventana_cursos.configure(bg='#98c1d9')  # Establecer el fondo con el nuevo color

        self.ventana_cursos.columnconfigure(0, weight=1)
        self.ventana_cursos.rowconfigure(0, weight=1)
        self.ventana_cursos.rowconfigure(1, weight=1)

        self.frame_cursos = Frame(self.ventana_cursos, bg='#1a759f')  # Cambiar fondo del frame
        self.frame_cursos.grid(row=0, column=0, sticky="nsew")
        self.frame_divisiones = Frame(self.ventana_cursos, bg='#1a759f')  # Cambiar fondo del frame
        self.frame_divisiones.grid(row=1, column=0, sticky="nsew")

        # Botón para volver con estilo mejorado
        self.boton_volver = Button(self.ventana_cursos, text="Volver", command=self.ventana_cursos.destroy, height=2, width=15, font=("Helvetica", 12), relief="solid", bg="#FF6347", fg="white", activebackground="#FF4500", activeforeground="white")
        self.boton_volver.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # Configurar columnas y filas
        for x in range(1, 8):
            self.frame_cursos.columnconfigure(x-1, weight=1)
            
        for x in range(1, 7):
            self.frame_divisiones.columnconfigure(x-1, weight=1)
        
        self.frame_cursos.rowconfigure(0, weight=1)
        self.frame_divisiones.rowconfigure(0, weight=1)

        # Variables para almacenar selección
        self.curso_seleccionado = None
        self.division_seleccionada = None

        # Crear botones de cursos con estilo mejorado
        for x in range(1, 8):
            boton = Button(self.frame_cursos, text=f"{x}º", command=lambda x=x: self.actualizar_divisiones(x), height=2, width=6, font=("Helvetica", 12), relief="solid", bg="#A2AEE0", fg="white", activebackground="#1F4E79", activeforeground="white")
            boton.grid(row=0, column=x-1, sticky="nsew", padx=5, pady=5)

            if x == 1:  # Seleccionar el primer curso por defecto
                self.actualizar_divisiones(x)
        
        # Botón para ingresar al curso seleccionado con estilo mejorado
        self.boton_ingresar = Button(self.ventana_cursos, text="Ingresar al curso", command=self.ingresar_ventana_HL, bg="#A2AEE0", borderwidth=1, padx=30, height=2, width=15, font=("Helvetica", 12), relief="solid", activebackground="#1F4E79", activeforeground="white")
        self.boton_ingresar.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        
        # Label para mostrar el curso y división seleccionada
        self.label_seleccion = Label(self.ventana_cursos, text="Curso: " + str(self.curso_seleccionado) + " Division: " + str(self.division_seleccionada), font=("Helvetica", 12), bg='#98c1d9', fg="white")  # Cambiar color de fondo del label
        self.label_seleccion.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)




    def actualizar_label(self):
        Label(self.ventana_cursos, text="Curso:"+str(self.curso_seleccionado)+" Division:"+str(self.division_seleccionada)).grid(row=2, column=0, sticky="nsew")

    def actualizar_divisiones(self, curso):
        # Almacenar el curso seleccionado
        self.curso_seleccionado = curso

        # Limpia los botones actuales en frame_divisiones
        for widget in self.frame_divisiones.winfo_children():
            widget.destroy()

        # Si el curso es mayor a 3, mostrar divisiones numéricas
        if curso > 3:
            divisiones = range(1, 8)  # Números del 1 al 7
            self.division_seleccionada=1
        else:
            divisiones = ['A', 'B', 'C', 'D', 'E', 'F']  # Letras de la A a la E
            self.division_seleccionada='A'

        # Crear botones para las divisiones con tamaño reducido y separación
        for i, division in enumerate(divisiones):
            boton = Button(self.frame_divisiones, text=str(division), command=lambda d=division: self.seleccionar_division(d), height=2, width=6)
            boton.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        self.actualizar_label()

    def seleccionar_division(self, division):
        # Almacenar la división seleccionada
        self.division_seleccionada = division
        self.actualizar_label()

    def ingresar_ventana_HL(self):
        # Verificar que se haya seleccionado un curso y una división
        if self.curso_seleccionado is not None and self.division_seleccionada is not None:
            self.ventana_cursos.destroy()
            self.eliminar()
            horario_entrada_class(self.ventana_qr,self.menuFunc,self.tipocuenta,self.nombrecuenta,self.curso_seleccionado,self.division_seleccionada)
        else:
            print("Debe seleccionar un curso y una división antes de continuar.")
#-----------------------------------------------------
    def cargar_asistencia_automatica(self):
        self.eliminar()
        Ingresar_Asistencias_qr(self.ventana_qr,self.menuFunc,self.tipocuenta,self.nombrecuenta)

    def eliminar(self):
        for elemento in self.ventana_qr.winfo_children():
            elemento.destroy()

    def Generar_qr_alumno(self):
        self.eliminar()
        Generar_Qr(self.ventana_qr,self.menuFunc,self.tipocuenta,self.nombrecuenta)

    def volver_al_menu(self,menuFunc, tipoCuenta, nombreCuenta):
        self.eliminar()
        self.menuFunc(tipoCuenta, nombreCuenta)

if __name__ == "__main__":
    ventana_qr = tk.Tk()
