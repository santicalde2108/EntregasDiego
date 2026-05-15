const inputRojo  = document.getElementById("rojo");
      const inputVerde = document.getElementById("verde");
      const inputAzul  = document.getElementById("azul");
 
      const textoRojo  = document.getElementById("texto-rojo");
      const textoVerde = document.getElementById("texto-verde");
      const textoAzul  = document.getElementById("texto-azul");
      const contenedor = document.querySelector(".contenedor-interno");
      const labels = document.querySelectorAll("label");
 
      const actualizarColor = () => {
        const r = inputRojo.value;
        const g = inputVerde.value;
        const b = inputAzul.value;
        const esTodoBlanco = r === "255" && g === "255" && b === "255";
 
        textoRojo.textContent  = r;
        textoVerde.textContent = g;
        textoAzul.textContent  = b;
 
        document.body.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        contenedor.classList.toggle("dark", esTodoBlanco);
        labels.forEach((label) => label.classList.toggle("dark-text", esTodoBlanco));
        textoRojo.classList.toggle("dark-text", esTodoBlanco);
        textoVerde.classList.toggle("dark-text", esTodoBlanco);
        textoAzul.classList.toggle("dark-text", esTodoBlanco);
      };
 
      inputRojo.addEventListener("input",  actualizarColor);
      inputVerde.addEventListener("input", actualizarColor);
      inputAzul.addEventListener("input",  actualizarColor);
 
      actualizarColor();