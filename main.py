import requests
import hashlib

class Usuario:
    def __init__(self, id_usuario, correo, password):
        self.__id_usuario = id_usuario
        self.__correo = correo
        self.__password_hash = hashlib.sha256(password.encode()).hexdigest()

    def login(self, correo, password):
        hash_intento = hashlib.sha256(password.encode()).hexdigest()
        if self.__correo == correo and self.__password_hash == hash_intento:
            return True
        return False

class Empleado(Usuario):
    def __init__(self, id_usuario, correo, password, nombre, rut, salario):
        super().__init__(id_usuario, correo, password)
        self.__nombre = nombre
        self.__rut = rut
        self.__salario = salario
        self.__departamento = None
        self.__registros = []

    def asignar_departamento(self, departamento):
        self.__departamento = departamento

    def registrar_horas(self, fecha, horas, tarea):
        nuevo_registro = RegistroTiempo(fecha, horas, tarea)
        self.__registros.append(nuevo_registro)

    def mostrar_info(self):
        if self.__departamento != None:
            depto_nombre = self.__departamento.get_nombre()
        else:
            depto_nombre = "Sin asignar"
        print(f"Empleado: {self.__nombre} | RUT: {self.__rut} | Depto: {depto_nombre}")

class Departamento:
    def __init__(self, id_depto, nombre):
        self.__id_depto = id_depto
        self.__nombre = nombre

    def get_nombre(self):
        return self.__nombre

class RegistroTiempo:
    def __init__(self, fecha, horas, tarea):
        self.__fecha = fecha
        self.__horas = horas
        self.__tarea = tarea

class ServicioExterno:
    def __init__(self):
        self.__url_base = "https://mindicador.cl/api"

    def sanear_entrada(self, entrada):
        permitidos = "abcdefghijklmnopqrstuvwxyz"
        salida = ""
        for letra in entrada.lower():
            if letra in permitidos:
                salida += letra
        return salida

    def obtener_indicador(self, tipo):
        tipo_limpio = self.sanear_entrada(tipo)
        if tipo_limpio == "":
            return None
        
        url = f"{self.__url_base}/{tipo_limpio}"
        respuesta = requests.get(url)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            valor = datos['serie'][0]['valor']
            fecha = datos['serie'][0]['fecha'][0:10]
            nombre = datos['nombre']
            return valor, fecha, nombre
        return None

def main():
    empleado_admin = Empleado("EMP01", "martin@ecotech.cl", "inacap123", "Martin Osorio", "19XXX", 850000)
    depto_tecnologia = Departamento("D01", "Desarrollo TI")
    empleado_admin.asignar_departamento(depto_tecnologia)
    
    autenticado = False
    
    while True:
        print("\n--- SISTEMA ECOTECH SOLUTIONS ---")
        print("1. Iniciar Sesion")
        print("2. Salir")
        opcion = input("Seleccione opcion: ")
        
        if opcion == "1":
            correo = input("Ingrese su correo: ")
            password = input("Ingrese su password: ")
            
            if empleado_admin.login(correo, password):
                autenticado = True
                print("\nAcceso concedido.")
                break
            else:
                print("\nCredenciales incorrectas.")
        elif opcion == "2":
            return
        else:
            print("\nOpcion no valida.")

    while autenticado:
        print("\n--- MENU PRINCIPAL ECOTECH ---")
        print("1. Ver informacion de empleado")
        print("2. Registrar horas de trabajo en proyecto")
        print("3. Consultar indicador economico (API Externa)")
        print("4. Cerrar Sesion")
        
        opcion_menu = input("Seleccione opcion: ")
        
        if opcion_menu == "1":
            empleado_admin.mostrar_info()
        
        elif opcion_menu == "2":
            fecha = input("Ingrese fecha (DD-MM-YYYY): ")
            horas = float(input("Ingrese cantidad de horas: "))
            tarea = input("Descripcion de la tarea: ")
            empleado_admin.registrar_horas(fecha, horas, tarea)
            print("Horas registradas mediante objetos. Problema de Excel solucionado.")
        
        elif opcion_menu == "3":
            api = ServicioExterno()
            indicador = input("Ingrese indicador (ejemplo: uf, dolar, euro): ")
            resultado = api.obtener_indicador(indicador)
            
            if resultado != None:
                valor, fecha, nombre = resultado
                print(f"\nDatos obtenidos de {nombre}:")
                print(f"Fecha: {fecha}")
                print(f"Valor: ${valor}")
            else:
                print("\nError al obtener el indicador. Verifique el nombre.")
                
        elif opcion_menu == "4":
            print("Cerrando sesion...")
            autenticado = False
        else:
            print("Opcion incorrecta.")

if __name__ == "__main__":
    main()