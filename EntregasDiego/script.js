function cambiarColor() {
      var color = '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');

      document.getElementById('caja').style.backgroundColor = color;
      document.body.style.backgroundColor = color;

      document.getElementById('etiqueta').textContent = color;
    }