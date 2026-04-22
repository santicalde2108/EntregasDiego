let contador = 0;


const boton = document.getElementById("btn");
const decrease = document.getElementById("decrease");
const reset = document.getElementById("reset");
const texto = document.getElementById("contador");

boton.addEventListener("click", aumentar);
decrease.addEventListener("click", disminuir);
reset.addEventListener("click", reiniciar);

function aumentar() {
    contador++;
    texto.textContent = contador;

    if (contador >= 10) {
        boton.classList.add("cambio-color");
    } else {
        boton.classList.remove("cambio-color");
    }

    if (contador >= 20) {
        boton.classList.add("girar");
    } else {
        boton.classList.remove("girar");
    }
}
function disminuir() {
    contador--;
    texto.textContent = contador;
    if (contador >= 10) {
        boton.classList.add("cambio-color");
    } else {
        boton.classList.remove("cambio-color");
    }
    if (contador >= 20) {
        boton.classList.add("girar");
    } else {
        boton.classList.remove("girar");
    }
}

function reiniciar() {
    contador = 0;
    texto.textContent = contador;

    boton.classList.remove("cambio-color");
    boton.classList.remove("girar");
}
