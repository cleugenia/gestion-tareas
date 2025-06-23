import requests

API_URL = 'http://localhost:5000'

token = None
usuario = None

def registrar():
    usuario = input("Nuevo usuario: ")
    contrasena = input("Contraseña: ")
    res = requests.post(f"{API_URL}/registro", json={"usuario": usuario, "contrasena": contrasena})
    print(res.json().get("mensaje") or res.json().get("error"))

def login():
    global token, usuario
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    res = requests.post(f"{API_URL}/login", json={"usuario": usuario, "contrasena": contrasena})
    data = res.json()
    if 'token' in data:
        token = data['token']
        print(f"Inicio de sesión exitoso. ¡Bienvenido, {usuario}!")
    else:
        print(data.get("error"))

def listar_tareas():
    if not token:
        print("Primero debes iniciar sesión.")
        return
    res = requests.get(f"{API_URL}/tareas/listar", headers={"Authorization": token})
    if res.status_code != 200:
        print(res.json().get("error"))
        return
    tareas = res.json()
    if not tareas:
        print("No hay tareas.")
    for t in tareas:
        estado = "✅" if t['completada'] else "⏳"
        print(f"{t['id']}: {t['descripcion']} {estado}")

def agregar_tarea():
    if not token:
        print("Primero debes iniciar sesión.")
        return
    descripcion = input("Descripción de la nueva tarea: ")
    res = requests.post(f"{API_URL}/tareas", 
                        json={"descripcion": descripcion}, 
                        headers={"Authorization": token})
    print(res.json().get("mensaje") or res.json().get("error"))

def completar_tarea():
    if not token:
        print("Primero debes iniciar sesión.")
        return
    id_tarea = input("ID de la tarea a marcar como completada: ")
    res = requests.patch(f"{API_URL}/tareas/{id_tarea}/completar", 
                         headers={"Authorization": token})
    print(res.json().get("mensaje") or res.json().get("error"))

def eliminar_tarea():
    if not token:
        print("Primero debes iniciar sesión.")
        return
    id_tarea = input("ID de la tarea a eliminar: ")
    res = requests.delete(f"{API_URL}/tareas/{id_tarea}", 
                          headers={"Authorization": token})
    print(res.json().get("mensaje") or res.json().get("error"))

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Listar tareas")
        print("4. Agregar tarea")
        print("5. Marcar tarea como completada")
        print("6. Eliminar tarea")
        print("7. Salir")

        opcion = input("Elegí una opción: ")

        if opcion == '1':
            registrar()
        elif opcion == '2':
            login()
        elif opcion == '3':
            listar_tareas()
        elif opcion == '4':
            agregar_tarea()
        elif opcion == '5':
            completar_tarea()
        elif opcion == '6':
            eliminar_tarea()
        elif opcion == '7':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida")

if __name__ == '__main__':
    menu()
