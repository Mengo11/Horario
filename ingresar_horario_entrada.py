import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from CompletarAU import AutocompleteEntry
import mysql.connector
import sys,os
import alumnos
class horario_entrada_class:
    def __init__(self, ventanaCC, menuFunc, tipoCuenta, nombreCuenta,Curso,Division):
        self.curso1 = Curso
        self.division1 = Division
        self.ventanaCC = ventanaCC
        self.menuFunc = menuFunc
        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.ventanaCC.title("Horarios de llegada")
        self.frame_t = ttk.Frame(self.ventanaCC)
        self.frame_t.place(x=0, y=0, relwidth=1, relheight=1)
        self.configuracion_widgets()
        
    def configuracion_widgets(self):
        
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
        self.widgets_cursos()
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
        
        Button(self.frame_botones, text="Volver", command=self.volver).grid(row=0, column=0, sticky="nsew", padx=15, pady=5)
        Button(self.frame_botones, text="Agregar").grid(row=1, column=0, sticky="nsew", padx=15, pady=5)
        self.ingresar_treeview()
        
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
    def volver(self):
        self.eliminar()
        from Pestaña_qr import clase_qr
        clase_qr(self.ventanaCC,self.menuFunc,self.tipocuenta,self.nombrecuenta)
    def eliminar(self):
        for elemento in self.ventanaCC.winfo_children():
            elemento.destroy()
    def ingresar_treeview(self):
        self.scrollbar = Scrollbar(self.frame_treeview)
        self.scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.frame_treeview, yscrollcommand=self.scrollbar.set,selectmode="extended")
        self.tree.pack(fill="both", expand=True)
        self.tree["columns"] = ("ID_horario","Curso","Division","Turno","Horario llegada","Dia","Grupo")

        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("ID_horario", anchor=CENTER, width=100)
        self.tree.column("Curso", anchor=CENTER, width=100)
        self.tree.column("Division", anchor=CENTER, width=100)
        self.tree.column("Turno", anchor=CENTER, width=100)
        self.tree.column("Horario llegada", anchor=CENTER, width=100)
        self.tree.column("Dia", anchor=CENTER, width=100)
        self.tree.column("Grupo", anchor=CENTER, width=100)
        
        self.tree.heading("#0", text="", anchor=CENTER)
        self.tree.heading("ID_horario", text="ID_horario", anchor=CENTER)
        self.tree.heading("Curso", text="Curso", anchor=CENTER)
        self.tree.heading("Division", text="Division", anchor=CENTER)
        self.tree.heading("Turno", text="Turno", anchor=CENTER)
        self.tree.heading("Horario llegada", text="Horario llegada", anchor=CENTER)
        self.tree.heading("Dia", text="Dia", anchor=CENTER)
        self.tree.heading("Grupo", text="Grupo", anchor=CENTER)

        self.scrollbar.config(command=self.tree.yview)
        self.conectar_base_de_datos()
        self.cursor.execute("SELECT id_horario,c.curso,c.division,turno,horario_llegada,dia,grupo FROM horarios_entrada h JOIN cursos c ON c.id_curso = h.id_curso WHERE c.curso=%s AND c.division=%s", (self.curso1, self.division1))
        resultado=self.cursor.fetchall()

        for i, row in enumerate(resultado):
            self.tree.insert("", "end", text="", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        self.cerrar_base_de_datos()