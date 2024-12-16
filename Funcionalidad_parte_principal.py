import tkinter as tk
import mysql.connector
from CompletarAU import AutocompleteEntry
from tkinter import ttk
from PDF import PDF
from datetime import datetime
from tkinter import messagebox
from PIL import ImageTk, Image
from ttkthemes import ThemedStyle

import os,sys

#Hecho por Tobias Bonanno
class menu_horarios():
    def resource_path(self, relative_path):
          try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
          except Exception:
            base_path = os.path.abspath(".")
          return os.path.join(base_path, relative_path)
    def eliminar(self):
        for elemento in self.ventana4.winfo_children():
            elemento.destroy()
    def horarios(self, ventana4, menuFunc, tipoCuenta, nombreCuenta):
        global nuevo_color,color_ttk,BG3color,color_fondo,tema_ttk
        def changeOnHover(button, colorOnHover, colorOnLeave):
            button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover))
            button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave))

        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.menuFunc = menuFunc
        self.ventana4 = ventana4
        

        self.ventana4.title("Pantalla de horarios")
        path = self.resource_path("Imagenes/Colegio_logo.ico")
        self.ventana4.iconbitmap(path)
        self.ventana4.geometry("800x600")
        BG2color="#98c1d9"
        BGcolor="#98c1d9"
        BG1color="#98c1d9"
        BG3color="#4A90E2"
        color_fondo=ventana4.cget("bg")
        nuevo_color = "black" if color_fondo != BGcolor else BG2color
        color_label = BGcolor if color_fondo != BG3color else BG3color
        color_boton = "white" if color_fondo != BG3color else "black"
        color_ttk = "white" if color_fondo != BG3color else "black"
        


        style = ttk.Style()
        style.configure('Mi.TLabelframe', background=color_ttk)
        style.configure('Mi.Tboton',bordercolor=color_boton, background=color_boton,foreground="black" if nuevo_color == BG3color else "white")
        style.configure('Mi.Tlabel', background=color_ttk,foreground="white" if nuevo_color == BG3color else "black")
        BG2 = tk.Frame(ventana4, bg=nuevo_color, width=512, height=32)
        BG2.place(relx=0.0, rely=1.0, anchor='sw', relwidth=1.0, relheight=0.07)
    
   
        # Utiliza resource_path para cargar las imágenes
        imagen_volver_path = self.resource_path("imagenes/volver.png")
        imagen_eliminar_path = self.resource_path("imagenes/eliminar.png")
        imagen_PDF_path = self.resource_path("imagenes/PDF.png")
        imagen_ver_horario_path = self.resource_path("imagenes/ver_horario.png")
        imagen_añadir_path = self.resource_path("imagenes/añadir.png")
        


        
        self.imagen_volver = ImageTk.PhotoImage(Image.open(imagen_volver_path).resize((20, 20)))
        self.imagen_eliminar = ImageTk.PhotoImage(Image.open(imagen_eliminar_path).resize((20, 20)))
        self.imagen_PDF = ImageTk.PhotoImage(Image.open(imagen_PDF_path).resize((20, 20)))
        self.imagen_ver_horario = ImageTk.PhotoImage(Image.open(imagen_ver_horario_path).resize((20, 20)))
        self.imagen_añadir = ImageTk.PhotoImage(Image.open(imagen_añadir_path).resize((20, 20)))



        tk.Label(self.ventana4,text="  Pestaña de Horarios",bg=color_label,fg="white" if color_label == BG3color else "black", font=("arial", 24, "bold")).grid(row=1,column=3,columnspan=3)

        tk.Button(self.ventana4, text="Volver",image=self.imagen_volver,compound="left",height=30 , width=300, command=lambda: self.volver_al_menu(menuFunc,tipoCuenta,nombreCuenta)).grid(row=8, column=4, sticky="e",padx=(0, 10), pady=(0, 0))
        tk.Button(self.ventana4, text="Ver horarios Laboratorios",image=self.imagen_ver_horario,compound="left",height=30 , width=300, command=lambda:self.opcion_ver_horarios("Laboratorio",self.ver_horarios)).grid(row=3, column=3, padx=(0, 10), pady=(0, 0), sticky="E")
        
        self.añadir_lab=tk.Button(self.ventana4, text="Añadir Horarios Laboratorios",image=self.imagen_añadir,compound="left",height=30 , width=300,command=lambda:self.opcion_ver_horarios("Laboratorio",self.añadir_aula))
        self.añadir_lab.grid(row=3, column=4, padx=(0, 10), pady=(0, 0), sticky="E")
        tk.Button(self.ventana4, text="Exportar laboratorio a PDF",image=self.imagen_PDF,compound="left",height=30 , width=300, command=lambda:self.opcion_ver_horarios("Laboratorio",self.exportar_pdf)).grid(row=3, column=5,  padx=(0, 10), pady=(0, 0), sticky="E")
        
        tk.Button(self.ventana4, text="Ver horarios aulas",image=self.imagen_ver_horario,compound="left",height=30 , width=300, command=lambda:self.opcion_ver_horarios("Aula",self.ver_horarios)).grid(row=4, column=3,  padx=(0, 10), pady=(0, 0), sticky="E")
            
            
        self.añadir_aula_b=tk.Button(self.ventana4, text="Añadir horarios horarios aulas",image=self.imagen_añadir,compound="left",height=30 , width=300,command=lambda:self.opcion_ver_horarios("Aula",self.añadir_aula))
        self.añadir_aula_b.grid(row=4, column=4,  padx=(0, 10), pady=(0, 0), sticky="E")
            
            
        tk.Button(self.ventana4, text="Exportar aula a PDF", image=self.imagen_PDF,compound="left",height=30 , width=300,command=lambda:self.opcion_ver_horarios("Aula",self.exportar_pdf)).grid(row=4, column=5, padx=(0, 10), pady=(0, 0), sticky="E")
        
        tk.Button(self.ventana4, text="Ver horarios talleres",image=self.imagen_ver_horario,compound="left",height=30 , width=300, command=lambda:self.opcion_ver_horarios("Taller",self.ver_horarios)).grid(row=5, column=3,  padx=(0, 10), pady=(0, 0), sticky="E")
            
            
        self.añadir_taller=tk.Button(self.ventana4, text="Añadir horarios talleres",image=self.imagen_añadir,compound="left",height=30 , width=300,command=lambda:self.opcion_ver_horarios("Taller",self.añadir_aula))
        self.añadir_taller.grid(row=5, column=4,  padx=(0, 10), pady=(0, 0), sticky="E")
            
       
        tk.Button(self.ventana4,text="Exportar taller a PDF",image=self.imagen_PDF,compound="left",height=30 , width=300, command=lambda:self.opcion_ver_horarios("Taller",self.exportar_pdf)).grid(row=5, column=5,  padx=(0, 10), pady=(0, 0), sticky="E")
        etiqueta_derecha = tk.Label(BG2, text="©6°5 - 2024", bg=nuevo_color,fg="white" ,font=("arial", 16))
        etiqueta_derecha.place(relx = 1.0, rely = 0.5, anchor ='e')
        
        print("Valor de self.tipocuenta:", self.tipocuenta)
        for elemento in self.ventana4.winfo_children():
            if isinstance(elemento, tk.Button):
                elemento['bg'] = "white"
                elemento["borderwidth"] = 0
                changeOnHover(elemento, "#A2AEE0", "white")
        if self.tipocuenta==1:
            self.añadir_lab.config(state=tk.DISABLED)
            self.añadir_aula_b.config(state=tk.DISABLED)
            self.añadir_taller.config(state=tk.DISABLED)
    def volver_al_menu(self,menuFunc,tipoCuenta,nombreCuenta):
        self.eliminar()
        menuFunc(tipoCuenta,nombreCuenta)
    def exportar_pdf(self,numero_aula2,tipo_de_aula1):
        pdf1=PDF(tipo_de_aula1,numero_aula2)
        pdf1.guardar_pdf()
        messagebox.showinfo("Exportar a PDF","PDF Exportado con exito al directorio de descargas")
        
    def conectar_base_de_datos(self):
        self.cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
            )
        # Crear un cursor para ejecutar consultas
        self.cursor = self.cnx.cursor()
    def cerrar_base_de_datos(self):
        self.cursor.close()
        self.cnx.close()
    def opcion_ver_horarios(self,tipo_aula,segunda_funcion):
        def resource_path(self, relative_path):
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        self.aula_ver_horarios= tk.Toplevel()
        self.aula_ver_horarios.resizable(False,False)
        self.aula_ver_horarios.title("Pantalla de horarios")
        self.aula_ver_horarios.configure(bg=nuevo_color)
        path = self.resource_path("Imagenes/Colegio_logo.ico")
        self.aula_ver_horarios.iconbitmap(path)
        botones_frame = ttk.LabelFrame(self.aula_ver_horarios, text="Horarios")
        
        #Temas['scidpink', M.'black', M.'equilux', 'scidgreen', 'xpnative', 'scidgrey', 'classic', M.'radiance', M.'itft1', 'scidmint', M.'ubuntu', 'plastik', 'winxpblue', M.'arc', 'smog', M-'yaru', M-'adapta', 'scidsand', M-'breeze', M-'elegance', M-'clam', 'scidblue', M-'aquativo', 'winnative', 'blue', 'default', 'clearlooks', M-'scidpurple', M-'alt', M-'keramik', 'kroc', 'vista']
        if color_fondo == BG3color:
         style = ThemedStyle(botones_frame)
         style.set_theme("black")
        else : 
         style = ThemedStyle(botones_frame)
         style.set_theme("xpnative")

        botones_frame.pack(padx=10, pady=10)
        self.conectar_base_de_datos()
        self.cursor.execute('SELECT Tipo_de_aula, Numero FROM aulas WHERE Tipo_de_aula = %s ORDER BY Numero ', (tipo_aula,))
        filas = self.cursor.fetchall()
        self.cerrar_base_de_datos()
        if filas:
            for i, fila in enumerate(filas):
                boton = ttk.Button(botones_frame, text=f"{tipo_aula} {fila[1]}", command=lambda r=fila[1]: segunda_funcion(r, tipo_aula))
                boton.grid(row=i // 3, column=i % 3, padx=10, pady=10)
        else:
            tk.Label(botones_frame, text="No hay aulas agregadas").pack()
        
    def ver_horarios(self,numero,tipo_aula):
        self.eliminar()
        self.aula_ver_horarios.destroy()
        self.ventana_horario2= añadir_horario(self.ventana4,tipo_aula,numero,self.menuFunc,self.tipocuenta,self.nombrecuenta)
        self.cerrar_base_de_datos()
        self.ventana_horario2.treeview(True)
        self.ventana_horario2.ejecutar()

    def añadir_aula(self,numero,tipo_aula):
        self.eliminar()
        self.aula_ver_horarios.destroy()
        ventana_horario2= añadir_horario(self.ventana4,tipo_aula,numero,self.menuFunc,self.tipocuenta,self.nombrecuenta)
        ventana_horario2.widgets()
        ventana_horario2.botones()
        self.cerrar_base_de_datos()
        ventana_horario2.ejecutar()
        
        
        
class añadir_horario():
    
    def __init__(self,ventana_horario,tipo_de_aula,numero_de_aula,menuFunc,tipoCuenta,nombreCuenta):
        def resource_path(relative_path):
          try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
          except Exception:
            base_path = os.path.abspath(".")
          return os.path.join(base_path, relative_path)
        
        self.tipocuenta=tipoCuenta
        self.nombrecuenta=nombreCuenta
        self.menuFunc=menuFunc
        self.numero_de_aula=numero_de_aula
        self.tipo_de_aula=tipo_de_aula
        self.ventana_horario=ventana_horario
        
        
        self.frame_pe = ttk.Frame(self.ventana_horario)
        self.frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.volver_imagen = ImageTk.PhotoImage(Image.open(resource_path("Imagenes/volver.png")).resize((15,15)))
        self.eliminar_imagen = ImageTk.PhotoImage(Image.open(resource_path("Imagenes/eliminar.png")).resize((15,15)))
        self.opciones_division=[]
        self.ventana_horario.title("Ver horario")
        self.ventana_horario.geometry("900x500")
        self.configuracion_widgets()

    def configuracion_widgets(self):
        self.frame_superior=ttk.Frame(self.frame_pe)
        self.frame_inferior=ttk.Frame(self.frame_pe)
        self.frame_botones=ttk.Frame(self.frame_superior)
        self.frame_superior.grid(row=0, column=0, sticky="nsew")
        self.frame_inferior.grid(row=1, column=0,sticky="nsew")
        self.frame_botones.grid(row=0,column=4,sticky="nsew",rowspan=4)
        self.frame_pe.columnconfigure(0, weight=1)
        self.frame_pe.rowconfigure(0, weight=2)
        self.frame_pe.rowconfigure(1, weight=8)
        self.frame_inferior.columnconfigure(0, weight=6)
        self.frame_inferior.columnconfigure(1, weight=1)
        self.frame_inferior.rowconfigure(0, weight=1)
        self.frame_botones.columnconfigure(0,weight=1)
        self.frame_botones.rowconfigure(0,weight=1)
        self.frame_botones.rowconfigure(1,weight=1)
        self.frame_botones.rowconfigure(2,weight=1)
    def variables(self):
        self.variable_hora_llegada = tk.StringVar()
        self.variable_hora_salida = tk.StringVar()
        self.variable_tipo_de_aula = tk.StringVar()
        self.variable_numero_aula = tk.IntVar()
        self.variable_grupo = tk.StringVar()
        self.variable_dia = tk.StringVar()
        self.opciones_dia = ["Lunes","Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
        self.opciones_grupos = ["A","A","B","C","D","Ambos"]
        self.opciones_division1 = ["A","B","C","D","E","F"]
        self.opciones_division2 = ["1","2","3","4","5","6","7"]
        self.horarios = []

        def resource_path(relative_path):
         try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
          base_path = sys._MEIPASS
         except Exception:
        # Si no se encuentra la variable _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta actual del script
          base_path = os.path.abspath(".")

    # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
         return os.path.join(base_path, relative_path)
       
        horarios=resource_path('horario.txt')
        with open(horarios, 'r') as archivo:
            for linea in archivo:
                hora, minuto = linea.strip().split(':')
                hora = int(hora)
                minuto = int(minuto)
                self.horarios.append((f"{hora:02d}:{minuto:02d}"))
        
        self.opciones_grados = [0,1,2,3,4,5,6,7]
        self.conectar_a_mysql()
        self.cursor.execute("SELECT DISTINCT MATERIA FROM materias")
        self.materia = self.cursor.fetchall()
        
        self.cursor.execute("SELECT nombre, apellido FROM profesores")
        self.profesor = self.cursor.fetchall()
        
        self.cursor.execute("SELECT Numero FROM aulas WHERE tipo_de_aula=%s", (self.tipo_de_aula,))
        self.aula = self.cursor.fetchall()
        
        self.aula.sort()
        self.opciones_aula=[self.numero_de_aula] + [numero[0] for numero in self.aula]
        self.opciones_tipo_de_aula=[self.tipo_de_aula,"Laboratorio","Aula","Taller"]
        self.opciones_espacio_curricular = [nombre[0] for nombre in self.materia]
        self.opciones_profesor = [f"{nombre} {apellido}" for nombre, apellido in self.profesor]
        self.desconectar_de_mysql()
        
    def widgets(self):
        self.variables()
        
        for x in range(4):
            self.frame_superior.columnconfigure(x, weight=1)
            
        self.current_color = self.ventana_horario.cget("bg")
        style = ttk.Style()
        style.configure('Mi.TLabelframe', background=self.current_color)
        self.frame_superior.configure(style='Mi.TLabelframe')
        self.frame_botones.configure(style="Mi.TLabelframe")
        self.frame_superior.rowconfigure(0, weight=1)
        self.frame_superior.rowconfigure(1, weight=1)
        self.frame_superior.rowconfigure(2, weight=1)
        self.frame_superior.rowconfigure(3, weight=1)
        
        
        ttk.Label(self.frame_superior,text="Horario llegada",font=("Arial", 16),background=self.current_color).grid(row=0, column=0,)
        self.entrada_hora_llegada = AutocompleteEntry(self.horarios,self.frame_superior)
        self.entrada_hora_llegada.grid(row=1, column=0)
        
        label_hora_S=ttk.Label(self.frame_superior,text="Horario salida",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=0, column=1,)
        self.entrada_hora_salida = AutocompleteEntry(self.horarios,self.frame_superior)
        self.entrada_hora_salida.grid(row=1, column=1)

        label_materia=ttk.Label(self.frame_superior,text="Espacio Curricular",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=0, column=2)
        self.espacio_curricular_entry = AutocompleteEntry(self.opciones_espacio_curricular,self.frame_superior)
        self.espacio_curricular_entry.grid(row=1, column=2,sticky="ew")
        
        label_año=ttk.Label(self.frame_superior,text="Curso",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=0, column=3)
        self.optionmenuan = ttk.Combobox(self.frame_superior,values=[1,2,3,4,5,6,7],state="readonly",font=("Arial", 16))
        self.optionmenuan.grid(row=1, column=3)
        
        label_div=ttk.Label(self.frame_superior,text="Division",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=2, column=3)
        self.optionmenudiv = ttk.Combobox(self.frame_superior,values=self.opciones_division,state="readonly",font=("Arial", 16))
        self.optionmenudiv.grid(row=3, column=3)
        
        label_grupo=ttk.Label(self.frame_superior,text="Grupo",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=2, column=0)
        ttk.OptionMenu(self.frame_superior, self.variable_grupo,*self.opciones_grupos).grid(row=3, column=0)
        
        label_prof=ttk.Label(self.frame_superior,text="Profesor",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=2, column=1)
        self.entry_profesor = AutocompleteEntry(self.opciones_profesor,self.frame_superior)
        self.entry_profesor.grid(row=3, column=1)
        
        label_dia=ttk.Label(self.frame_superior,text="Dia",foreground="white" if color_fondo == BG3color else "black",background=self.current_color,font=("Arial", 16)).grid(row=2, column=2)
        tk.OptionMenu(self.frame_superior, self.variable_dia,*self.opciones_dia).grid(row=3, column=2)
        
        tk.Button(self.frame_botones,text="Volver",image=self.volver_imagen,compound="left",command=self.volver,font=("Arial", 16),borderwidth=0,bg="#8d99d7",fg="white").grid(row=0, column=0,sticky="ew")
        
        

        self.espacio_curricular_entry.bind('<FocusOut>', lambda event: self.validar_materia(event, self.espacio_curricular_entry))
        self.entrada_hora_llegada.bind('<FocusOut>', lambda event: self.validar_contenido(event, self.entrada_hora_llegada))
        self.entrada_hora_salida.bind('<FocusOut>', lambda event: self.validar_contenido(event, self.entrada_hora_salida))
        self.entry_profesor.bind('<FocusOut>', lambda event: self.validar_profesor(event, self.entry_profesor))
        self.optionmenuan.bind("<<ComboboxSelected>>", self.actualizar_division)
        
        self.treeview()
        
    def actualizar_division(self,event):
        año_seleccionado = self.optionmenuan.get()
        if int(año_seleccionado) <= 3:
            opciones_division = self.opciones_division1
            self.optionmenudiv.config(values=opciones_division)
            self.optionmenudiv.current(0)
        else:
            opciones_division = self.opciones_division2
            self.optionmenudiv.config(values=opciones_division)
            self.optionmenudiv.current(0)


    def botones(self):
        tk.Button(self.frame_botones,text="Agregar horario",command=self.agregar_horario,font=("Arial", 16),fg="white",bg="#8d99d7",borderwidth=0).grid(row=1, column=0,sticky="ew")
        tk.Button(self.frame_botones,text="Eliminar horario",image=self.eliminar_imagen,bg="red",fg="white",compound="left",borderwidth=0,command=self.eliminar_horario,font=("Arial", 16)).grid(row=2, column=0,sticky="ew")


    def eliminar_horario(self):
        mensaje_confirmar=messagebox.askokcancel("Eliminar","Realmente desea eliminar el horario?")
        if mensaje_confirmar:
            try:
                    self.conectar_a_mysql()
                    selected_items = self.my_treeview.selection()
                    if not selected_items:
                        messagebox.showerror("Error", "Seleccione al menos un horario")
                        return
                    
                    for item in selected_items:
                        horario_id = self.my_treeview.item(item, "values")[0]
                        self.cursor.execute("DELETE FROM horarios WHERE id_hor=%s", (horario_id,))
                        self.my_treeview.delete(item)
                    
                    self.cnx.commit()
                    if len(selected_items) == 1:
                        messagebox.showinfo("Horario", "Horario eliminado")
                    else:
                        messagebox.showinfo("Horarios", "Horarios eliminados")
        
            except:
                messagebox.showerror("Error", "Seleccione al menos un horario")
            finally:
                self.desconectar_de_mysql()
        else:
            pass
    def validar_horario(self):
        for i,element in enumerate(self.__data):
            if element[3] == self.hora_llegada_get and element[4] == self.hora_salida_get:
                messagebox.showinfo("Horario", "Horario invalido, ya existe en la base de datos")
                return False
        if self.hora_llegada_get == self.hora_salida_get:
            messagebox.showerror("Error", "Los horarios no pueden ser siguales")
            return False
        elif self.hora_salida_get < self.hora_llegada_get:
            messagebox.showerror("Error", "La hora de salida no puede ser menor a la hora de llegada")
            return False
        elif self.calcular_diferencia_horas(self.hora_llegada_get, self.hora_salida_get) < 1:
            messagebox.showerror("Error", "Tiene que haber minimo una hora de diferencia entre la hora de llegada y la hora de salida")
            return False
        elif self.profesor_get=="" or self.espacio_curricular_get=="" or self.hora_llegada_get=="" or self.hora_salida_get=="":
            messagebox.showerror("Error", "Debe ingresar todos los datos")
            return False
        else:
            return True
    def agregar_horario(self):
        askyesnoal = messagebox.askyesno("Horario", "¿Desea agregar el horario?")
        if askyesnoal:
            try:
                numero_a_dia = {
                    1: "Lunes",
                    2: "Martes",
                    3: "Miércoles",
                    4: "Jueves",
                    5: "Viernes"
                }
                self.conectar_a_mysql()
                self.obtener_datos()
                if self.validar_horario==False:
                    pass
                else:
                    self.cursor.execute("""INSERT INTO horarios(Numero_aula,Tipo_de_aula,Horario_e,Horario_s,Espacio_curricular,Año,Division,Grupo,Profesor,Dia)
                                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(self.aula_get,self.aula_tipo_get,self.hora_llegada_get,self.hora_salida_get,self.espacio_curricular_get,self.año_get,self.division_get,self.grupo_get,self.profesor_get,self.dia_get))
                    self.cnx.commit()
                    self.cursor.execute("SELECT ID_hor FROM horarios ORDER BY ID_hor DESC;")
                    id_profesor=self.cursor.fetchone()
                    messagebox.showinfo("Horario","Horario agregado")
                    self.dia_get = numero_a_dia.get(self.dia_get,"")                 
                    self.my_treeview.insert(parent='', index='end', values=(id_profesor,self.aula_get,self.aula_tipo_get,self.hora_llegada_get,self.hora_salida_get,self.espacio_curricular_get,self.año_get,self.division_get,self.grupo_get,self.profesor_get,self.dia_get))
            except mysql.connector.Error as err:
                print(err)
                messagebox.showerror("Error","No se pudo agregar el horario")
            finally:
                self.desconectar_de_mysql()
        
    def treeview(self,backyesno=False):
        self.frame = self.frame_inferior
        self.scrollbar = ttk.Scrollbar(self.frame)
        self.scrollbar.pack(side="right", fill="y")

        self.my_treeview = ttk.Treeview(self.frame,yscrollcommand=self.scrollbar.set, selectmode="extended")
        self.my_treeview.pack(fill="both", expand=True)
        
        
        self.scrollbar.config(command=self.my_treeview.yview)
        if backyesno==True:
            ttk.Button(self.frame_superior,text="Volver",image=self.volver_imagen,compound="left",command=self.volver).grid(row=0, column=5,rowspan=1)
        self.my_treeview["columns"] = ("ID","Numero de aula","Tipo de aula","Horario llegada","Horario salida","Espacio Curricular","Curso","Division","Grupo","Profesor","Dia")
        self.my_treeview.column("#0", width=0, stretch=0)
        self.my_treeview.column("ID", anchor="center", width=1)
        self.my_treeview.column("Numero de aula", anchor="center", width=50)
        self.my_treeview.column("Tipo de aula", anchor="center", width=30)
        self.my_treeview.column("Horario llegada", anchor="center", width=45)
        self.my_treeview.column("Horario salida", anchor="center", width=40)
        self.my_treeview.column("Espacio Curricular", anchor="center", width=55)
        self.my_treeview.column("Curso", anchor="center", width=20)
        self.my_treeview.column("Division", anchor="center", width=20)
        self.my_treeview.column("Grupo", anchor="center", width=20)
        self.my_treeview.column("Profesor", anchor="center", width=20)
        self.my_treeview.column("Dia", anchor="center", width=20)
        
        self.my_treeview.heading("#0", text="", anchor="w")
        self.my_treeview.heading("ID", text="ID", anchor="center")
        self.my_treeview.heading("Numero de aula", text="Numero de aula", anchor="center")
        self.my_treeview.heading("Tipo de aula", text="Tipo de aula", anchor="center")
        self.my_treeview.heading("Horario llegada", text="Horario llegada", anchor="center")
        self.my_treeview.heading("Horario salida", text="Horario salida", anchor="center")
        self.my_treeview.heading("Espacio Curricular", text="Espacio Curricular", anchor="center")
        self.my_treeview.heading("Curso", text="Curso", anchor="center")
        self.my_treeview.heading("Division", text="Division", anchor="center")
        self.my_treeview.heading("Grupo", text="Grupo", anchor="center")
        self.my_treeview.heading("Profesor", text="Profesor", anchor="center")
        self.my_treeview.heading("Dia", text="Dia", anchor="center")
        self.insertar_tree()
        
    def insertar_tree(self):
        self.conectar_a_mysql()
        numero_a_dia = {
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes"
        }
        
        self.cursor.execute("SELECT * FROM horarios WHERE Numero_aula=%s AND tipo_de_aula=%s ORDER BY Horario_e", (self.numero_de_aula,self.tipo_de_aula)) 
        self.__data = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM horarios WHERE (CURTIME() BETWEEN `Horario_e` AND `Horario_s` AND DAYOFWEEK(NOW()) - 1 = Dia) AND Numero_aula=%s AND tipo_de_aula=%s; ", (self.numero_de_aula,self.tipo_de_aula))
        self.horario_actual = self.cursor.fetchall()
        
        self.__data=[elemento for elemento in self.__data if elemento not in self.horario_actual]
        self.__data = [list(row) for row in self.__data]
        self.horario_actual = [list(row) for row in self.horario_actual]
        
        for i, elemento in enumerate(self.__data):
            dia_numero = elemento[10]
            dia_nombre = numero_a_dia.get(dia_numero, "")
            self.__data[i][10] = dia_nombre
        for i, elemento in enumerate(self.horario_actual):
            dia_numero = elemento[10]
            dia_nombre = numero_a_dia.get(dia_numero, "desconocido")
            self.horario_actual[i][10] = dia_nombre

        
        self.my_treeview.tag_configure("meowrow",background="#6B8F71")
        for i in self.horario_actual:
            self.my_treeview.insert(parent='', index='end', values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],i[10]), tags=("meowrow", i[1]))
        for x in self.__data:
            self.my_treeview.insert(parent='', index='end', values=(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9],x[10]), tags=(x[1],))

    def validar_materia(self, event, entry_widget):
        self.espacio_curricular_entry.hide_listbox(self.ventana_horario)
        widget_con_enfoque = self.ventana_horario.focus_get()
        if isinstance(widget_con_enfoque, tk.Listbox) or isinstance(widget_con_enfoque, tk.Entry):
            return
        entrada = entry_widget.get()
        if not entrada in self.opciones_espacio_curricular:
            messagebox.showerror("Error", "La materia no existe")

    def validar_profesor(self, event, entry_widget):
        self.entry_profesor.hide_listbox(self.ventana_horario)
        widget_con_enfoque = self.ventana_horario.focus_get()
        if isinstance(widget_con_enfoque, tk.Listbox) or isinstance(widget_con_enfoque, tk.Entry):
            return
        entrada = entry_widget.get()
        if not entrada in self.opciones_profesor:
            messagebox.showerror("Error", "El profesor no existe")
            
    def calcular_diferencia_horas(self,hora_llegada, hora_salida):
        hora_llegada_obj = datetime.strptime(hora_llegada, "%H:%M")
        hora_salida_obj = datetime.strptime(hora_salida, "%H:%M")
        self.diferencia = hora_salida_obj - hora_llegada_obj
        return self.diferencia.total_seconds() / 3600 
    
    def validar_contenido(self, event, entry_widget):
        entry_widget.hide_listbox(self.ventana_horario)
        widget_con_enfoque = self.ventana_horario.focus_get()
        
        if isinstance(widget_con_enfoque, tk.Listbox) or isinstance(widget_con_enfoque, tk.Entry):
            return
        entrada = entry_widget.get()
        try:
            if any(c.isalpha() for c in entrada):
                messagebox.showerror("Error", "El contenido contiene letras. Debe ser numérico.")
                entry_widget.delete(0, tk.END)
                
            elif len(entrada)==4:
                if int(entrada[0:1]) <=6 or int(entrada[3:5]) >=60 or int(entrada[3:5])%5 != 0:
                    messagebox.showerror("Error", "El contenido tiene que tener un horario valido")
                    entry_widget.delete(0, tk.END)
                else:
                    pass
                
            if not entrada in self.horarios:
                messagebox.showerror("Error", "El horario no es valido")
                entry_widget.delete(0, tk.END)
                
            elif int(entrada[0:2]) >=22 or int(entrada[0:2]) <=6 or int(entrada[3:5]) >=60 or int(entrada[3:5])%5 != 0:
                messagebox.showerror("Error", "El contenido tiene que tener un horario valido")
                entry_widget.delete(0, tk.END)
                
            elif len(entrada)>5 or len(entrada)<4:
                messagebox.showerror("Error", "El contenido tiene que tener menos de 5 caracteres o mas de 4")
                entry_widget.delete(0, tk.END)
        except ValueError:
            pass
    
    def obtener_datos(self):
        self.dias_a_numeros = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
        self.aula_get = self.numero_de_aula
        self.aula_tipo_get = self.tipo_de_aula
        self.hora_llegada_get = self.entrada_hora_llegada.get()
        self.hora_salida_get = self.entrada_hora_salida.get()
        self.espacio_curricular_get = self.espacio_curricular_entry.get()
        self.año_get = self.optionmenuan.get()
        self.division_get = self.optionmenudiv.get()
        self.grupo_get = self.variable_grupo.get()
        self.profesor_get = self.entry_profesor.get()
        self.dia_get = self.variable_dia.get()
        self.dia_get = self.dias_a_numeros.get(self.dia_get.capitalize(), 0)
    
    def volver(self):
        self.eliminar()
        ventana_horario2= menu_horarios()
        print(self.menuFunc,self.tipocuenta,self.nombrecuenta)
        ventana_horario2.horarios(self.ventana_horario,self.menuFunc,self.tipocuenta,self.nombrecuenta)
    def eliminar(self):
        for elemento in self.ventana_horario.winfo_children():
            elemento.destroy()
    def conectar_a_mysql(self):
        try:
                self.cnx = mysql.connector.connect(
                host='eestn1.com.ar',
                user='tecnica1',
                password='z%51#q57A7BR',
                database='tec_boletines2023',
                port=3306
                )
                self.cursor = self.cnx.cursor()
        except Exception as e:
                print(e)
                messagebox.showerror("Error", "No se pudo conectar a la base de datos")
                self.cnx.rollback()
    def desconectar_de_mysql(self):
        self.cursor.close()
        self.cnx.close()
    def ejecutar(self):
        self.ventana_horario.mainloop()

if __name__ == "__main__":
    ventana_horario = tk.Tk()
    ventana_horario2= menu_horarios()
    menufunc="fsagas"
    tipoCuenta="asddsa"
    nombreCuenta="lala"
    ventana_horario2.horarios(ventana_horario,menufunc,tipoCuenta,nombreCuenta)
    ventana_horario.mainloop()