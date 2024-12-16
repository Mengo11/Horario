import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from CompletarAU import AutocompleteEntry
import mysql.connector
import sys,os
import alumnos

class Cambiar_de_curso:
    def __init__(self, ventanaCC, menuFunc, tipoCuenta, nombreCuenta,Curso,Division,ver=False):
        self.curso1 = Curso
        self.division1 = Division
        self.ventanaCC = ventanaCC
        self.menuFunc = menuFunc
        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.ventanaCC.title("Cambio de Cursos")
        
        def resource_path(relative_path):
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
        self.frame_t = ttk.Frame(self.ventanaCC)
        self.frame_t.place(x=0, y=0, relwidth=1, relheight=1)
        self.configuracion_widgets(ver)
        
    def configuracion_widgets(self,ver):
        
        self.frame_superior = ttk.LabelFrame(self.frame_t)
        self.frame_superior.grid(row=0, column=0, sticky="nsew")
        self.frame_treeview = ttk.LabelFrame(self.frame_t)
        self.frame_treeview.grid(row=1, column=0, sticky="nsew")
        
        self.frame_t.columnconfigure(0, weight=1)
        self.frame_t.rowconfigure(0, weight=1)
        self.frame_t.rowconfigure(1, weight=1)
        
        self.frame_superior.columnconfigure(0, weight=4)
        self.frame_superior.columnconfigure(1, weight=1)
        self.frame_superior.rowconfigure(0, weight=1)
        self.frame_superior.rowconfigure(1, weight=1)
        if ver==False:
            self.widgets_cursos()
        else:
            self.widget_ver()
        
    def widgets_cursos(self):
        self.frame_cursos=ttk.LabelFrame(self.frame_superior)
        self.frame_divisiones=ttk.LabelFrame(self.frame_superior)
        self.frame_botones=ttk.LabelFrame(self.frame_superior)
        #se configura los frames
        self.frame_cursos.grid(row=0, column=0, sticky="nsew")
        self.frame_divisiones.grid(row=1, column=0, sticky="nsew")
        self.frame_botones.grid(row=0, column=1,rowspan=2, sticky="nsew")
        
        self.frame_cursos.rowconfigure(0, weight=1)
        self.frame_divisiones.rowconfigure(0, weight=1)
        
        self.frame_botones.rowconfigure(0, weight=1)
        self.frame_botones.rowconfigure(1, weight=1)
        self.frame_botones.rowconfigure(2, weight=1)
        self.frame_botones.columnconfigure(0, weight=1)
        for x in range(1, 8):
            self.frame_cursos.columnconfigure(x-1, weight=1)
            self.frame_divisiones.columnconfigure(x-1, weight=1)
        for x in range(1, 8):
            boton = Button(self.frame_cursos, text=f"{x}º", command=lambda x=x: self.actualizar_Cursos(x))
            boton.grid(row=0, column=x-1, sticky="nsew", padx=15, pady=5)
            
            if x == 1:  # Seleccionar el primer curso por defecto
                self.actualizar_Cursos(x)
        Button(self.frame_botones, text="Volver", command=self.volver).grid(row=0, column=0, sticky="nsew", padx=15, pady=5)
        Button(self.frame_botones, text="Cambiar", command=self.actualizar_curso_seleccionado_db).grid(row=1, column=0, sticky="nsew",padx=15, pady=5)
        self.ingresar_treeview()
        
    def widget_ver(self):
        frame_b=Frame(self.frame_superior)
        frame_b.grid(row=0, column=0, sticky="nsew", padx=50, pady=60,columnspan=2,rowspan=2)
        frame_b.columnconfigure(0, weight=1)
        frame_b.rowconfigure(0, weight=1)
        Button(frame_b, text="Volver",fg="white",font=("arial",30),width=30,anchor="center",bg="#FF0035", command=self.volver, borderwidth=0).grid(row=0,padx=3, pady=3, column=0)
        self.ingresar_treeview()
        
    def actualizar_Cursos(self,curso):
        
        self.curso_seleccionado = curso

        # Limpia los botones actuales en frame_divisiones
        for widget in self.frame_divisiones.winfo_children():
            widget.destroy()

        # Si el curso es mayor a 3, mostrar divisiones numéricas
        if curso > 3:
            divisiones = range(1, 7)  # Números del 1 al 6
            self.division_seleccionada=1
        else:
            divisiones = ['A', 'B', 'C', 'D', 'E']  # Letras de la A a la E
            self.division_seleccionada='A'

        for i, division in enumerate(divisiones):
            boton = Button(self.frame_divisiones, text=str(division), command=lambda d=division: self.seleccionar_division(d))
            boton.grid(row=0, column=i, sticky="nsew", padx=20, pady=5)
        self.actualizar_label()
    def actualizar_label(self):
        Label(self.frame_botones, text="Su/Sus alumno/s va a pasar de\nCurso :"+str(self.curso1)+" Division:"+str(self.division1)+ "\nAl nuevo año:\nCurso:"+str(self.curso_seleccionado)+" Division:"+str(self.division_seleccionada),bg="#0D090A", fg="white", padx=10, pady=20).grid(row=2, column=0, sticky="nsew")
    def seleccionar_division(self, division):
        # Almacenar la división seleccionada
        self.division_seleccionada = division
        self.actualizar_label()
    def actualizar_curso_seleccionado_db(self):
        self.conectar_base_de_datos()
        seleccionados = self.tree.selection()
        
        if not seleccionados:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún alumno.")
            self.cerrar_base_de_datos()
            return

        for seleccionado in seleccionados:
            self.legajo_seleccionado = self.tree.item(seleccionado)['values'][0]
            self.cursor.execute("UPDATE alumnos SET curso=%s, division=%s WHERE N_Legajo=%s", 
                                (self.curso_seleccionado, self.division_seleccionada, self.legajo_seleccionado))
        
        self.cnx.commit()
        
        for seleccionado in seleccionados:
            self.tree.item(seleccionado, values=(self.legajo_seleccionado,
                                                  self.tree.item(seleccionado)['values'][1], 
                                                  self.curso_seleccionado, 
                                                  self.division_seleccionada, 
                                                  self.tree.item(seleccionado)['values'][4]))

        self.cerrar_base_de_datos()
        messagebox.showinfo("Éxito", "Se han cambiado los cursos correctamente")
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
    def ingresar_treeview(self):
        self.scrollbar = Scrollbar(self.frame_treeview)
        self.scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.frame_treeview, yscrollcommand=self.scrollbar.set,selectmode="extended")
        self.tree.pack(fill="both", expand=True)
        self.tree["columns"] = ("N_Legajo", "Nombre_y_apellido", "Curso", "Division","DNI")
        self.tree.column("#0", width=0, stretch=0)
        self.tree.column("N_Legajo", anchor="center", width=50)
        self.tree.column("Nombre_y_apellido", anchor="center", width=100)
        self.tree.column("Curso", anchor="center", width=50)
        self.tree.column("Division", anchor="center", width=50)
        self.tree.column("DNI", anchor="center", width=50)
        self.tree.heading("#0", text="", anchor="center")
        self.tree.heading("N_Legajo", text="N° Legajo", anchor="center")
        self.tree.heading("Nombre_y_apellido", text="Nombre_y_apellido", anchor="center")
        self.tree.heading("Curso", text="Curso", anchor="center")
        self.tree.heading("Division", text="Division", anchor="center")
        self.tree.heading("DNI", text="DNI", anchor="center")

        self.scrollbar.config(command=self.tree.yview)
        self.conectar_base_de_datos()
        self.cursor.execute("SELECT N_legajo,Nombre_y_apellido,Curso,Division,DNI FROM alumnos WHERE curso=%s AND division=%s", (self.curso1, self.division1))
        resultado=self.cursor.fetchall()

        for i, row in enumerate(resultado):
            self.tree.insert("", "end", text="", values=(row[0], row[1], row[2], row[3], row[4]))
        self.cerrar_base_de_datos()
        
    def volver(self):
        self.eliminar()
        from alumnos import clase_alumnos
        clase_alumnos(self.ventanaCC,self.menuFunc,self.tipocuenta,self.nombrecuenta)
    def eliminar(self):
        for elemento in self.ventanaCC.winfo_children():
            elemento.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = Cambiar_de_curso(root, None, 1, "NombreCuenta",6,5)
    root.mainloop()