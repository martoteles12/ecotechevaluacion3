import requests
import bcrypt
import re

class Usuario:
    def __init__(self, id_usuario, correo, password_plana):
        self.__id_usuario = id_usuario
        self.__correo = correo
        # Cifrado de contraseña al instanciar el objeto (3.1.2.I.5)
        self.__password_hash = self.__generar_hash(password_plana)

    def __generar_hash(self, password):
        """Genera un hash seguro utilizando bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def login(self, correo_intento, password_intento):
        """Valida las credenciales cifradas."""
        if self.__correo == correo_intento:
            if bcrypt.checkpw(password_intento.encode('utf-8'), self.__password_hash):
                print("\n[+] Autenticación exitosa. Acceso concedido a EcoTech Solutions.")
                return True
        print("\n[-] Error: Credenciales inválidas.")
        return False

class ServicioExterno:
    def __init__(self):
        self.__base_url = "https://mindicador.cl/api"

    def __sanear_entrada(self, entrada):
        """
        Valida y sanea la entrada del usuario usando expresiones regulares.
        Solo permite letras minúsculas (ej. 'uf', 'dolar', 'euro'). (3.1.2.I.6)
        """
        entrada_limpia = re.sub(r'[^a-z]', '', entrada.lower())
        return entrada_limpia

    def obtener_tipo_cambio(self, indicador):
        """
        Realiza la solicitud HTTP GET y procesa la respuesta JSON. (3.1.1.I.1 y 3.1.1.I.2)
        """
        indicador_saneado = self.__sanear_entrada(indicador)
        
        if not indicador_saneado:
            print("[-] Error: El indicador ingresado no es válido tras la sanitización.")
            return None

        url_completa = f"{self.__base_url}/{indicador_saneado}"
        
        try:
            # Solicitud HTTP funcional utilizando la librería requests
            respuesta = requests.get(url_completa, timeout=5)
            respuesta.raise_for_status() # Verifica si hay errores HTTP (404, 500, etc.)
            
            # Obtiene y procesa la respuesta en formato JSON
            datos = respuesta.json()
            valor_actual = datos['serie'][0]['valor']
            fecha = datos['serie'][0]['fecha'][:10]
            
            print(f"\n[+] Datos obtenidos de la API externa:")
            print(f"    Indicador: {datos['nombre']}")
            print(f"    Fecha: {fecha}")
            print(f"    Valor: ${valor_actual} CLP")
            return datos
            
        except requests.exceptions.HTTPError:
            print(f"[-] Error: No se encontró el indicador '{indicador_saneado}'.")
        except requests.exceptions.RequestException as e:
            print(f"[-] Error de conexión con el servicio externo: {e}")
        
        return None

# --- Flujo Principal de Ejecución ---
def main():
    print("=== Sistema de Gestión Interna EcoTech ===")
    
    # 1. Creación de un usuario de prueba (Simulando la base de datos)
    # Se aplica el encapsulamiento y cifrado automático definido en tu informe
    admin = Usuario(id_usuario="USR-001", correo="admin@ecotech.cl", password_plana="Segura123!")
    
    # 2. Proceso de Login Seguro
    print("\n--- Inicio de Sesión ---")
    correo_input = input("Ingrese correo corporativo: ")
    password_input = input("Ingrese contraseña: ")
    
    # Solo si el login es exitoso, se permite el acceso a las funciones externas
    if admin.login(correo_input, password_input):
        servicio = ServicioExterno()
        
        print("\n--- Consulta de Servicios Externos (Tipo de Cambio) ---")
        print("Opciones válidas: uf, dolar, euro, utm")
        # Entrada directa del usuario que será validada y saneada
        indicador_usuario = input("Ingrese el indicador económico a consultar: ")
        
        servicio.obtener_tipo_cambio(indicador_usuario)

if __name__ == "__main__":
    main()git add .