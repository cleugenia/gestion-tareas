# 📝 Gestor de Tareas 

Este proyecto consiste en una aplicación web para gestionar tareas, con funcionalidades de:

- Registro de usuarios
- Inicio de sesión con autenticación
- Gestión de tareas (crear, listar, eliminar, completar)
- Cliente web (frontend con HTML/JS)
- Cliente por consola para interacción directa con la API

---

## 🔧 Tecnologías utilizadas

### Backend
- Python 3
- Flask
- Flask-CORS
- SQLite3
- Werkzeug (para hash de contraseñas)

### Frontend
- HTML, CSS, JavaScript
- Bootstrap 5
- GitHub Pages (para alojamiento del frontend)

---

## 📁 Estructura del repositorio

```
/
├── servidor.py          # Código fuente del backend (API REST)
├── cliente.py           # Cliente por consola 
├── tareas.db            # Base de datos SQLite (se genera automáticamente)
├── frontend/
│   ├── index.html       # Interfaz de usuario
│   ├── script.js        # Lógica de interacción con la API
│   ├── style.css        # Estilos personalizados
├── capturas/            # Capturas de pantalla 
├── README.md            # Este archivo
```

---

## 🚀 Instrucciones para ejecutar el proyecto

### 1. Cloná el repositorio

```bash
git clone https://github.com/cleugenia/gestion-tareas.git
cd gestion-tareas
```

### 2. Instalá las dependencias necesarias

Asegurate de tener Python 3 y pip. Luego ejecutá:

```bash
pip install flask flask-cors werkzeug
```

### 3. Ejecutá el backend (Flask API)

```bash
python servidor.py
```

Esto levantará el servidor en:  
`http://localhost:5000`

---

## 💻 Cliente por Consola

Podés interactuar directamente con la API mediante el archivo cliente.py, sin necesidad de usar navegador web.

```bash
python cliente.py
```

Este cliente por consola permite:

    - Registro de usuario

    - Login y almacenamiento del token

    - Crear tareas

    - Listar tareas

    - Marcar como completadas

    - Eliminar tareas

    Ideal para probar los endpoints REST sin depender del frontend gráfico.

## 🌐 Cliente web (frontend)

El proyecto incluye también una interfaz gráfica en HTML ubicada en la carpeta /frontend.

## 🔁 Formas de uso del proyecto

### 🖥️ Opción 1: Todo local

    Frontend: se abre localmente (index.html desde la carpeta /frontend)

    Backend: se ejecuta con python servidor.py en http://localhost:5000

✅ Ideal para desarrollo o pruebas sin conexión.

### 🌐 Opción 2: Frontend en GitHub Pages + Backend local

    Frontend: alojado en GitHub Pages
    https://cleugenia.github.io/gestion-tareas/
    
    Backend: debe estar corriendo en la máquina local (localhost:5000)

⚠️ Esta opción solo funciona desde la misma máquina donde se está ejecutando el backend. GitHub Pages no puede acceder a localhost en otra computadora.


---


## 🖼️ Capturas de pantalla

> Se encuentran en la carpeta `capturas/` del repositorio.  
Algunas imágenes de ejemplo:

- Registro exitoso  
- Login exitoso  
- Vista de tareas con tareas agregadas  
- Tarea completada y eliminada  

---


    
## ✅ Funcionalidades implementadas

### API REST (Flask)
- `POST /registro` → Registro de usuarios (con contraseñas hasheadas)
- `POST /login` → Inicio de sesión y generación de token
- `GET /tareas` → Página de bienvenida si está autenticado
- `POST /tareas` → Crear nueva tarea
- `GET /tareas/listar` → Listar tareas del usuario
- `DELETE /tareas/<id>` → Eliminar tarea
- `PATCH /tareas/<id>/completar` → Marcar tarea como completada

---

## 🔐 Seguridad
- Las contraseñas se almacenan **hasheadas** con `generate_password_hash`.
- La autenticación se realiza mediante un **token simple** enviado en el header `Authorization`.

---

## ✍️ Autora
Esta app fue realizada por **M. Eugenia Descalzo** 
