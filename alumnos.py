import tkinter as tk
from tkinter import *
from tkinter import messagebox
from CompletarAU import AutocompleteEntry
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import re, os, sys
from tkinter import ttk
import mysql.connector
from PDF import PDF_alumnos
from ttkthemes import ThemedStyle
import Cambiar_de_curso

class clase_alumnos:
    def __init__(self, tk, menuFunc, tipoCuenta, nombreCuenta):
        self.ventana_alumnos = tk
        tk.title("Administrar Alumnos")
        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.menuFunc = menuFunc
        self.widgets_clase_alumnos_pr()
    def widgets_clase_alumnos_pr(self):
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
        
            # background color on leving widget
            button.bind("<Leave>", func=lambda e: button.config(
                background=colorOnLeave))
        self.path = resource_path("Imagenes/Colegio_logo.ico")
        self.ventana_alumnos.iconbitmap(self.path)
        BGcolor = "#98c1d9" #fondo de pantalla
        BG2color = "#4A90E2"
        BG3color = "#4A90E2"
        color_fondo = self.ventana_alumnos.cget("bg")
        new_color = BGcolor if color_fondo != BG3color else BG3color
        color_label = BGcolor if new_color == BGcolor else BG3color
        nuevo_color = BG2color if new_color == BGcolor else "black"  # Color de fondo de la pestaña
        style=ttk.Style()
        style.configure("TFrame", background=new_color)
        self.frame_pe = ttk.Frame(self.ventana_alumnos,)
        self.frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame_pe.columnconfigure(0, weight=1)
        self.frame_pe.rowconfigure(0, weight=1)
        self.frame_pe.rowconfigure(1, weight=1)
        self.frame_pe.rowconfigure(2, weight=1) 
        
        
        self.frame_pe.config(style="TFrame")
        self.imagen_ver_path = resource_path("imagenes/ver_asistencia.png")
        imagen_volver_path = resource_path("imagenes/volver.png")
        self.imagen_cargar_m_path = resource_path("imagenes/cargar_asistencia_m.png")
        self.imagen_cargar_a_path = resource_path("imagenes/carga_auto.png")
        self.imagen_ver_cursos_path = resource_path("imagenes/ver-cursos.png")
        self.imagen_cursos_path = resource_path("imagenes/cambiar-curso.png")

        self.imagen_cursos = ImageTk.PhotoImage(Image.open(self.imagen_cursos_path).resize((20, 20)))
        self.imagen_ver_asistencia = ImageTk.PhotoImage(Image.open(self.imagen_ver_path).resize((20, 20)))
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        self.imagen_cargar_m = ImageTk.PhotoImage(Image.open(self.imagen_cargar_m_path).resize((20, 20), Image.LANCZOS))
        self.imagen_cargar_a = ImageTk.PhotoImage(Image.open(self.imagen_cargar_a_path).resize((20,20),Image.LANCZOS))
        self.imagen_ver_cursos = ImageTk.PhotoImage(Image.open(self.imagen_ver_cursos_path).resize((20,20),Image.LANCZOS))
        BG2 = Frame(self.ventana_alumnos, bg=nuevo_color, width=512, height=32)
        BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
        self.etiqueta_bienvenida = Label(self.ventana_alumnos, text="Pestaña de administrar alumnos",bg=color_label,fg="white" if color_label == BG3color else "black",  font=("Monaco", 24, "bold"))
        self.etiqueta_bienvenida.place(relx=0.5, rely=0.1, anchor='n')

        self.ver_asistencia = Button(self.ventana_alumnos, text="Ver alumnos", image=self.imagen_ver_asistencia, compound="left", relief="solid", borderwidth=0, height=35, width=300, font=("Helvetica", 16),command=lambda: self.ver_alumno(("fecha_de_admision","N_Legajo", "Procedencia", "Nombre_y_apellido", "DNI","Fecha_nacimiento","edad","nacionalidad","Curso", "Division","nombre_tutor", "dni_tutor", "nacionalidad_tutor","domicilio_tutor","telefono_tutor"),"SELECT fecha_de_admision, N_Legajo, Procedencia, Nombre_y_apellido, DNI, Fecha_nacimiento, edad, nacionalidad, Curso, Division, nombre_tutor, dni_tutor, nacionalidad_tutor, domicilio_tutor, telefono_tutor FROM alumnos",self.ventana_alumnos,1))
        self.ver_asistencia.grid(row=3, column=3, columnspan=2, padx=(0, 10), pady=(0, 0), sticky="E")
        
        self.cargar_asistencia = Button(self.ventana_alumnos, text="Agregar alumnos", image=self.imagen_cargar_m, compound="left",borderwidth=0, relief="solid", height=35, width=430, font=("Helvetica", 16), command=lambda: self.añadir_alm(("fecha_de_admision","N_Legajo", "Procedencia", "Nombre_y_apellido", "DNI","Fecha_nacimiento","edad","nacionalidad","Curso", "Division","nombre_tutor", "dni_tutor", "nacionalidad_tutor","domicilio_tutor","telefono_tutor"),"SELECT fecha_de_admision, N_Legajo, Procedencia, Nombre_y_apellido, DNI, Fecha_nacimiento, edad, nacionalidad, Curso, Division, nombre_tutor, dni_tutor, nacionalidad_tutor, domicilio_tutor, telefono_tutor FROM alumnos",self.ventana_alumnos))
        self.cargar_asistencia.grid(row=3, column=5, padx=(0, 10), pady=(0, 0), sticky="E")
        
        self.cursos=Button(self.ventana_alumnos,text="Cambiar curso",image=self.imagen_cursos, command=self.cambiar_curso,compound="left",height=30,width=430,borderwidth=0,relief="solid",font=("Helvetica",16))
        self.cursos.grid(row=5,column=5,padx=(0,10),pady=(0,0),sticky="E")
        self.ver_curso=Button(self.ventana_alumnos,text="Ver cursos",image=self.imagen_ver_cursos,command=lambda:self.cambiar_curso(True),compound="left",height=35,width=300,borderwidth=0,relief="solid",font=("Helvetica",16))
        self.ver_curso.grid(row=5,column=3,columnspan=2,padx=(0,10),pady=(0,0),sticky="E")
        self.boton_volver = Button(self.ventana_alumnos, text="Volver", image=self.imagen_volver, compound="left", height=30, width=300, borderwidth=0, relief="solid", command=lambda: self.volver_al_menu(self.menuFunc, self.tipocuenta, self.nombrecuenta))
        self.boton_volver.grid(row=8, column=3,columnspan=4,  padx=(0, 10), pady=(0, 0))

        etiqueta_derecha = Label(BG2, text="©6°5 - 2024",fg="white", bg=nuevo_color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=nuevo_color,fg="white",font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')
    

        for elemento in self.ventana_alumnos.winfo_children():
            if isinstance(elemento, Button):
                elemento['bg'] = "white"
                elemento["borderwidth"] = 0
                changeOnHover(elemento, "#A2AEE0", "white")
        if self.tipocuenta==1:
            etiqueta_izquierda.config(text="Profesor")
        elif self.tipocuenta==2:
            etiqueta_izquierda.config(text="Preceptor")
        elif self.tipocuenta==3:
            etiqueta_izquierda.config(text="Administrador")
#--------------------------------------------------------------------[Interfaz Mengo]


    def cambiar_curso(self, ver=False):
        # Crear la ventana secundaria
        self.ventana_cursos = Toplevel(self.ventana_alumnos)
        
        # Configurar tamaño fijo de la ventana
        self.ventana_cursos.geometry("600x400")
        self.ventana_cursos.resizable(False, False)  # Impedir que se cambie el tamaño
        
        # Configurar columnas y filas
        self.ventana_cursos.columnconfigure(0, weight=1)
        self.ventana_cursos.rowconfigure(0, weight=1)
        self.ventana_cursos.rowconfigure(1, weight=1)

        # Establecer color de fondo de la ventana principal
        self.ventana_cursos.configure(bg="#98c1d9")  # Un color suave para el fondo

        # Crear marcos
        self.frame_cursos = Frame(self.ventana_cursos, bg="#98c1d9")  # Color de marco más suave
        self.frame_cursos.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.frame_divisiones = Frame(self.ventana_cursos, bg="#98c1d9")  # Color de marco más suave
        self.frame_divisiones.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        # Botón para volver con color y tamaño mejorado
        Button(self.ventana_cursos, text="Volver", command=self.ventana_cursos.destroy, 
            bg="#1a759f", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=3, padx=20, pady=10).grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Configurar columnas y filas para los botones de los cursos
        for x in range(1, 8):
            self.frame_cursos.columnconfigure(x-1, weight=1)
        
        for x in range(1, 7):
            self.frame_divisiones.columnconfigure(x-1, weight=1)
        
        self.frame_cursos.rowconfigure(0, weight=1)
        self.frame_divisiones.rowconfigure(0, weight=1)

        # Variables para almacenar la selección
        self.curso_seleccionado = None
        self.division_seleccionada = None

        # Crear botones de cursos con estilo mejorado (colores más vivos y mejor tamaño)
        for x in range(1, 8):
            boton = Button(self.frame_cursos, text=f"{x}º", command=lambda x=x: self.actualizar_divisiones(x),
                        bg="#1a759f", fg="white", font=("Arial", 12, "bold"), relief="raised", bd=2, padx=20, pady=8)
            boton.grid(row=0, column=x-1, sticky="nsew", padx=10, pady=10)

            if x == 1:  # Seleccionar el primer curso por defecto
                self.actualizar_divisiones(x)
        
        # Botón para ingresar al curso seleccionado con un color más vibrante
        ingresar_button = Button(self.ventana_cursos, text="Ingresar al curso", 
                                command=self.ingresar_ventana_cambiar_curso, 
                                bg="#1a759f", fg="white", font=("Arial", 14, "bold"), relief="raised", bd=3, padx=40, pady=10)
        ingresar_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        # Botón de opción secundaria para ingresar al curso
        if ver == False:
            Button(self.ventana_cursos, text="Ingresar al curso", command=self.ingresar_ventana_cambiar_curso, 
                bg="#1a759f", borderwidth=2, padx=35, pady=8, font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        else:
            Button(self.ventana_cursos, text="Ingresar al curso", command=lambda: self.ingresar_ventana_cambiar_curso(True), 
                bg="#1a759f", borderwidth=2, padx=35, pady=8, font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        # Etiqueta de selección de curso y división
        label = Label(self.ventana_cursos, text="Curso:" + str(self.curso_seleccionado) + " División:" + str(self.division_seleccionada), 
                    bg="#1a759f", font=("Arial", 12, "bold"))
        label.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    def actualizar_label(self):
        # Actualiza la etiqueta con el curso y división seleccionada
        label = Label(self.ventana_cursos, text="Curso:" + str(self.curso_seleccionado) + " División:" + str(self.division_seleccionada), 
                    bg="#1a759f", font=("Arial", 12, "bold"))
        label.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    def actualizar_divisiones(self, curso):
        # Almacenar el curso seleccionado
        self.curso_seleccionado = curso

        # Limpia los botones actuales en frame_divisiones
        for widget in self.frame_divisiones.winfo_children():
            widget.destroy()

        # Si el curso es mayor a 3, mostrar divisiones numéricas
        if curso > 3:
            divisiones = range(1, 8)  # Números del 1 al 7
            self.division_seleccionada = 1
        else:
            divisiones = ['A', 'B', 'C', 'D', 'E', 'F']  # Letras de la A a la E
            self.division_seleccionada = 'A'

        # Crear botones para las divisiones con color de fondo #4F81BD
        for i, division in enumerate(divisiones):
            boton = Button(self.frame_divisiones, text=str(division), command=lambda d=division: self.seleccionar_division(d), 
                        padx=20, pady=8, bg="#4F81BD", fg="white", relief="raised", font=("Arial", 12, "bold"))
            boton.grid(row=0, column=i, sticky="nsew", padx=10, pady=10)
        
        self.actualizar_label()

    def seleccionar_division(self, division):
        # Almacenar la división seleccionada
        self.division_seleccionada = division
        self.actualizar_label()

    def ingresar_ventana_cambiar_curso(self, ver=False):
        # Verificar que se haya seleccionado un curso y una división
        if self.curso_seleccionado is not None and self.division_seleccionada is not None and ver == False:
            self.ventana_cursos.destroy()
            self.eliminar()
            Cambiar_de_curso.Cambiar_de_curso(self.ventana_alumnos, self.menuFunc, self.tipocuenta, self.nombrecuenta, self.curso_seleccionado, self.division_seleccionada)
        if self.curso_seleccionado is not None and self.division_seleccionada is not None and ver == True:
            self.ventana_cursos.destroy()
            self.eliminar()
            Cambiar_de_curso.Cambiar_de_curso(self.ventana_alumnos, self.menuFunc, self.tipocuenta, self.nombrecuenta, self.curso_seleccionado, self.division_seleccionada, True)
        else:
            print("Debe seleccionar un curso y una división antes de continuar.")




#------------------------------------------------------------------
        
    def eliminar(self):
        for elemento in self.ventana_alumnos.winfo_children():
            elemento.destroy()

    def volver_al_menu(self, menuFunc, tipoCuenta, nombreCuenta):
        self.eliminar()
        self.menuFunc(tipoCuenta, nombreCuenta)
    def volveralumnos(self,ventana):
        ventana.destroy()
        self.ventana_alumnos()

    def conectar_base_de_datos(self):
        
        global cursor
        global cnx
        cnx = mysql.connector.connect(
                host='eestn1.com.ar',
                user='tecnica1',
                password='z%51#q57A7BR',
                database='tec_boletines2023',
                port=3306
        )
        # Crear un cursor para ejecutar consultas
        cursor = cnx.cursor()
    def cerrar_base_de_datos(self):
        cursor.close()
        cnx.close()    
    
    #FUNCIONES PARA EVITAR ERRORES, ETC.
    def altura_confirmacion(self, variable, entry):
        self.x = variable 
        self.y = entry
        if self.x.get() == 0:
            self.y.config(state=tk.NORMAL)  # Habilita el Entry
        else:
            self.y.delete(0, tk.END)
            self.y.config(state=tk.DISABLED)  # Deshabilita el Entry
    def actualizar_opciones_division(self, event):
        # Obtener el valor seleccionado en el combobox de Curso
        curso_seleccionado = self.division.get()
        
        # Filtrar las opciones de División basadas en el valor del Curso
        if curso_seleccionado in ["1", "2", "3"]:
            opciones_filtradas = ["A", "B", "C", "D", "E"]
        else:
            opciones_filtradas = ["1", "2", "3", "4", "5", "6"]
        
        # Actualizar las opciones en el combobox de División
        self.division_sup.config(values=opciones_filtradas)
        self.division_sup.set('')  # Limpiar selección previ
    def validar_prefijo(self,event, entry_widget,arriba_alm):
        self.entry_telefono3.hide_listbox(self.ventana_alumnos)
        widget_con_enfoque = self.entry_telefono3.focus_get()
        if isinstance(widget_con_enfoque, tk.Listbox):
            return
        entrada = entry_widget.get()
        if not entrada in self.prefijos2:
            if len(entrada) > 0: #no mostrar error si campo se deja vacio
                messagebox.showerror("Error", "Por favor seleccionar la opcion del menu")
                entry_widget.delete(0, tk.END)

    def mayuscula_inicial(self,entry_widget):
    # Obtenemos el contenido actual del Entry
        try:
            current_text = entry_widget.get()

            # Capitalizamos la primera letra de cada palabra si el contenido no está vacío
            if current_text:
                capitalized_words = [word.capitalize() for word in current_text.split()]
                capitalized_text = " ".join(capitalized_words)
                entry_widget.delete(0, tk.END)  # Borramos el contenido actual
                entry_widget.insert(0, capitalized_text) 
                return True
        except:
            messagebox.showerror("Error", "No tiene mayuscula el inicio de los nombres")
            return False 
    def validar_numeros(self,P):
    # Función de validación para permitir solo caracteres numéricos
        if all(c.isdigit() for c in P):
            return True
        else:
            messagebox.showerror("Error", "Solo se permiten números")
            return False
    def validar_letras(self,P):
        
        # Esta función permite solo letras y números
        if all(c.isalpha() or c.isspace() for c in P):
            return True
        else:
            messagebox.showerror("Error", "Solo se permiten letras")
            return False 

    def validar_letras_numeros(self,P):
        
        # Esta función permite solo letras y números
        if all(c.isalpha() or c.isspace() or c.isdigit() for c in P):
            return True
        else:
            messagebox.showerror("Error", "Solo se permiten letras y numeros")
    def guardar_informacion(self,x,event):
        obtenerfecha = x.get()
        
        # Verifica si la fecha es válida
        if not self.es_fecha_valida(obtenerfecha):
            messagebox.showerror("Error", "Debe seleccionar una fecha a traves del calendario.")
            self.x.delete(0, tk.END)
            return False
    def es_fecha_valida(self,fecha):
        try:
            datetime.strptime(fecha, "%Y/%m/%d")
            return True
        except ValueError:
            return False
    def get_entrys(self):
        entrys = []
        nombre = self.añadir_nombre.get()
        apellido = self.añadir_apellido.get()
        self.nombre = nombre.strip()
        self.apellido = apellido.strip()
        direccion = self.entry_direccion.get()
        altura = self.entry_altura.get()
        self.direccion = direccion.strip()
        self.altura = altura.strip()
        telefono3 = self.entry_telefono3.get()
        telefono4 = self.entry_telefono4.get()
        codigo_area_tutor = self.c_a2.get()
        self.telefono3 = telefono3.strip()
        self.telefono4 = telefono4.strip()
        self.codigo_area_tutor = codigo_area_tutor.strip()
        entrys.append(self.entry_fecha_admision.get())#0
        entrys.append(self.entry_legajo.get())#1
        entrys.append(self.entry_procedencia.get())#2
        entrys.append(f"{self.nombre} {self.apellido}")#3
        entrys.append(self.añadir_nro_documento.get())#4
        entrys.append(self.entry_fecha.get())#5
        entrys.append(self.edad.get())#6s
        entrys.append(self.entry_nacionalidad.get())#7
        entrys.append(self.division.get())#8
        entrys.append(self.division_sup.get())#9
        entrys.append(self.entry_tutor.get())#10
        entrys.append(self.entry_dni.get())#11
        entrys.append(self.entry_nacionalidad_tutor.get())#12
        entrys.append(f"{self.direccion} {self.altura}")#13
        entrys.append(f"{self.codigo_area_tutor} {self.telefono3} {self.telefono4}")#14

        
        
        
        return entrys
    def borrar_entrys(self):
        for borrar in self.entry_widgets:
            borrar.delete(0, tk.END)
        self.edad.set("11")
        self.division.set("1")
        self.division_sup.set("A")
        self.entry_telefono3.hide_listbox(self.ventana_alumnos)
    def doble_cliclk_alumnos(self,event):
        self.item = self.tree_alm.selection()
        if self.item:
            values = self.tree_alm.item(self.item, "values")
            self.entry_fecha_admision.delete(0, tk.END)
            self.entry_fecha_admision.insert(0, values[0])
            self.entry_legajo.delete(0, tk.END)
            self.entry_legajo.insert(0, values[1])
            self.entry_procedencia.delete(0, tk.END)
            self.entry_procedencia.insert(0, values[2])
            self.nombres = values[3].split()
            
            if len(self.nombres) >= 1:
                self.nombre = self.nombres[0]
            else:
                self.nombre = ""
            if len(self.nombres) >= 2:
                self.apellido = self.nombres[1]
            else:
                self.apellido = ""
            
            self.añadir_nombre.delete(0, tk.END)
            self.añadir_nombre.insert(0, self.nombre)
            self.añadir_apellido.delete(0, tk.END)
            self.añadir_apellido.insert(0, self.apellido)
            self.añadir_nro_documento.delete(0, tk.END)
            self.añadir_nro_documento.insert(0, values[4])
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, values[5])
            self.edad.set(values[6])
            self.entry_nacionalidad.delete(0, tk.END)
            self.entry_nacionalidad.insert(0, values[7])
            self.division.set( values[8])
            self.division_sup.set(values[9])
            self.entry_tutor.delete(0, tk.END)
            self.entry_tutor.insert(0, values[10])
            self.entry_dni.delete(0, tk.END)
            self.entry_dni.insert(0, values[11])
            self.entry_nacionalidad_tutor.delete(0, tk.END)
            self.entry_nacionalidad_tutor.insert(0, values[12])
            self.ubicacion = values[13].split()

            if len(self.ubicacion) >= 2:
                self.direccion = " ".join(self.ubicacion[:-1])  # Toma todo excepto el último elemento como dirección
                self.altura = self.ubicacion[-1]  # Toma el último elemento como altura
            elif len(self.ubicacion) == 1:
                self.direccion = self.ubicacion[0]  # Si solo hay un elemento, lo trata como dirección
                self.altura = ""  # No hay altura, se deja vacío
            else:
                self.direccion = ""
                self.altura = ""
            
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(0, self.direccion)
            self.entry_altura.delete(0, tk.END)
            self.entry_altura.insert(0, self.altura)

            telefonos = values[14].split()

            if len(telefonos) >= 2:
                telefono = telefonos[2]
            else:
                telefono = ""
            if len(telefonos) >= 3:
                telefono2 = telefonos[3]
            else:
                telefono2 = ""

            self.entry_telefono3.delete(0, tk.END)
            self.entry_telefono3.insert(0, telefono)
            self.entry_telefono3.hide_listbox(self.ventana_alumnos)
            self.entry_telefono4.delete(0, tk.END)
            self.entry_telefono4.insert(0, telefono2)




    def limites(self, event,entrys, x):
        self.contenido = entrys.get()
        if len(self.contenido) > x:
            nuevo_contenido = self.contenido[:x]
            entrys.delete(0, tk.END)
            entrys.insert(0, nuevo_contenido)
            messagebox.showerror("Error", "Solo se permiten "+str(x)+" caracteres")
        
    

        
    def focus_Outside(self, event, entrys, x):
        self.contenido = entrys.get()
        if len(self.contenido) > 0 and len(self.contenido) < x:
            entrys.delete(0, tk.END)
            messagebox.showerror("Error", "Solo se permiten como minimo "+str(x)+" caracteres")
        self.mayuscula_inicial(entrys)
       
        



    #FUNCIONES LLAMADAS A BOTONES EJEMPLO: AGREGAR ALUMNOS
    def ver_alumno(self,columnas_alm,query,ver_alm,eliminar_b):
        if eliminar_b == 1:
            print("anashe")
            self.eliminar()
            self.frame_pe= tk.Frame(ver_alm)
            self.frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
    
        ver_alm.title("Ver alumnos")
        self.conectar_base_de_datos()
        self.cursor = cnx.cursor()
        BG3color = "#1b284f"
        color_fondo = self.ventana_alumnos.cget("bg")
        if  color_fondo== BG3color:
         style = ThemedStyle(self.frame_pe)
         style.set_theme("black")
        else : 
         style = ThemedStyle(self.frame_pe)
         style.set_theme("xpnative")
        ttk.Button(self.frame_pe, text="Volver", command=self.volver_menu_alumnos).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.treeview_alm = ttk.Labelframe(self.frame_pe, text="Alumnos")   
        self.treeview_alm.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")     
        scrollbar = ttk.Scrollbar(self.treeview_alm)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = ttk.Scrollbar(self.treeview_alm, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree_alm = ttk.Treeview(self.treeview_alm, yscrollcommand=scrollbar.set, xscrollcommand=scrollbar_x.set, selectmode="extended")
        self.tree_alm.pack(expand=True, fill="both")
        self.tree_alm.bind("<Double-1>", self.doble_cliclk_alumnos)
        scrollbar.config(command=self.tree_alm.yview)
        scrollbar_x.config(command=self.tree_alm.xview)
        self.tree_alm["columns"]=("fecha_de_admision","N_Legajo", "Procedencia", "Nombre_y_apellido", "DNI","Fecha_nacimiento","edad","nacionalidad","Curso", "Division","nombre_tutor", "dni_tutor", "nacionalidad_tutor","domicilio_tutor","telefono_tutor")
        self.tree_alm.column("#0", width=0, stretch=0)
        self.tree_alm.column("fecha_de_admision", anchor="center", width=100)
        self.tree_alm.column("N_Legajo", anchor="center", width=100)
        self.tree_alm.column("Procedencia", anchor="center", width=100)
        self.tree_alm.column("Nombre_y_apellido", anchor="center", width=100)
        self.tree_alm.column("DNI", anchor="center", width=100)
        self.tree_alm.column("Fecha_nacimiento", anchor="center", width=100)
        self.tree_alm.column("edad", anchor="center", width=100)
        self.tree_alm.column("nacionalidad", anchor="center", width=100)
        self.tree_alm.column("Curso", anchor="center", width=100)
        self.tree_alm.column("Division", anchor="center", width=100)
        self.tree_alm.column("nombre_tutor", anchor="center", width=100)
        self.tree_alm.column("dni_tutor", anchor="center", width=100)
        self.tree_alm.column("nacionalidad_tutor", anchor="center", width=100)
        self.tree_alm.column("domicilio_tutor", anchor="center", width=100)
        self.tree_alm.column("telefono_tutor", anchor="center", width=100)
        columnas_alm = ["fecha_de_admision","N_Legajo", "Procedencia", "Nombre_y_apellido", "DNI","Fecha_nacimiento","edad","nacionalidad","Curso", "Division","nombre_tutor", "dni_tutor", "nacionalidad_tutor","domicilio_tutor","telefono_tutor"]
        for col in columnas_alm:
            self.tree_alm.column(col, anchor="center", width=100)
            self.tree_alm.heading(col, text=col)
        cursor.execute(query)
        data = cursor.fetchall()
        for index, values in enumerate(data):
            self.tree_alm.insert(parent='', index='end', iid=index, values=values)
        self.tree_alm.pack()
        self.treeview_alm.columnconfigure(0, weight=1)
        self.treeview_alm.rowconfigure(1, weight=1)
        self.frame_pe.columnconfigure(0, weight=1)
        self.frame_pe.rowconfigure(1, weight=1)
        self.cerrar_base_de_datos()
        


    def entry_alumnos(self,ver_alm):
        for x in range(7):
            self.arriba_alm.columnconfigure(x, weight=1)
        self.arriba_alm.rowconfigure(0, weight=1)
        self.arriba_alm.rowconfigure(1, weight=1)

        ttk.Label(self.arriba_alm, text="Fecha de admisión").grid(row=0, column=0)
        self.entry_fecha_admision = DateEntry(self.arriba_alm, selectmode="day", year=2000, month=1, day=1,date_pattern="yyyy/mm/dd", mindate=None, maxdate=None,state="readonly")
        self.entry_fecha_admision.grid(row=1, column=0)
        self.entry_fecha_admision.bind("<KeyRelease>", self.guardar_informacion(self.entry_fecha_admision,1))

        ttk.Label(self.arriba_alm, text="Legajo").grid(row=0, column=1)
        self.entry_legajo = ttk.Entry(self.arriba_alm)
        self.entry_legajo.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_numeros), "%P"))
        self.entry_legajo.bind("<Focus>")
        self.entry_legajo.grid(row=1, column=1)
        
        ttk.Label(self.arriba_alm, text="Procedencia").grid(row=0, column=2)
        self.entry_procedencia = ttk.Entry(self.arriba_alm)
        self.entry_procedencia.bind("<FocusOut>", lambda event: self.mayuscula_inicial(self.entry_procedencia))
        self.entry_procedencia.grid(row=1, column=2)
        
        ttk.Label(self.arriba_alm, text="Apellido").grid(row=0, column=3)
        self.añadir_nombre = ttk.Entry(self.arriba_alm)
        self.añadir_nombre.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.añadir_nombre,3))
        self.añadir_nombre.bind("<KeyRelease>", lambda event: self.limites(0,self.añadir_nombre,20))
        self.añadir_nombre.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras), "%P"))
        self.añadir_nombre.grid(row=1, column=3)
        
        ttk.Label(self.arriba_alm, text="Nombre").grid(row=0, column=4)
        self.añadir_apellido = ttk.Entry(self.arriba_alm)
        self.añadir_apellido.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.añadir_apellido,4))
        self.añadir_apellido.bind("<KeyRelease>", lambda event: self.limites(0,self.añadir_apellido,20))
        self.añadir_apellido.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras), "%P"))
        self.añadir_apellido.grid(row=1, column=4)

        ttk.Label(self.arriba_alm, text="DNI").grid(row=0, column=5)
        self.añadir_nro_documento = ttk.Entry(self.arriba_alm)
        self.añadir_nro_documento.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_numeros), "%P"))
        self.añadir_nro_documento.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.añadir_nro_documento,4))
        self.añadir_nro_documento.bind("<KeyRelease>", lambda event: self.limites(0,self.añadir_nro_documento,15))
        self.añadir_nro_documento.grid(row=1, column=5)

        tk.Label(self.arriba_alm, text="Fecha de nacimiento").grid(row=0, column=6)
        self.entry_fecha = DateEntry(self.arriba_alm, selectmode="day", year=2000, month=1, day=1,date_pattern="yyyy/mm/dd", mindate=None, maxdate=None,state="readonly")
        self.entry_fecha.grid(row=1, column=6)
        self.entry_fecha.bind("<KeyRelease>", self.guardar_informacion(self.entry_fecha,1))

        ttk.Label(self.arriba_alm, text="edad").grid(row=0, column=7)
        self.edad = tk.StringVar() 
        self.spin_edad = ttk.Spinbox(self.arriba_alm,textvariable=self.edad,from_=10,to=25,validate="key", state="readonly")
        self.spin_edad.grid(row=1, column=7)

        ttk.Label(self.arriba_alm, text="Nacionalidad").grid(row=2, column=0)
        self.entry_nacionalidad = ttk.Entry(self.arriba_alm)
        self.entry_nacionalidad.bind("<FocusOut>", lambda event: self.mayuscula_inicial(0,self.entry_nacionalidad,4))
        self.entry_nacionalidad.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_nacionalidad,25))
        self.entry_nacionalidad.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras), "%P"))
        self.entry_nacionalidad.grid(row=3, column=0)

        ttk.Label(self.arriba_alm, text="Curso").grid(row=2, column=1)
        self.cursos =  ["1","2","3","4","5","6","7"]
        self.division = ttk.Combobox(self.arriba_alm, values=self.cursos, state="readonly")
        self.division.grid(column=1, row=3)
        
        ttk.Label(self.arriba_alm, text="Division").grid(row=2, column=2)
        self.opc_division_sup = ["A","B","C","D","E","1","2","3","4","5","6"]
        self.division_sup = ttk.Combobox(self.arriba_alm, state="readonly")
        self.division_sup.grid(column=2, row=3)
        self.division.bind("<<ComboboxSelected>>", self.actualizar_opciones_division)

        def resource_path(relative_path):
            try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
                base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
            return os.path.join(base_path, relative_path)
        


        ttk.Label(self.arriba_alm, text="Nombre completo tutor").grid(row=2, column=3)
        self.entry_tutor = ttk.Entry(self.arriba_alm)
        self.entry_tutor.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_tutor,40))
        self.entry_tutor.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.entry_tutor,6))
        self.entry_tutor.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras), "%P"))
        self.entry_tutor.grid(row=3, column=3)

        ttk.Label(self.arriba_alm, text="DNI tutor").grid(row=2, column=4)
        self.entry_dni = ttk.Entry(self.arriba_alm)
        self.entry_dni.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.entry_dni,4))
        self.entry_dni.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_dni,15))
        self.entry_dni.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_numeros), "%P"))
        self.entry_dni.grid(row=3, column=4)

        ttk.Label(self.arriba_alm, text="Nacionalidad tutor").grid(row=2, column=5)
        self.entry_nacionalidad_tutor = ttk.Entry(self.arriba_alm)
        self.entry_nacionalidad_tutor.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_nacionalidad_tutor,25))
        self.entry_nacionalidad_tutor.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras), "%P"))
        self.entry_nacionalidad_tutor.grid(row=3, column=5)

        ttk.Label(self.arriba_alm, text="Direccion").grid(row=2, column=6)
        self.entry_direccion = ttk.Entry(self.arriba_alm)
        self.entry_direccion.bind("<FocusOut>", lambda event: self.focus_Outside(0,self.entry_direccion,5))
        self.entry_direccion.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_direccion,40))
        self.entry_direccion.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_letras_numeros), "%P"))
        self.entry_direccion.grid(row=3, column=6)

        ttk.Label(self.arriba_alm, text="Altura").grid(row=2, column=7)
        self.entry_altura = ttk.Entry(self.arriba_alm)
        self.entry_altura.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_altura,6))
        self.entry_altura.grid(row=3, column=7, sticky="w")
        self.entry_altura.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_numeros), "%P"))
        self.check = tk.IntVar()
        self.altura = ttk.Checkbutton(self.arriba_alm, text="Sin Numero", variable=self.check, command=lambda: self.altura_confirmacion(self.check, self.entry_altura))
        self.altura.grid(row=3, column=7, sticky="e")
        
        self.valor_predeterminado2 = "+54 9"
        # Crea una instancia de StringVar y establece el valor predeterminado
        string_var2 = tk.StringVar()
        string_var2.set(self.valor_predeterminado2)

        # Crea el Entry y enlaza su textvariabl
        ttk.Label(self.arriba_alm, text="Codigo de area:").grid(column=0, row=4)
        self.c_a2 = tk.Entry(self.arriba_alm, textvariable=string_var2, state=tk.DISABLED, width=len(self.valor_predeterminado2))
        self.c_a2.grid(column=0, row=5)
        
        ttk.Label(self.arriba_alm, text="Prefijos:").grid(column=1, row=4)
        codigo_prefijos=resource_path('numero_codigo.txt')
        self.prefijos2=[]
        with open(codigo_prefijos, 'r') as archivo:
            for linea in archivo:
                numero = linea.strip()
                self.prefijos2.append(numero)
        self.entry_telefono3 = AutocompleteEntry(self.prefijos2,self.arriba_alm)
        self.entry_telefono3.bind("<FocusOut>", lambda event: self.validar_prefijo(event, self.entry_telefono3,ver_alm))
        self.entry_telefono3.grid(row=5, column=1)
        
        ttk.Label(self.arriba_alm, text="Numero de teléfono tutor").grid(column=2, row=4)
        self.entry_telefono4 = ttk.Entry(self.arriba_alm, validate="key")
        self.entry_telefono4.bind("<KeyRelease>", lambda event: self.limites(0,self.entry_telefono4,20))
        self.entry_telefono4.config(validate="key",validatecommand=(self.arriba_alm.register(self.validar_numeros), "%P"))
        self.entry_telefono4.grid(row=5, column=2)
        self.entry_widgets=[self.entry_fecha_admision, self.entry_legajo, self.entry_procedencia, self.añadir_nombre, self.añadir_apellido, self.añadir_nro_documento, self.entry_fecha, self.entry_nacionalidad,  self.entry_tutor, self.entry_dni, self.entry_nacionalidad_tutor,self.entry_direccion,self.entry_altura,self.c_a2,self.entry_telefono3,self.entry_telefono4]    


    def añadir_alm(self,columnas_alm,query,ver_alm):    
        self.eliminar()
        self.frame_pe= tk.Frame(ver_alm)
        self.frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        self.ver_alumno(columnas_alm,query,ver_alm,1)
        self.arriba_alm = ttk.LabelFrame(self.frame_pe, text="Alumno")
        self.arriba_alm.grid(row=0, column=0, sticky="nsew")
       
        BG3color = "#1b284f"
        color_fondo = self.ventana_alumnos.cget("bg")
        if  color_fondo== BG3color:
         style = ThemedStyle(self.frame_pe)
         style.set_theme("black")
        else : 
         style = ThemedStyle(self.frame_pe)
         style.set_theme("xpnative")

        tk.Button(self.arriba_alm, text="Añadir", command=lambda: self.funcion(1)).grid(row=0, column=8, sticky="nsew")
        tk.Button(self.arriba_alm, text="Eliminar",compound="left",fg="white",bg="#960000", command=lambda: self.funcion(2)).grid(column=8, row=1, sticky="nsew")
        tk.Button(self.arriba_alm,text="Volver",compound="left",fg="white",bg="#960000", command=self.volver_menu_alumnos).grid(column=8, row=4, sticky="nsew")
        tk.Button(self.arriba_alm, text="modificar", command=lambda: self.funcion(3)).grid(row=3, column=8, sticky="nsew") 
        tk.Button(self.arriba_alm, text="Exportar a PDF", command=self.exportar_a_pdf).grid(row=2,column=8, sticky="nsew")
        self.entry_alumnos(ver_alm)
        for x in range(7):
            self.arriba_alm.columnconfigure(x, weight=1)
            self.arriba_alm.rowconfigure(x, weight=1)
    def volver_menu_alumnos(self):
        self.eliminar()
        self.widgets_clase_alumnos_pr()
        
    def exportar_a_pdf(self):
     try:
        pdf3 = PDF_alumnos()
        
        # Asegúrate de agregar la página de los alumnos
        pdf3.add_student_page()
        pdf3.agregar_padre()
        
        nombre_archivo = "exportacion_alumnos.pdf"  
        pdf3.guardar_archivo(nombre_archivo)
        messagebox.showinfo("Exportar a PDF", f"PDF exportado con éxito como {nombre_archivo}")
     except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el PDF: {e}")


    #FUNCIONES DE MODIFICACION DE LA BASE DE DATOS:
    def funcion(self,opcion):
        self.conectar_base_de_datos()
        if opcion ==1:
            self.entrys = self.get_entrys()

            if self.check == 0:
                if not self.entrys[0] or not self.entrys[1] or not self.entrys[2] or not self.nombre or not self.apellido or not self.entrys[4] or not self.entrys[5] or not self.entrys[6] or not self.entrys[7] or not self.entrys[8] or not self.entrys[9] or not self.entrys[10] or not self.entrys[11] or not self.entrys[12] or not self.direccion or not self.altura or not self.codigo_area_tutor or not self.telefono3 or not self.telefono4:
                    messagebox.showerror("Error", "Por favor rellena todos los campos") 
                    return False
            else:
                if not self.entrys[0] or not self.entrys[1] or not self.entrys[2] or not self.nombre or not self.apellido or not self.entrys[4] or not self.entrys[5] or not self.entrys[6] or not self.entrys[7] or not self.entrys[8] or not self.entrys[9] or not self.entrys[10] or not self.entrys[11] or not self.entrys[12] or not self.direccion or not  self.codigo_area_tutor or not self.telefono3 or not self.telefono4:
                    messagebox.showerror("Error", "Por favor rellena todos los campos")
                    return False
            select_legajo_query = "SELECT * FROM alumnos WHERE N_Legajo = %s"
            cursor = cnx.cursor()
            cursor.execute(select_legajo_query, (self.entrys[1],))
            legajo_existente = cursor.fetchone()

            if legajo_existente:
                messagebox.showerror("Error", "El legajo ya existe")
                return False
            self.select_query = "SELECT * FROM alumnos WHERE fecha_de_admision = %s AND N_Legajo = %s AND Procedencia = %s AND Nombre_y_apellido = %s AND DNI = %s AND Fecha_nacimiento = %s AND edad = %s AND nacionalidad = %s AND Curso = %s AND Division = %s AND nombre_tutor = %s AND dni_tutor = %s AND nacionalidad_tutor = %s AND domicilio_tutor = %s AND telefono_tutor = %s"
            self.verificar = (self.entrys[0], self.entrys[1], self.entrys[2], self.entrys[3], self.entrys[4], self.entrys[5], self.entrys[6], self.entrys[7],self.entrys[8], self.entrys[9], self.entrys[10], self.entrys[11], self.entrys[12], self.entrys[13], self.entrys[14])               
            cursor = cnx.cursor()
            cursor.execute(self.select_query, self.verificar)
            fila_existente = cursor.fetchone()
            if fila_existente:
                messagebox.showerror("Error", "El alumno ya existe")
                return False
           
            
            self.insert_query = "INSERT INTO alumnos (fecha_de_admision, N_Legajo, Procedencia, Nombre_y_apellido, DNI, Fecha_nacimiento, edad, nacionalidad, Curso, Division, nombre_tutor, dni_tutor, nacionalidad_tutor, domicilio_tutor, telefono_tutor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            self.verificar_insertar = (self.entrys[0], self.entrys[1], self.entrys[2], self.entrys[3], self.entrys[4], self.entrys[5], self.entrys[6], self.entrys[7],self.entrys[8], self.entrys[9], self.entrys[10], self.entrys[11], self.entrys[12], self.entrys[13], self.entrys[14])               
            cursor = cnx.cursor()
            cursor.execute(self.insert_query, self.verificar)
            cnx.commit() 
            messagebox.showinfo("Exito", "Alumno creado con exito")
            self.tree_alm.insert(parent='', index='end', values=(self.entrys[0], self.entrys[1], self.entrys[2], self.entrys[3], self.entrys[4], self.entrys[5], self.entrys[6], self.entrys[7],self.entrys[8], self.entrys[9], self.entrys[10], self.entrys[11], self.entrys[12], self.entrys[13], self.entrys[14])) 
            self.borrar_entrys()

            self.cerrar_base_de_datos()
        elif opcion == 2:
            self.respuesta = messagebox.askyesno("Advertencia", "¿Desea borrar el registro?")
            
            if self.respuesta:
                self.conectar_base_de_datos()
                self.eleccion = self.tree_alm.selection()
                if not self.eleccion:
                    messagebox.showerror("Error", "Por favor seleccione un registro")
                    return False
                else:
                    try:
                        cursor = cnx.cursor()
                        for self.ele in self.eleccion:
                            self.legajo_id = self.tree_alm.item(self.ele, 'values')[1]
                            cursor.execute("DELETE FROM alumnos WHERE N_Legajo = %s", (self.legajo_id,))
                            cnx.commit()
                            self.tree_alm.delete(self.ele)
                            if len(self.eleccion) == 1:
                                messagebox.showinfo("Exito", "Alumno borrado con exito")
                            else:
                                messagebox.showinfo("Exito", f"{len(self.eleccion)} Alumnos borrados con exito")
                    except Exception as e:
                        messagebox.showerror("Error", e)
                    finally:
                        self.cerrar_base_de_datos()
        elif opcion == 3:
            self.entrys = self.get_entrys()
            self.answer_update = messagebox.askyesno("Advertencia", "Estas seguro de modificar estos datos")
            if self.answer_update == True: 
                self.conectar_base_de_datos()
                self.eleccion_update = self.tree_alm.selection()
                if self.check == 0:
                    if not self.entrys[0] or not self.entrys[1] or not self.entrys[2] or not self.nombre or not self.apellido or not self.entrys[4] or not self.entrys[5] or not self.entrys[6] or not self.entrys[7] or not self.entrys[8] or not self.entrys[9] or not self.entrys[10] or not self.entrys[11] or not self.entrys[12] or not self.direccion or not self.altura or not self.codigo_area_tutor or not self.telefono3 or not self.telefono4:
                        messagebox.showerror("Error", "Por favor rellena todos los campos") 
                        return False
                else:
                    if not self.entrys[0] or not self.entrys[1] or not self.entrys[2] or not self.nombre or not self.apellido or not self.entrys[4] or not self.entrys[5] or not self.entrys[6] or not self.entrys[7] or not self.entrys[8] or not self.entrys[9] or not self.entrys[10] or not self.entrys[11] or not self.entrys[12] or not self.direccion or not  self.codigo_area_tutor or not self.telefono3 or not self.telefono4:
                        messagebox.showerror("Error", "Por favor rellena todos los campos")
                        return False
                if not self.eleccion_update:
                    messagebox.showerror("Error", "Por favor selecciona un dato apretando doble click sobre el")
                    return False
                else:
                    try:
                        #values = self.tree_alm.item(self.eleccion_update, "values")         
            
                        #print(f"self.entrys: {self.entrys} (length: {len(self.entrys)})")
                        #print(f"values: {values} (length: {len(values)})")        
                        #if (self.entrys[0] == values[0] and self.entrys[1] == values[1] and self.entrys[2] == values[2] and self.entrys[3] == f"{values[3]} {values[4]}" and self.entrys[4] == values[5] and self.entrys[5] == values[6] and self.entrys[6] == values[7] and self.entrys[7] == values[8] and self.entrys[8] == values[9] and self.entrys[9] == values[10] and self.entrys[10] == values[11] and self.entrys[11] == values[12] and self.entrys[12] == values[13] and self.entrys[13] == values[14]):
                            #messagebox.showerror("Error", "No ha modificado ningún dato")
                            #return False

                            cursor = cnx.cursor()
                            alumno_legajo = self.tree_alm.item(self.eleccion_update, "values")[1]
                            cursor.execute("UPDATE alumnos SET  fecha_de_admision = %s, N_Legajo = %s, Procedencia = %s, Nombre_y_apellido = %s, DNI = %s, Fecha_nacimiento = %s, edad = %s, nacionalidad = %s, Curso = %s, Division = %s, nombre_tutor = %s, dni_tutor = %s, nacionalidad_tutor = %s, domicilio_tutor = %s, telefono_tutor = %s WHERE N_Legajo = %s",(self.entrys[0], self.entrys[1], self.entrys[2], self.entrys[3], self.entrys[4], self.entrys[5], self.entrys[6], self.entrys[7],self.entrys[8], self.entrys[9], self.entrys[10], self.entrys[11], self.entrys[12], self.entrys[13], self.entrys[14], alumno_legajo))
                            cnx.commit()
                            cnx.commit()
                            cursor.close()
                            messagebox.showinfo("Exito", "Alumno modificado correctamente")
                            self.tree_alm.item(self.eleccion_update, values=(self.entrys[0], self.entrys[1], self.entrys[2], self.entrys[3], self.entrys[4], self.entrys[5], self.entrys[6], self.entrys[7],self.entrys[8], self.entrys[9], self.entrys[10], self.entrys[11], self.entrys[12], self.entrys[13], self.entrys[14]))
                    except Exception as e:
                        messagebox.showerror("Error", "Se produjo un error al actualizar los datos: " + str(e))
                    finally:
                        self.cerrar_base_de_datos()

if __name__ == "__main__":
    root = tk.Tk()
    app = clase_alumnos(root, None, 1, "NombreCuenta")
    root.mainloop()
