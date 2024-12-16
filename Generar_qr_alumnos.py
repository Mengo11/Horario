import tkinter as tk
from tkinter import ttk, IntVar, StringVar
import mysql.connector
from ttkthemes import ThemedStyle
from tkinter import messagebox
import os, sys
from PIL import Image
import qrcode
from PIL import ImageTk, Image
from fpdf import FPDF
import webbrowser

class Generar_Qr:
    
    def __init__(self, ventana_qr, menuFunc, tipoCuenta, nombreCuenta):
        def resource_path(relative_path):
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        self.tipocuenta = tipoCuenta
        self.nombrecuenta = nombreCuenta
        self.menuFunc = menuFunc
        self.ventana_qr = ventana_qr

        self.frame_pe = ttk.Frame(self.ventana_qr)
        self.frame_pe.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame_pe.rowconfigure(0, weight=4)
        self.frame_pe.rowconfigure(1, weight=8)
        self.frame_pe.columnconfigure(0, weight=1)
        self.volver_imagen = ImageTk.PhotoImage(Image.open(resource_path("Imagenes/volver.png")).resize((15, 15)))
        self.eliminar_imagen = ImageTk.PhotoImage(Image.open(resource_path("Imagenes/eliminar.png")).resize((15, 15)))
        self.ventana_qr.title("Generar QR")
        self.configuracion_widgets()

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

    def on_enter_lega(self, event):
        self.nombre = self.nombre.get().capitalize()  
        self.nombre.set(self.nombre)
        self.txtnm.focus()
    
    def on_enter_name(self, event):
        self.nombre = self.nombre.get().capitalize()  
        self.nombre.set(self.nombre)
        self.txtap.focus()
        
    def validar_numeros(P):
        if all(c.isdigit() for c in P):
            return True
        else:
            messagebox.showerror("Error", "Solo se permiten números")
            return False 

    def configuracion_widgets(self):
        self.current_color = self.ventana_qr.cget("bg")
        self.style_all=ttk.Style()
        if  self.current_color== "#1b284f":
            self.style_all = ThemedStyle(self.ventana_qr)
            self.style_all.set_theme("black")
        else : 
            style = ThemedStyle(self.ventana_qr)
            style.set_theme("xpnative")
            
        self.frame_inferior = ttk.Frame(self.frame_pe)
        arriba_designacion = ttk.Frame(self.frame_pe)
        arriba_designacion.grid(row=0, column=0, sticky="nsew")
        self.frame_inferior.grid(row=1, column=0, sticky="nsew")
        style = ttk.Style()
        style.configure('Mi.TLabelframe', background=self.current_color)
        arriba_designacion.configure(style='Mi.TLabelframe')
        arriba_designacion.columnconfigure(0, weight=1)
        arriba_designacion.columnconfigure(1, weight=1)
        arriba_designacion.columnconfigure(2, weight=1)
        arriba_designacion.rowconfigure(0, weight=1)
        arriba_designacion.rowconfigure(1, weight=1)
        
        
        boton_volver = tk.Button(arriba_designacion, text="Volver", command=self.volver,width=10,font=("Futura", 16),borderwidth=0,bg="#0e79b2",fg="white")
        boton_volver.grid(row=0, column=2,sticky="nes",padx=20,pady=10)

        boton_generar_qr = tk.Button(arriba_designacion, text="QR", command=self.generar_qr,width=10,font=("Futura", 16),borderwidth=0,bg="#0e79b2",fg="white")
        boton_generar_qr.grid(row=1, column=2,pady=10, padx=20,sticky="nes")
        
        self.tree_alumnos()

    def tree_alumnos(self):
        self.scrollbar = ttk.Scrollbar(self.frame_inferior)
        self.scrollbar.pack(side="right", fill="y")

        self.tvtAgregaralumnos = ttk.Treeview(self.frame_inferior, yscrollcommand=self.scrollbar.set, selectmode="extended")
        self.tvtAgregaralumnos.pack(expand=True, fill="both")
        
        self.tvtAgregaralumnos["columns"] = ("Legajo", "Nombre", "DNI", "Edad", "Curso", "Division", "Nombre_padre")
        self.tvtAgregaralumnos.column("#0", width=0, stretch=0)
        self.tvtAgregaralumnos.heading("#0", text="") 



        # Configuración de los encabezados
        self.tvtAgregaralumnos.heading("Legajo", text="Numero de legajo")
        self.tvtAgregaralumnos.heading("Nombre", text="Nombre y Apellido")
        self.tvtAgregaralumnos.heading("DNI", text="DNI")
        self.tvtAgregaralumnos.heading("Edad", text="Edad")
        self.tvtAgregaralumnos.heading("Curso", text="Curso")
        self.tvtAgregaralumnos.heading("Division", text="División")
        self.tvtAgregaralumnos.heading("Nombre_padre", text="Nombre del padre")
        
        # Configuración de tamaño de columnas
        self.tvtAgregaralumnos.column("Legajo", width=120)
        self.tvtAgregaralumnos.column("Nombre", width=150)
        self.tvtAgregaralumnos.column("DNI", width=60)
        self.tvtAgregaralumnos.column("Edad", width=50)
        self.tvtAgregaralumnos.column("Curso", width=80)
        self.tvtAgregaralumnos.column("Division", width=100)
        self.tvtAgregaralumnos.column("Nombre_padre", width=150)
        
        # Insertar datos desde la base de datos
        self.cargar_datos()

    def cargar_datos(self):
        try:
            self.conectar_base_de_datos()
            
            # Ajustar la consulta SQL según tu estructura
            query = """
            SELECT N_Legajo, Nombre_y_Apellido, DNI, edad, Curso, Division, nombre_tutor
            FROM alumnos
            """
            cursor.execute(query)
            rows = cursor.fetchall()

            # Insertar los datos en el Treeview
            for row in rows:
                # Asegúrate de que los datos se correspondan con las columnas
                self.tvtAgregaralumnos.insert("", "end", values=row)

            # Cerrar el cursor y la conexión
            cursor.close()
            cnx.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

    def volver(self):
        self.eliminar()
        from Pestaña_qr import clase_qr
        clase_qr(self.ventana_qr,self.menuFunc,self.tipocuenta,self.nombrecuenta)
    def eliminar(self):
        for elemento in self.ventana_qr.winfo_children():
            elemento.destroy()

    def generar_qr(self):
        selected_items = self.tvtAgregaralumnos.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Por favor selecciona uno o más alumnos.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for item in selected_items:
            item_values = self.tvtAgregaralumnos.item(item, "values")
            legajo = item_values[0]
            
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(legajo)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            qr_filename = f"{legajo}.png"
            img.save(qr_filename)

            # Añadir QR al PDF
            pdf.image(qr_filename, x=10, y=pdf.get_y(), w=50)
            pdf.ln(60)

            # Eliminar archivo QR temporal
            os.remove(qr_filename)

        
        # Guardar PDF
        output_path = 'registro_matricula.pdf'
        pdf.output(output_path)
        webbrowser.open_new_tab(f'file://{os.path.abspath(output_path)}')
        messagebox.showinfo("Éxito", f"Códigos QR guardados en {output_path}")
