from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from PIL import ImageTk, Image

import sqlite3

class Registro():
    db_name = 'database_registro.db'

    def __init__(self, ventana):
        self.window = ventana
        self.window.title('Formulario de registro')
        self.window.geometry('390x450')
        self.window.resizable(0,0)
        self.window.config(bd=10)

        # -------------- titulo -----------
        titulo = Label(ventana, text='Registro de Usuario', fg="black", font=("Times New Roman", 13, "bold"), pady=5).pack()

        # -------------- Logo nuevo usuario
        imagen_registro = Image.open('./nuevo_usuario.png')
        nueva_imagen = imagen_registro.resize((40,40))
        render = ImageTk.PhotoImage(nueva_imagen)
        label_imagen = Label(ventana, image=render)
        label_imagen.image = render
        label_imagen.pack(pady=5)

        # -------------- Marco --------------
        marco = LabelFrame(ventana, text='Datos Personales', font=('Comic Sans', 10, 'bold'))
        marco.config(bd=2, pady=5)
        marco.pack()

        # ------------- Formulario -------------
        label_cedula = Label(marco, text='Cedula', font=("Comic Sans", 10,"bold")).grid(row=0, column=0, sticky='s', padx=5, pady=8)
        self.cedula = Entry(marco, width=25)
        self.cedula.focus()
        self.cedula.grid(row=0, column=1, padx=5, pady=8)

        label_nombres = Label(marco, text='Nombre', font=("Comic Sans", 10,"bold")).grid(row=1, column=0, sticky='s', padx=10, pady=8)
        self.nombres = Entry(marco, width=25)
        self.nombres.grid(row=1, column=1, padx=10, pady=8)

        label_apellido = Label(marco, text='Apellido', font=("Comic Sans", 10,"bold")).grid(row=2, column=0, sticky='s', padx=10, pady=8)
        self.apellido = Entry(marco, width=25)
        self.apellido.grid(row=2, column=1, padx=10, pady=8)

        label_sexo = Label(marco, text='Sexo', font=("Comic Sans", 10,"bold")).grid(row=3, column=0, sticky='s', padx=10, pady=8)
        self.combo_sexo = ttk.Combobox(marco, values=['Masculino', 'Femenino'], width=23, state='readonly')
        self.combo_sexo.current(0)
        self.combo_sexo.grid(row=3, column=1, padx=10, pady=8)

        label_edad = Label(marco, text='Edad', font=("Comic Sans", 10,"bold")).grid(row=4, column=0, sticky='s', padx=10, pady=8)
        self.edad = Entry(marco, width=25)
        self.edad.grid(row=4, column=1, padx=10, pady=8)

        label_correo = Label(marco, text='Correo electronico', font=("Comic Sans", 10,"bold")).grid(row=5, column=0, sticky='s', padx=10, pady=8)
        self.correo = Entry(marco, width=25)
        self.correo.grid(row=5, column=1, padx=10, pady=8)

        label_password = Label(marco, text='Contraseña', font=("Comic Sans", 10,"bold")).grid(row=6, column=0, sticky='s', padx=10, pady=8)
        self.password = Entry(marco, width=25)
        self.password.grid(row=6, column=1, padx=10, pady=8)

        label_password = Label(marco, text='Repetir contraseña', font=("Comic Sans", 10,"bold")).grid(row=7, column=0, sticky='s', padx=10, pady=8)
        self.repeater_password = Entry(marco, width=25)
        self.repeater_password.grid(row=7, column=1, padx=10, pady=8)

        # ---------- Frame botones ---------------
        frame_botones = Frame(ventana)
        frame_botones.pack()

        # --------- Botones -------------
        boton_registrar = Button(frame_botones, command=self.registrat_usuario , text='Registrar', height=2, width=10, bg='green', fg='white', font=("Comic Sans", 10,"bold")).grid(row=0, column=1, padx=10, pady=15)
        boton_limpiar = Button(frame_botones, command=self.limpiar_formularo, text='Limpiar', height=2, width=10, bg='gray',   fg='white', font=("Comic Sans", 10,"bold")).grid(row=0, column=2, padx=10, pady=15)
        boton_cancelar = Button(frame_botones, command=ventana.quit, text='Cerrar', height=2, width=10, bg='red',   fg='white', font=("Comic Sans", 10,"bold")).grid(row=0, column=3, padx=10, pady=15)

    def ejecutar_cosulta(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def limpiar_formularo(self):
        self.cedula.delete(0, END)
        self.nombres.delete(0, END)
        self.apellido.delete(0, END)
        self.combo_sexo.delete(0, END)
        self.edad.delete(0, END)
        self.correo.delete(0, END)
        self.password.delete(0, END)
        self.repeater_password.delete(0, END)

    def validar_formulario_completo(self):
        if len(self.cedula.get()) !=0 and len(self.nombres.get()) !=0 and len(self.apellido.get()) !=0 and len(self.combo_sexo.get()) !=0 and len(self.edad.get()) !=0 and len(self.password.get()) !=0 and len(self.repeater_password.get()) !=0 and len(self.correo.get()):
            return True
        else:
            messagebox.showerror('Error en registro', 'Complete todos los campos')
    
    def validar_password(self):
        if str(self.password.get()) == str(self.repeater_password.get()):
            return True
        else:
            messagebox.showerror('Error en registro', 'Contraseñas no coinciden')

    def buscar_cedula(self, cedula):
        with sqlite3.connect(self.db_name) as conexion:
            cursor = conexion.cursor()
            query = "SELECT * FROM registro where cedula = {}".format(cedula)
            cursor.execute(query)
            cedulax = cursor.fetchall() #repuesta como lista
            cursor.close()
            return cedulax
        
    def validar_cedula(self):
        cedula = self.cedula.get()
        dato = self.buscar_cedula(cedula)
        if dato == []:
            return True
        else:
            messagebox.showerror("ERROR EN REGISTRO", "CEDULA registrada anteriormente")

    def registrat_usuario(self):
        if self.validar_formulario_completo() and self.validar_password() and self.validar_cedula():
            query='INSERT INTO registro VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)'
            parameters = self.cedula.get(), self.nombres.get(), self.apellido.get(), self.combo_sexo.get(), self.correo.get(), self.password.get(), self.edad.get()
            self.ejecutar_cosulta(query, parameters)
            messagebox.showinfo("REGISTRO EXITOSO", f'Bienvenido {self.nombres.get()} {self.apellido.get()}')
            print("Usuario creado")
            self.limpiar_formularo()

if __name__ == '__main__':
    ventana = Tk()
    application = Registro(ventana)
    ventana.mainloop()