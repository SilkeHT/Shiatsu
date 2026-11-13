(() => {
  const form = document.getElementById("form-cita");

  // Mensaje de cita
  const preview = document.getElementById("preview");
  const wa = document.getElementById("enviar-wa");
  const mail = document.getElementById("enviar-mail");

  function actualizarMensaje() {
    const datos = new FormData(form);
    const nombre = (datos.get("nombre") || "").trim();
    const horario = datos.get("horario") || "cuando haya hueco";
    const nota = (datos.get("nota") || "").trim();

    let texto = nombre ? `Hola, Raquel. Soy ${nombre}.` : "Hola, Raquel.";
    texto += " Me gustaría reservar una sesión de shiatsu";
    texto += horario === "cuando haya hueco" ? ", cuando tengas disponibilidad." : ` ${horario}.`;
    if (nota) texto += `\n${nota}`;

    preview.textContent = texto;
    wa.href = `https://wa.me/34696663229?text=${encodeURIComponent(texto)}`;
    mail.href = `mailto:tushiatsu@gmail.com?subject=${encodeURIComponent("Cita de shiatsu")}&body=${encodeURIComponent(texto)}`;
  }

  form.addEventListener("input", actualizarMensaje);
  form.addEventListener("submit", (e) => e.preventDefault());
  actualizarMensaje();
})();
