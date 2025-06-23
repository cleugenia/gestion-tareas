document.addEventListener('DOMContentLoaded', () => {

  const formRegister = document.getElementById('form-register');
  const formLogin = document.getElementById('form-login');
  const formTarea = document.getElementById('form-tarea');
  const listaTareas = document.getElementById('lista-tareas');
  const tareasSection = document.getElementById('tareas-section');
  const loginSection = document.getElementById('login');
  const registerSection = document.getElementById('register');
  const usuarioNombre = document.getElementById('usuario-nombre');
  const btnLogout = document.getElementById('btn-logout');

  const API_URL = 'http://localhost:5000';
   

  // REGISTRO
  formRegister.addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuario = document.getElementById('register-usuario').value;
    const contrasena = document.getElementById('register-contrasena').value;

    const res = await fetch(`${API_URL}/registro`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario, contrasena })
    });

    const data = await res.json();
    alert(data.mensaje || data.error);
  });

  // LOGIN
  formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();
    const usuario = document.getElementById('login-usuario').value;
    const contrasena = document.getElementById('login-contrasena').value;

    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario, contrasena })
    });

    const data = await res.json();

  
    if (data.token) {
        localStorage.setItem('token', data.token);
        localStorage.setItem('usuario', usuario);  // <--- guardamos nombre real aquí
        usuarioNombre.textContent = usuario;
        mostrarSeccionTareas();
        cargarTareas();
    } else {
        alert(data.error);
    }

});
  // AGREGAR TAREA
  formTarea.addEventListener('submit', async (e) => {
    e.preventDefault();
    const descripcion = document.getElementById('descripcion-tarea').value;
    const token = localStorage.getItem('token');

    const res = await fetch(`${API_URL}/tareas`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token
      },
      body: JSON.stringify({ descripcion })
    });

    const data = await res.json();
    alert(data.mensaje || data.error);
    cargarTareas();
    e.target.reset();
  });

  // LISTAR TAREAS
  async function cargarTareas() {
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_URL}/tareas/listar`, {
      headers: { 'Authorization': token }
    });

    if (!res.ok) {
      alert('Error cargando tareas, por favor logueate nuevamente.');
      logout();
      return;
    }

    const tareas = await res.json();
    listaTareas.innerHTML = '';

    tareas.forEach(t => {
      const li = document.createElement('li');
      li.className = 'list-group-item d-flex justify-content-between align-items-center';
      li.innerHTML = `
        <span>${t.descripcion} ${t.completada ? '✅' : ''}</span>
        <div>
          <button class="btn btn-sm btn-danger me-2" onclick="eliminarTarea(${t.id})">🗑️</button>
          ${!t.completada ? `<button class="btn btn-sm btn-success" onclick="marcarCompletada(${t.id})">✔️</button>` : ''}
        </div>
      `;
      listaTareas.appendChild(li);
    });
  }

  // Mostrar la sección de tareas y ocultar login y registro
  function mostrarSeccionTareas() {
    tareasSection.classList.remove('d-none');
    loginSection.classList.add('d-none');
    registerSection.classList.add('d-none');
  }

  // Cerrar sesión
  btnLogout.addEventListener('click', () => {
    logout();
  });

  function logout() {
    localStorage.removeItem('token');
    location.reload();
  }

  // Comprobar si hay token guardado
  if (localStorage.getItem('token')) {
    const usuarioGuardado = localStorage.getItem('usuario');
    usuarioNombre.textContent = usuarioGuardado || 'Usuario';
    mostrarSeccionTareas();
    cargarTareas();
  }

  // Exponer funciones globales para que los botones inline puedan usarlas
  window.eliminarTarea = async function (id) {
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_URL}/tareas/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': token }
    });
    const data = await res.json();
    alert(data.mensaje || data.error);
    cargarTareas();
  };

  window.marcarCompletada = async function (id) {
    const token = localStorage.getItem('token');
    const res = await fetch(`${API_URL}/tareas/${id}/completar`, {
      method: 'PATCH',
      headers: { 'Authorization': token }
    });
    const data = await res.json();
    alert(data.mensaje || data.error);
    cargarTareas();
  };

});

