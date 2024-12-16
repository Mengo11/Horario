#menu.py

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import Funcionalidad_parte_principal as FPP
import Pestaña_filtro as PF
import Aulas
import Pestaña_qr
from cuentas import cuentas1
import Profesores,os,sys
import alumnos
import asistencias


class menu1:
    
    def __init__(self,tk):
        self.cuentas = cuentas1(tk)
        tk.title("Menu")
        
    def resource_path(relative_path):
      try:
       base_path = sys._MEIPASS
      except Exception:
      
       base_path = os.path.abspath(".")
      return os.path.join(base_path, relative_path)        
    def crear(self,tk,tipoCuenta,nombreCuenta,cerrarSesion,menuFunc):

        def eliminar():
            for elemento in tk.winfo_children():
                elemento.destroy()
        

            #ejecutar modulo del ingreso de alumnos
        def horarios(tk):
            eliminar()
            menu_horarios=FPP.menu_horarios()
            menu_horarios.horarios(tk,menuFunc,tipoCuenta,nombreCuenta)
        def administrar_cuentas():
            eliminar()
            def cuentasFunc(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc):
                self.cuentas.crear(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            cuentasFunc(tk,tipoCuenta,nombreCuenta,menuFunc,cuentasFunc)
            return
        def administrar_materias(tk):
            eliminar()
            Profesores.botones_docentes(tk, menuFunc, tipoCuenta, nombreCuenta)
        def abrir_qr(tk):
            eliminar()
            Pestaña_qr.clase_qr(tk,menuFunc,tipoCuenta,nombreCuenta)
        def administrar_filtros(tk):
            eliminar()
            PF.menu_filtros(tk,menuFunc,tipoCuenta,nombreCuenta)

        def administrar_de_asistencia(tk):
            eliminar()
            asistencias.clase_asistencias(tk,menuFunc,tipoCuenta,nombreCuenta)

        def administrar_alumnos(tk):
            eliminar()
            alumnos.clase_alumnos(tk,menuFunc,tipoCuenta,nombreCuenta)

        def administrar_aulas(tk):
            eliminar()
            Aulas.botones_aulas(tk,menuFunc,tipoCuenta,nombreCuenta)

        def cerrar_sesion():
            eliminar()
            cerrarSesion()
            return
        def cambiar_tema():
            global nuevo_color,nueva_imagen,color_boton_hover
            color = tk.cget("bg")
            new_color = BG3color if color != BG3color else BGcolor
            color_boton_hover="#A2AEE0" if new_color != BGcolor else "#55608B"
            nuevo_color = "black" if new_color != BGcolor else BG2color
            
            color_boton = new_color
            nueva_imagen = self.imagen_tema_alternativa if new_color != BGcolor  else self.imagen_tema
            boton_tema.configure(image=nueva_imagen)

            tk.configure(bg=new_color)
            BG2.configure(bg=nuevo_color)
            boton_tema.configure(bg=color_boton,activebackground=tk.cget("bg"))
            etiqueta_bienvenida.configure(bg=new_color, fg="white" if new_color == BG3color else "black")
            etiqueta_accion.configure(bg=new_color,fg="white" if new_color == BG3color else "black")
            etiqueta_derecha.configure(bg=nuevo_color)
            etiqueta_version.configure(bg=new_color,fg="white" if new_color == BG3color else "black")
            etiqueta_izquierda.configure(bg=nuevo_color)
            
        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(
                background=colorOnHover))
        
            # background color on leving widget
            button.bind("<Leave>", func=lambda e: button.config(
                background=colorOnLeave))
        
        BGcolor="#98c1d9" #fondo de bienvenida y etc
        BG2color="#4A90E2" #footer
        BG3color="#1b284f"
        negro="#000000"
        current_color = tk.cget("bg")
        color_boton_hover = "#A2AEE0"
        new_color = BGcolor if current_color == BG3color else BG3color
        nuevo_color = BG2color if new_color != BGcolor else negro
        color_label = BGcolor if new_color == BG3color else BG3color
        color_boton = BGcolor if current_color != BG3color else BG3color
        

        tk.grid_columnconfigure(0, weight=1)
        
        BG2 = Frame(tk,width=512,height=32,bg=nuevo_color)
        BG2.place(relx = 0.0, rely = 1.0, anchor ='sw', relwidth=1.0, relheight=0.07)
        imagen_administrar_boletin_path = menu1.resource_path("imagenes/administrar_boletin.png")
        self.imagen_administrar_boletin = ImageTk.PhotoImage(Image.open(imagen_administrar_boletin_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_horario_path = menu1.resource_path("imagenes/administrar_horario.png")
        self.imagen_administrar_horario = ImageTk.PhotoImage(Image.open(imagen_administrar_horario_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_asistencia_path = menu1.resource_path("imagenes/administrador_de_asistencia.png")
        self.imagen_administrar_asistencia = ImageTk.PhotoImage(Image.open(imagen_administrar_asistencia_path).resize((20, 20), Image.LANCZOS))

        imagen_administrar_alumnos_path = menu1.resource_path("imagenes/administrar_alumnos.png")
        self.imagen_administrar_alumnos = ImageTk.PhotoImage(Image.open(imagen_administrar_alumnos_path).resize((25, 25), Image.LANCZOS))

        imagen_administrar_cuentas_path = menu1.resource_path("imagenes/administrar_cuentas.png")
        self.imagen_administrar_cuentas = ImageTk.PhotoImage(Image.open(imagen_administrar_cuentas_path).resize((20, 20), Image.LANCZOS))

        imagen_qr_path = menu1.resource_path("imagenes/qr.png")
        self.imagen_qr = ImageTk.PhotoImage(Image.open(imagen_qr_path).resize((20,20),Image.LANCZOS))


        imagen_materia_path = menu1.resource_path("imagenes/materia.png")
        self.imagen_materia = ImageTk.PhotoImage(Image.open(imagen_materia_path).resize((25, 25), Image.LANCZOS))

        imagen_cerrar_sesion_path = menu1.resource_path("imagenes/cerrar_sesion.png")
        self.imagen_cerrar_sesion = ImageTk.PhotoImage(Image.open(imagen_cerrar_sesion_path).resize((20, 20), Image.LANCZOS))

        imagen_aula_path = menu1.resource_path("imagenes/aulas.png")
        self.imagen_aula = ImageTk.PhotoImage(Image.open(imagen_aula_path).resize((20, 20), Image.LANCZOS))

        imagen_filtro_path = menu1.resource_path("imagenes/filtrar.png")
        self.imagen_filtro = ImageTk.PhotoImage(Image.open(imagen_filtro_path).resize((20, 20), Image.LANCZOS))

        imagen_tema_path = menu1.resource_path("imagenes/fondo_claro.png")
        self.imagen_tema = ImageTk.PhotoImage(Image.open(imagen_tema_path).resize((50, 50), Image.LANCZOS))

        imagen_tema_alternativa_path = menu1.resource_path("imagenes/fondo_oscuro.png")
        self.imagen_tema_alternativa = ImageTk.PhotoImage(Image.open(imagen_tema_alternativa_path).resize((50, 50), Image.LANCZOS))


        nueva_imagen = self.imagen_tema if new_color == BG3color else self.imagen_tema_alternativa

        gridposicion = Label(tk, text="", font=('Arial',0), bg=BGcolor)
        gridposicion.grid(row=10,column=1, columnspan=2, padx=9999, pady=(0, 0 ))

        fuente_grande = ('Arial', 32, "bold")
        etiqueta_bienvenida = Label(tk, text="Bienvenido "+nombreCuenta+"", font=fuente_grande, bg=color_label,fg="black" if new_color == BG3color else "white")
        etiqueta_bienvenida.grid(row=0,column=1, columnspan=2, padx=0, pady=(0, 0))

        fuente_chica = ('Arial', 15, "bold")
        etiqueta_accion = Label(tk, text="¿Qué desea hacer hoy?", font=fuente_chica,bg=color_label,fg="black" if new_color == BG3color else "white")
        etiqueta_accion.grid(row=1, column=1, columnspan=2,padx=0, pady=(0, 0), ipady=0)

        etiqueta_version = Label(tk,text="Versión Beta 0.8.95",font=('Arial',15,"bold"),bg=color_label,fg="black" if new_color == BG3color else "white")
        etiqueta_version.place(relx = 0.56, rely = 0.93, anchor ='se')
 
        #boton asistencia
        boton_asistencias = Button(tk, text="Administrar Asistencias", image=self.imagen_administrar_asistencia, compound="left", borderwidth=0, 
                                relief="solid", height=30, width=300, command=lambda:administrar_de_asistencia(tk), font=("Helvetica", 16))
        boton_asistencias.grid(row=3, column=1, padx=(0, 10), pady=(0, 0), sticky="E")
 


        #Boton Alumnos
        boton_alumno = Button(tk, text="Administrar alumnos",image=self.imagen_administrar_alumnos,compound="left",borderwidth=0,relief="solid",  height=30 , width=300,command=lambda:administrar_alumnos(tk), font=("Helvetica", 16))
        boton_alumno.grid(row=4, column=1, padx=(0, 10), pady=(0,0), sticky="E")

        #Boton Cuentas
        boton_cuentas = Button(tk, text="Cuentas",image=self.imagen_administrar_cuentas,compound="left",borderwidth=0,relief="solid",  height=30 , width=300, command=administrar_cuentas, font=("Helvetica", 16))
        boton_cuentas.grid(row=5, column=1, padx=(0, 10), pady=(0,0), sticky="E")

        #Boton Horarios
        boton_horarios = Button(tk, text="Horarios",image=self.imagen_administrar_horario,compound="left",borderwidth=0,relief="solid",  height=30 , width=300, command=lambda:horarios(tk), font=("Helvetica", 16))
        boton_horarios.grid(row=2, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Materias
        boton_materias = Button(tk, text="Materias y profesores",image=self.imagen_materia,compound="left",borderwidth=0,relief="solid",  height=30 , width=300, command=lambda:administrar_materias(tk), font=("Helvetica", 16))
        boton_materias.grid(row=3, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Filtros
        boton_filtros = Button(tk, text="Filtros",image=self.imagen_filtro,compound="left",borderwidth=0,relief="solid",  height=30 , width=300, command=lambda:administrar_filtros(tk), font=("Helvetica", 16))
        boton_filtros.grid(row=4, column=2, padx=(10, 0), pady=(0, 0), sticky="W")

        #Boton Aulas
        boton_aulas = Button(tk, text="Administrar Aulas",image=self.imagen_aula,compound="left",borderwidth=0,relief="solid",  height=30 , width=300, command=lambda:administrar_aulas(tk), font=("Helvetica", 16))
        boton_aulas.grid(row=5, column=2, padx=(10, 0), pady=(0, 0), sticky="W")
        #Boton QR
        boton_qr=Button(tk,text="QR",image=self.imagen_qr,compound="left",borderwidth=0,relief="solid",height=30,width=300,command=lambda:abrir_qr(tk),font=("Helvetica",16))
        boton_qr.grid(row=2, column=1, padx=(0, 10), pady=(0, 0), sticky="E")
        
        #boton temas
        
        boton_tema = Button(tk, image=nueva_imagen, compound="left", borderwidth=0, highlightthickness=0, 
                       bg=color_boton, height=50, width=50, command=cambiar_tema, fg="white", 
                       font=("Helvetica", 16), relief='flat', activebackground=tk.cget("bg"))
        boton_tema.place(relx = 0.04, rely = 0.93, anchor ='se')
        for elemento in tk.winfo_children():
                if isinstance(elemento, Button):
                    if elemento==boton_tema:
                        continue
                    elemento['bg'] = "white"
                    changeOnHover(elemento, color_boton_hover, "white")


        if tipoCuenta == 1: #botones Maestro
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = DISABLED
            boton_alumno['state'] = DISABLED
            boton_cuentas['state'] = DISABLED
        if tipoCuenta == 2: #botones Preceptor
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = NORMAL
            boton_alumno['state'] = NORMAL
            boton_cuentas['state'] = DISABLED
        if tipoCuenta == 3: #botones Administrador
            boton_horarios['state'] = NORMAL
            boton_asistencias['state'] = NORMAL
            boton_alumno['state'] = NORMAL
            boton_cuentas['state'] = NORMAL

        boton_cerrar_sesion = Button(tk, text="Cerrar Sesión",image=self.imagen_cerrar_sesion,compound="left",borderwidth=0,relief="solid", width=150, height=30, command=cerrar_sesion, bg="light coral", font=("Helvetica", 12))
        boton_cerrar_sesion.place(relx = 0.995, rely = 0.92, anchor ='se')

        etiqueta_derecha = Label(BG2, text="©6°5 - 2024",fg="white", bg=nuevo_color,font=("Helvetica", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')

        etiqueta_izquierda = Label(BG2, text="", bg=nuevo_color,fg="white",font=("Helvetica", 16))
        etiqueta_izquierda.place(relx = 0.0, rely = 0.5, anchor ='w')

        if tipoCuenta==1:
            etiqueta_izquierda.config(text="Profesor")
        elif tipoCuenta==2:
            etiqueta_izquierda.config(text="Preceptor")
        elif tipoCuenta==3:
            etiqueta_izquierda.config(text="Administrador")