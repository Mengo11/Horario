import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
import qrcode as qr
import mysql.connector
from PIL import Image, ImageTk
from datetime import datetime, time, timedelta
from Gif_class import GifPlayer
import os,sys
class Ingresar_Asistencias_qr:
    def __init__(self,ventana_asis,menuFunc,tipoCuenta,nombreCuenta):
        self.ventana_asis=ventana_asis
        self.menuFunc=menuFunc
        self.tipocuenta=tipoCuenta
        self.nombrecuenta=nombreCuenta
        self.scanned_code = ""
        self.ventana_asis.title("Ingresar Asistencias")
        self.procesando = False  # Flag para evitar múltiples ejecuciones
        self.frame_t=ttk.Frame(self.ventana_asis)
        self.frame_t.place(x=0, y=0, relwidth=1, relheight=1)

        self.frame_t.columnconfigure(0, weight=1)
        self.frame_t.rowconfigure(0, weight=1)
        self.frame_t.rowconfigure(1, weight=4)
        self.configuracion_widgets()
    def resource_path(self,relative_path):
            try:
                # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                # Si no se encuentra _MEIPASS, asumimos que estamos en un entorno de desarrollo y obtenemos la ruta del script
                base_path = os.path.abspath(".")
            # Combinar la ruta base con la ruta relativa del recurso para obtener la ruta absoluta
            return os.path.join(base_path, relative_path)    
    def configuracion_widgets(self):
        self.frame_superior = ttk.Frame(self.frame_t)
        self.frame_superior.grid(row=0, column=0, sticky="nsew")
        self.frame_treeview = ttk.Frame(self.frame_t)
        self.frame_treeview.grid(row=1, column=0, sticky="nsew")
        self.frame_superior.columnconfigure(0, weight=1)
        self.frame_superior.rowconfigure(0, weight=1)
        self.frame_superior.rowconfigure(1, weight=1)
        self.frame_superior.columnconfigure(1, weight=1)
        self.widgets()
        

        
    def widgets(self):
        self.frame_superior.bind('<KeyPress>', self.on_key_press)
        self.frame_superior.focus_set()
        self.current_color = self.ventana_asis.cget("bg")
        style = ttk.Style()
        style.configure('Mi.TLabelframe', background=self.current_color)
        self.frame_superior.configure(style='Mi.TLabelframe')
        Button(self.frame_superior, text="Volver", command=self.volver,width=10,font=("Futura", 16),borderwidth=0,bg="#8d99d7",fg="white").grid(row=0, column=1,sticky="nes",padx=10,pady=10)
        self.gif_path =self.resource_path("Imagenes/Qr_scan.gif")
        self.gif_scan =GifPlayer(self.frame_superior,self.gif_path)
        self.gif_scan.bind('<KeyPress>', self.on_key_press)
        self.gif_scan.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.gif_scan.configure(bg=self.current_color)
        self.ingresar_treeview()
        
    def on_ctrl_v_press(self, event):
        pasted_text = self.ventana_asis.clipboard_get()
        # Extraer solo los dígitos ignorando el primer carácter si es un carácter especial
        pasted_text = pasted_text[1:]
        self.scanned_code += pasted_text
        print(f'Código escaneado: {self.scanned_code}')
        self.procesar_codigo()
    def buscar_legajo(self):
        num_legajo = self.entry_legajo.get().strip()
        if num_legajo.isdigit():
            dia_actual = datetime.today().date()
            dia_semana = dia_actual.weekday() + 1  # weekday() devuelve 0 = lunes, ajusta sumando 1
            hora_actual = datetime.now().time()

            if time(7, 40) <= hora_actual <= time(12, 5):
                turno = "mañana"
            elif time(12, 5) < hora_actual < time(17, 30):
                turno = "tarde"
            elif time(17, 30) <= hora_actual <= time(21, 50):
                turno = "vespertino"
            else:
                turno = "FR"

            self.buscar_alumno(num_legajo, dia_semana, turno)
        else:
            messagebox.showerror("Error", "Por favor, ingresa un número de legajo válido.")
    def buscar_alumno(self,num_legajo,dia,turno):
        hora_entrada_dt = datetime.now()

        # Crear el timedelta basado en la hora actual
        self.hora_entrada = timedelta(hours=hora_entrada_dt.hour, 
                                    minutes=hora_entrada_dt.minute, 
                                    seconds=hora_entrada_dt.second)
        print(num_legajo,dia,turno)
        # Obtener el horario esperado para el alumno según su legajo
        query = '''
            SELECT 
                a.N_Legajo,
                c.Curso,
                c.Division,
                h.horario_llegada AS Hora_Entrada,
                h.turno
            FROM 
                alumnos a
            JOIN 
                cursos c ON a.Curso = c.Curso AND a.Division = c.Division
            JOIN 
                horarios_entrada h ON c.id_Curso = h.id_curso 
                AND (h.grupo = 'ambos' OR a.Grupo = h.grupo)
            WHERE 
                a.N_Legajo = %s
                AND h.Dia = %s
                AND h.turno LIKE %s
        '''
        if turno == "FR":
            messagebox.showerror("Error", "Turno fuera de horario")
            return
        else:
            self.conectar_base_de_datos()
            self.cursor.execute(query, (num_legajo, dia, turno))
            resultado = self.cursor.fetchone()
            print(resultado)

        if resultado:
            # Convertir el horario esperado a timedelta
            horario_esperado_dt = datetime.strptime(str(resultado[3]), '%H:%M:%S')
            horario_esperado = timedelta(hours=horario_esperado_dt.hour, 
                                        minutes=horario_esperado_dt.minute, 
                                        seconds=horario_esperado_dt.second)

            # Tolerancia de tiempo
            tolerancia = timedelta(minutes=10)

            # Comparación para determinar si el alumno llegó a tiempo1
            if horario_esperado <= self.hora_entrada <= horario_esperado + tolerancia:
                print("El alumno llegó a tiempo, no se cuenta como falta.")
                print("Horario esperado:", horario_esperado)
                print("Horario actual:", self.hora_entrada)
                llegada_tarde="No"
            else:
                print("El alumno llegó tarde, se cuenta como falta.")
                print("Horario esperado:", horario_esperado)
                print("Horario actual:", self.hora_entrada)
                llegada_tarde="Si"
            print("Asistencia registrada.")
        else:
            messagebox.showerror("Error", "No se encontraron resultados para el legajo proporcionado.")
        

        fecha = datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute("Insert into asistencias(Num_legajo,Fecha,Hora_Entrada,Horario_llegada,Llegada_tarde) values (%s,%s,%s,%s,%s)",(num_legajo,fecha,horario_esperado,self.hora_entrada,llegada_tarde))
        self.cnx.commit()
        
        self.cursor.execute("SELECT id_asistencia FROM asistencias ORDER BY id_asistencia DESC")
        id_asistencia = self.cursor.fetchone()[0]  # Obtiene solo el valor del ID
        self.cursor.execute("SELECT Nombre_y_apellido, DNI FROM alumnos WHERE N_Legajo = %s", (num_legajo,))
        alumno_info = self.cursor.fetchone()
        self.tree.insert("", "end", values=(id_asistencia, num_legajo, alumno_info[0], resultado[1], resultado[2], alumno_info[1], fecha, horario_esperado, self.hora_entrada, llegada_tarde))
        if self.cursor.with_rows:  
            self.cursor.fetchall() 
        self.cursor.reset()
        self.cerrar_base_de_datos()
        messagebox.showinfo("Asistencia registrada", "La asistencia fue registrada exitosamente.")
        self.ventana_asis.focus()
    def ingresar_treeview(self):
        self.scrollbar = Scrollbar(self.frame_treeview)
        self.scrollbar.pack(side="right", fill="y")

        self.tree = ttk.Treeview(self.frame_treeview, yscrollcommand=self.scrollbar.set)
        self.tree.pack(fill="both", expand=True)
        self.tree["columns"] = ("id_asistencia","Num_legajo","Nombre y apellido","Curso", "Division","DNI", "Fecha", "Hora_Entrada", "Horario_llegada", "Llegada_tarde")
        self.scrollbar.config(command=self.tree.yview)
        self.tree.column("#0", width=0, stretch=0)
        self.tree.column("id_asistencia", anchor="center", width=50)
        self.tree.column("Num_legajo", anchor="center", width=50)
        self.tree.column("Nombre y apellido", anchor="center", width=100)
        self.tree.column("Curso", anchor="center", width=50)
        self.tree.column("Division", anchor="center", width=50)
        self.tree.column("DNI", anchor="center", width=50)
        self.tree.column("Fecha", anchor="center", width=50)
        self.tree.column("Hora_Entrada", anchor="center", width=50)
        self.tree.column("Horario_llegada", anchor="center", width=50)
        self.tree.column("Llegada_tarde", anchor="center", width=50)
        
        self.tree.heading("#0", text="", anchor="center")
        self.tree.heading("id_asistencia", text="id_asistencia", anchor="center")
        self.tree.heading("Num_legajo", text="Num_legajo", anchor="center")
        self.tree.heading("Nombre y apellido", text="Nombre y apellido", anchor="center")
        self.tree.heading("Curso", text="Curso", anchor="center")
        self.tree.heading("Division", text="Division", anchor="center")
        self.tree.heading("DNI", text="DNI", anchor="center")
        self.tree.heading("Fecha", text="Fecha", anchor="center")
        self.tree.heading("Hora_Entrada", text="Hora_Entrada", anchor="center")
        self.tree.heading("Horario_llegada", text="Horario_llegada", anchor="center")
        self.tree.heading("Llegada_tarde", text="Llegada_tarde", anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        self.conectar_base_de_datos()
        self.cursor.execute("""SELECT 
                        asis.id_asistencia,
                        a.N_Legajo,
                        a.Nombre_y_apellido,
                        a.Curso,
                        a.Division,
                        a.DNI,
                        asis.Fecha,
                        asis.Hora_Entrada,
                        asis.horario_llegada,
                        asis.Llegada_tarde
                        from asistencias asis
                        JOIN
                        alumnos a ON a.N_Legajo = asis.Num_legajo""")
        self.registros = self.cursor.fetchall()

        for registro in self.registros:
            self.tree.insert("", "end", values=registro)
        
        self.cerrar_base_de_datos()
        
    def on_key_press(self, event):
        if not self.procesando:  # Solo si no está procesando un código
            if event.keysym == 'Return':  # Si se presiona 'Enter'
                print(f'Código escaneado: {self.scanned_code}')
                self.procesando = True  # Marcar que está procesando el código
                self.procesar_codigo()  # Llamar la función de procesamiento
                self.scanned_code = ""  # Reiniciar el código escaneado
            else:
                self.scanned_code += event.char  # Agregar el carácter ingresado al código
    def volver(self):
        self.eliminar()
        from Pestaña_qr import clase_qr
        clase_qr(self.ventana_asis,self.menuFunc,self.tipocuenta,self.nombrecuenta)
        
    def eliminar(self):
        for elemento in self.ventana_asis.winfo_children():
            elemento.destroy()
    def procesar_codigo(self):
        dia_actual = datetime.today().date()  # Obtener la fecha de hoy correctamente
        dia_semana = dia_actual.weekday() + 1  # weekday() devuelve 0 = lunes, ajusta sumando 1
        hora_actual = datetime.now().time() 

        # Comparar si la hora actual está dentro del rango especificado
        if time(7, 40) <= hora_actual <= time(12, 5):
            turno = "mañana"
        elif time(12, 5) < hora_actual < time(17, 30):
            turno = "tarde"
        elif time(17, 30) <= hora_actual <= time(21, 50):
            turno = "vespertino"
        else:
            turno = "FR"

        print(f'Turno: {turno}' + f' - ' + f'Día: {dia_semana}')
        
        # Simular el proceso de búsqueda de alumno
        self.buscar_alumno(self.scanned_code,dia_semana, turno)
        
        # Reiniciar la flag después de un tiempo
        self.ventana_asis.after(1000, self.resetear_procesamiento)
        
    def resetear_procesamiento(self):
        self.procesando = False
    def conectar_base_de_datos(self):
        self.cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
            )
        # Crear un cursor para ejecutar consultas
        self.cursor = self.cnx.cursor(buffered=True)
    def cerrar_base_de_datos(self):
        self.cursor.close()
        self.cnx.close()

if __name__ == "__main__":
    tk=Tk()
    tk.geometry("500x500")
    tk.title("Ingresar Asistencias")
    app = Ingresar_Asistencias_qr(tk,None,None,None)
    tk.mainloop()