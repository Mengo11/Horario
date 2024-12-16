from fpdf import FPDF
import mysql.connector
import os,webbrowser
from win10toast import ToastNotifier
from tkinter import Tk, filedialog
from datetime import timedelta

#Hecho por Valentino signorello
class PDF(FPDF):
    def __init__(self, tipo_de_aula, numero_de_aula):
        super().__init__(orientation='L', unit='mm', format='A3')
        self.tipo_de_aula = tipo_de_aula
        self.numero_de_aula = numero_de_aula
        self.add_page()
        self.tabla() 

       
    def header(self):
        url="https://eestn1tfeb.blogspot.com"
        self.set_font("Times", "B", 25)
        self.cell(395, 15, "Escuela Técnica N°1: Manuel Belgrano", border=1,align="C", ln=True,link=url)
        self.ln(5)

       
    def tabla(self):
        try:
            # Conexión a la base de datos
            self.cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
            )
            self.cursor = self.cnx.cursor()
            self.cursor.execute("""SELECT * FROM horarios WHERE Numero_aula=%s AND tipo_de_aula=%s ORDER BY Horario_e""",
                                (self.numero_de_aula, self.tipo_de_aula))
            self.VALORES = self.cursor.fetchall()

            self.dias_a_numeros = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
            horarios_por_dia = {dia: [] for dia in self.dias_a_numeros.keys()}
            print(horarios_por_dia)
            for valor in self.VALORES:
                dia_numero = valor[10]
                dia_texto = list(self.dias_a_numeros.keys())[dia_numero - 1]
                horarios_por_dia[dia_texto].append(valor)

        except mysql.connector.Error as err:
            print("Error al conectarse a MySQL: {}".format(err))
            self.cursor.close()
            self.cnx.close()
            return

    
        # Encabezados
        self.set_fill_color(81, 112, 238)  
        self.cell(395,10, "Horarios", border=1,align='C',fill=1,ln=1)
        #cambiar fuente a la normal
        self.set_font("Arial", size=10)
        #y color
        self.set_fill_color(12, 171, 196)
        self.cell(30, 10, "Dia", border=1, align='C', fill=1)
        self.cell(35, 10, "Numero de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Tipo de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario entrada", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario salida", border=1, align='C', fill=1)
        self.cell(85, 10, "Espacio curricular", border=1, align='C', fill=1)
        self.cell(15, 10, "Año", border=1, align='C', fill=1)
        self.cell(15, 10, "Division", border=1, align='C', fill=1)
        self.cell(15, 10, "Grupo", border=1, align='C', fill=1)
        self.cell(80, 10, "Profesor", border=1, align='C', fill=1)
        self.ln()

        self.set_fill_color(220, 220, 220)
        dia_antes=None
        fila_nueva=True
        self.c = 0 
       
        

        for dia, horarios in horarios_por_dia.items():
         if horarios:
            if dia == dia_antes:
                  self.cell(25,10, "",border=1,align='C',fill=0)

            else:
                fila_nueva=True
                self.cell(30,10 * len(horarios) ,str(dia),border=1,align='C',fill=0)
                dia_antes = dia

            
            
            for valor in horarios:
                
                if not fila_nueva:
                 self.cell(30, 10, "", border=0, align='C', fill=0)
                else:
                 fila_nueva = False  

                hora_entrada = str(valor[3] // timedelta(hours=1)).zfill(2) + ":" + str((valor[3] % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2)
                hora_salida = str(valor[4] // timedelta(hours=1)).zfill(2) + ":" + str((valor[4] % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2)
               

                self.cell(35, 10, str(valor[1]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[2]), border=1, align='C', fill=1)
                self.cell(40, 10, str(hora_entrada), border=1, align='C', fill=1)
                self.cell(40, 10, str(hora_salida), border=1, align='C', fill=1)
                self.cell(85, 10, str(valor[5]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[6]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[7]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[8]), border=1, align='C', fill=1)
                self.cell(80, 10, str(valor[9]), border=1, align='C', fill=1)
                self.ln()
                if self.c % 2 == 0:
                        self.set_fill_color(255, 255, 255)  
                else:
                        self.set_fill_color(220, 220, 220)  

                self.c += 1 
                 
    def guardar_pdf(self):
        nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula}.pdf"
        ruta_descargas = os.path.expanduser("~/Downloads")

        # Generar un nombre de archivo único si ya existe
        contador = 1
        ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
        while os.path.exists(ruta_pdf_descargas):
            nombre_archivo = f"Horario {self.tipo_de_aula} {self.numero_de_aula} ({contador}).pdf"
            ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
            contador += 1

        self.output(ruta_pdf_descargas)
        os.startfile(ruta_pdf_descargas)
        

class PDF_filtro(FPDF):
    def __init__(self, query):
        super().__init__(orientation='L', unit='mm', format='A3')
        self.query = query
        self.add_page()
        self.tabla()
    
    def header(self):
        url="https://eestn1tfeb.blogspot.com"
        self.set_font("Times", "B", 25)
        self.cell(395, 15, "Escuela Técnica N°1: Manuel Belgrano", border=1,align="C", ln=True,link=url)
        self.ln(5)
        self.set_fill_color(81, 112, 238)  
        self.cell(395,10, "Horarios", border=1,align='C',fill=1,ln=1)
        #cambiar fuente a la normal
        self.set_font("Arial", size=10)
        #y color
        self.set_fill_color(12, 171, 196)
        self.cell(30, 10, "Dia", border=1, align='C', fill=1)
        self.cell(35, 10, "Numero de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Tipo de aula", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario entrada", border=1, align='C', fill=1)
        self.cell(40, 10, "Horario salida", border=1, align='C', fill=1)
        self.cell(85, 10, "Espacio curricular", border=1, align='C', fill=1)
        self.cell(15, 10, "Año", border=1, align='C', fill=1)
        self.cell(15, 10, "Division", border=1, align='C', fill=1)
        self.cell(15, 10, "Grupo", border=1, align='C', fill=1)
        self.cell(80, 10, "Profesor", border=1, align='C', fill=1)
        self.ln()
         
    def tabla(self):
        try:
            # Conexión a la base de datos
            self.cnx = mysql.connector.connect(
                host='eestn1.com.ar',
                user='tecnica1',
                password='z%51#q57A7BR',
                database='tec_boletines2023',
                port=3306
            )
            self.cursor = self.cnx.cursor()
            self.cursor.execute(self.query)
            self.VALORES = self.cursor.fetchall()

            self.dias_a_numeros = {"Lunes": 1, "Martes": 2, "Miercoles": 3, "Jueves": 4, "Viernes": 5}
            horarios_por_dia = {dia: [] for dia in self.dias_a_numeros.keys()}
            print(horarios_por_dia)
            for valor in self.VALORES:
                dia_numero = valor[10]
                dia_texto = list(self.dias_a_numeros.keys())[dia_numero - 1]
                horarios_por_dia[dia_texto].append(valor)

        except mysql.connector.Error as err:
            print("Error al conectarse a MySQL: {}".format(err))
            self.cursor.close()
            self.cnx.close()
            return

        # Encabezados
        

        self.set_fill_color(220, 220, 220)
        dia_antes=None
        fila_nueva=True
        self.c = 0 
       
        

        for dia, horarios in horarios_por_dia.items():
         if horarios:
            if dia == dia_antes:
                  self.cell(25,10, "",border=1,align='C',fill=0)

            else:
                fila_nueva=True
                self.cell(30,10 * len(horarios) ,str(dia),border=1,align='C',fill=0)
                dia_antes = dia

            
            
            for valor in horarios:
                
                if not fila_nueva:
                 self.cell(30, 10, "", border=0, align='C', fill=0)
                else:
                 fila_nueva = False  

                hora_entrada = str(valor[3] // timedelta(hours=1)).zfill(2) + ":" + str((valor[3] % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2)
                hora_salida = str(valor[4] // timedelta(hours=1)).zfill(2) + ":" + str((valor[4] % timedelta(hours=1)) // timedelta(minutes=1)).zfill(2)
               

                self.cell(35, 10, str(valor[1]), border=1, align='C', fill=1)
                self.cell(40, 10, str(valor[2]), border=1, align='C', fill=1)
                self.cell(40, 10, str(hora_entrada), border=1, align='C', fill=1)
                self.cell(40, 10, str(hora_salida), border=1, align='C', fill=1)
                self.cell(85, 10, str(valor[5]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[6]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[7]), border=1, align='C', fill=1)
                self.cell(15, 10, str(valor[8]), border=1, align='C', fill=1)
                self.cell(80, 10, str(valor[9]), border=1, align='C', fill=1)
                self.ln()
                if self.c % 2 == 0:
                        self.set_fill_color(255, 255, 255)  
                else:
                        self.set_fill_color(220, 220, 220)  

                self.c += 1 
                
    def guardar_pdf(self, nombre_archivo):
     ruta_descargas = os.path.expanduser("~/Downloads")

    # Generar un nombre de archivo único si ya existe
     contador = 1
     ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
     while os.path.exists(ruta_pdf_descargas):
        nombre_archivo = f"{os.path.splitext(nombre_archivo)[0]} ({contador}).pdf"
        ruta_pdf_descargas = os.path.join(ruta_descargas, nombre_archivo)
        contador += 1

     self.output(ruta_pdf_descargas)
     os.startfile(ruta_pdf_descargas)
class PDF_alumnos(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(3, 10, 10)  # Márgenes izquierdo, superior y derecho
        self.pagina_padre = False
        self.obtener_datos()

    def header(self):
        self.set_font("Times", "B", 15)
        if not self.pagina_padre:
            # Encabezado para la página de estudiantes
            self.cell(200, 7, 'REGISTRO DE MATRÍCULA', border=1, align="C", ln=1)
            self.set_font("Times", "B", 10)
            self.cell(40, 5, 'CICLO: 2024', border=1, align="L")
            self.cell(130, 5, 'DISTRITO ESCOLAR: 117', border=1, align="C")
            self.cell(30, 5, 'CURSO: 2° A', border=1, align="R", ln=1)
        else:
            # Encabezado para la página de padres/tutores
            self.cell(205, 7, 'ADULTOS RESPONSABLES', border=1, align="C", ln=1)
            self.set_font("Times", "B", 10)
            self.cell(40, 5, 'CICLO: 2024', border=1, align="L")
            self.cell(130, 5, 'Escuela Técnica N°1: Manuel Belgrano', border=1, align="C")
            self.cell(35, 5, 'CURSO: 2° A', border=1, align="R", ln=1)
        
        self.ln(5)
        self.set_font("Times", "B", 10)
        self.ln(9)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def obtener_datos(self):
     try:
        self.cnx = mysql.connector.connect(
            host='eestn1.com.ar',
            user='tecnica1',
            password='z%51#q57A7BR',
            database='tec_boletines2023',
            port=3306
        )
        self.cursor = self.cnx.cursor()  
        self.cursor.execute("""SELECT * FROM alumnos ORDER BY N_legajo""")
        self.VALORES = self.cursor.fetchall()

        # Agrega una línea para imprimir los datos obtenidos (solo para depuración)
        print("Datos obtenidos:", self.VALORES)

     except mysql.connector.Error as err:
        print("Error al conectarse a MySQL: {}".format(err))
        self.VALORES = []
     finally:
        if self.cursor:
            self.cursor.close()
        if self.cnx:
            self.cnx.close()



        # Encabezado de tabla
    def add_student_page(self):
        self.pagina_padre = False
        alumnos_por_pagina = 32  # Máximo de alumnos por página
        contador_alumnos = 0

        # Encabezado de tabla
        def agregar_encabezado():
            self.cell(10, 12, 'N°', 1, 0, 'C')
            x = self.get_x()
            y = self.get_y()
            self.multi_cell(20, 6, 'Fecha de admisión', border=1, align='C')
            self.set_xy(x + 20, y)

            x = self.get_x()
            y = self.get_y()
            self.multi_cell(20, 6, 'N° de Legajo', border=1, align='C')
            self.set_xy(x + 20, y)

            self.cell(20, 12, 'Procedencia', border=1, align='C')
            self.cell(40, 12, 'Nombre y Apellido', border=1, align='C')
            self.cell(20, 12, 'DNI', border=1, align='C')

            x = self.get_x()
            y = self.get_y()
            self.multi_cell(25, 6, 'Fecha de nacimiento', border=1, align='C')
            self.set_xy(x + 25, y)
        
            self.cell(15, 12, 'Edad', border=1, align='C')
            self.cell(25, 12, 'Nacionalidad', border=1, align='C')
            self.cell(5, 12, '', border=1, align="C")
            self.ln()

        self.add_page()  
        agregar_encabezado()

        numero_fila = 1  

        for valor in self.VALORES:
            if contador_alumnos == alumnos_por_pagina:
                self.agregar_padre()  # Añadir página de padres/tutores
                self.add_page()  # Añadir nueva página de alumnos
                agregar_encabezado()
                contador_alumnos = 0

            self.set_font('Arial', '', 10)
            self.cell(10, 6, str(numero_fila), border=1, align='C')  # N°
            self.cell(20, 6, str(valor[0]), border=1, align='C')  # Fecha de admisión
            self.cell(20, 6, str(valor[1]), border=1, align='C')  # N° de Legajo
            self.cell(20, 6, str(valor[2]), border=1, align='C')  # Procedencia
            self.cell(40, 6, str(valor[3]), border=1, align='C')  # Nombre y Apellido
            self.cell(20, 6, str(valor[4]), border=1, align='C')  # DNI
            self.cell(25, 6, str(valor[5]), border=1, align='C')  # Fecha de nacimiento
            self.cell(15, 6, str(valor[6]), border=1, align='C')  # Edad
            self.cell(25, 6, str(valor[7]), border=1, align='C')  # Nacionalidad
            self.cell(5, 6, '', border=1, align='C')
            self.ln()

            contador_alumnos += 1
            numero_fila += 1

        for _ in range(3):
            self.set_font('Arial', '', 10)
            self.cell(10, 6, str(numero_fila), border=1, align='C')  # N° (Numerado)
            self.cell(20, 6, '', border=1, align='C')  # Fecha de admisión
            self.cell(20, 6, '', border=1, align='C')  # N° de Legajo
            self.cell(20, 6, '', border=1, align='C')  # Procedencia
            self.cell(40, 6, '', border=1, align='C')  # Nombre y Apellido
            self.cell(20, 6, '', border=1, align='C')  # DNI
            self.cell(25, 6, '', border=1, align='C')  # Fecha de nacimiento
            self.cell(15, 6, '', border=1, align='C')  # Edad
            self.cell(25, 6, '', border=1, align='C')  # Nacionalidad
            self.cell(5, 6, '', border=1, align='C')
            self.ln()
            numero_fila += 1

    def agregar_padre(self):
        self.pagina_padre = True  
        self.add_page()  
        
        self.set_font('Times', 'B', 10)

        self.cell(10, 12, 'N°', 1, 0, 'C')
        self.cell(40, 12, 'Nombre del Tutor', border=1, align='C')
        self.cell(30, 12, 'DNI Tutor', border=1, align='C')
        x = self.get_x()
        y = self.get_y()
        self.multi_cell(25, 6, 'Nacionalidad Tutor', border=1, align='C')
        self.set_xy(x + 25, y)

        self.cell(50, 12, 'Domicilio Tutor', border=1, align='C')
        self.cell(40, 12, 'Teléfono Tutor', border=1, align='C')
        self.cell(10, 12, 'Pase', border=1, align='C')
        self.ln()
        numero_fila = 1  # Contador de número de filas

        for valor in self.VALORES:
            self.set_font('Arial', '', 10)
            self.cell(10, 6, str(numero_fila), border=1, align='C')  # N°
            self.cell(40, 6, str(valor[10]), border=1, align='C')  # Nombre del Tutor
            self.cell(30, 6, str(valor[11]), border=1, align='C')  # DNI Tutor
            self.cell(25, 6, str(valor[12]), border=1, align='C')  # Nacionalidad Tutor
            self.cell(50, 6, str(valor[13]), border=1, align='C')  # Domicilio Tutor
            self.cell(40, 6, str(valor[14]), border=1, align='C')  # Teléfono Tutor
            self.cell(10, 6, '', border=1, align='C')
            self.ln()
            numero_fila += 1

        for _ in range(3):
            self.set_font('Arial', '', 10)
            self.cell(10, 6, str(numero_fila), border=1, align='C')  # N° (Numerado)
            self.cell(40, 6, '', border=1, align='C')  # nombre
            self.cell(30, 6, '', border=1, align='C')  # dni
            self.cell(25, 6, '', border=1, align='C')  # nacio
            self.cell(50, 6, '', border=1, align='C')  # tele
            self.cell(40, 6, '', border=1, align='C')  # domi
            self.cell(10, 6, '', border=1, align='C')  # 
          
            self.ln()
            numero_fila += 1
            self.obtener_datos
    def guardar_archivo(self, nombre_archivo):
        carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        ruta_completa = os.path.join(carpeta_descargas, nombre_archivo)    
        self.output(ruta_completa)
        webbrowser.open(f'file://{ruta_completa}')
        os.startfile(ruta_completa)
    
if __name__ == '__main__':
    app = PDF("Laboratorio", 10)
    app.guardar_pdf()