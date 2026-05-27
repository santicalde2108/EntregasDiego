function actualizarContador() {
    const tareas = document.querySelectorAll('.task-container');
    const completadas = document.querySelectorAll('.task-container input[type="checkbox"]:checked');
    const pendientes = tareas.length - completadas.length;
    document.getElementById('stats').textContent = `Tasks Completed: ${completadas.length} | Tasks Remaining: ${pendientes}`;
}

userInput.addEventListener('submit', (event) => {
    event.preventDefault();
    const inputTexto = document.querySelector('#userInput input[type="text"]');
    const textoTarea = inputTexto.value;

    const nuevaTarea = document.createElement('div');
    nuevaTarea.className = 'task-container';
    nuevaTarea.innerHTML = `
        <label>
            <input type="checkbox">
            ${textoTarea}
        </label>
        <img src="./imagenes/Delete.png" class="closeBtn" alt="Delete Task">
    `;

    document.getElementById('list-container').appendChild(nuevaTarea);
    inputTexto.value = '';
    actualizarContador();
});

document.getElementById('list-container').addEventListener('click', (event) => {
    if (event.target.classList.contains('closeBtn')) {
        event.target.parentElement.remove();
        actualizarContador();
    }
    if (event.target.type === 'checkbox') {
        actualizarContador();
    }
});

document.getElementById('clearAllBtn').addEventListener('click', () => {
    document.getElementById('list-container').innerHTML = '';
    actualizarContador();
});