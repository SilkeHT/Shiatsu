(() => {
  const zonas = {
    cabeza: {
      titulo: "Cabeza y cuello",
      ayuda: "Reduce el estrés",
      texto: "Para cuando la mente va acelerada, cuesta dormir o la nuca se queda rígida de tanto mirar pantallas. La presión suave en la base del cráneo y a lo largo del cuello ayuda a soltar y a respirar más despacio.",
      valor: "cabeza y cuello",
    },
    hombros: {
      titulo: "Hombros",
      ayuda: "Proporciona bienestar",
      texto: "Es donde se queda la carga del día. Trabajar los hombros y la zona entre los omóplatos alivia la sensación de peso y devuelve movilidad a los brazos.",
      valor: "hombros",
    },
    espalda: {
      titulo: "Espalda alta",
      ayuda: "Devuelve el equilibrio",
      texto: "A ambos lados de la columna recorre el meridiano de la vejiga, que en el shiatsu se relaciona con todo el cuerpo. Por eso la espalda es el centro de casi todas las sesiones.",
      valor: "espalda alta",
    },
    lumbar: {
      titulo: "Zona lumbar",
      ayuda: "Ayuda a la recuperación",
      texto: "Para quien pasa muchas horas sentado o de pie. La presión mantenida y los estiramientos suaves relajan la parte baja de la espalda y la pelvis.",
      valor: "zona lumbar",
    },
    brazos: {
      titulo: "Brazos y manos",
      ayuda: "Renueva tu energía",
      texto: "Tensión de teclado, de ratón o de trabajo manual. Los meridianos de los brazos terminan en las manos, y trabajarlos deja una sensación de ligereza.",
      valor: "brazos y manos",
    },
    piernas: {
      titulo: "Piernas y pies",
      ayuda: "Mejora la circulación",
      texto: "Para piernas cansadas o pesadas. El trabajo en piernas y pies favorece la circulación y te ayuda a sentirte con los pies en la tierra.",
      valor: "piernas y pies",
    },
  };

  const svgZonas = document.querySelectorAll(".figure .zone");
  const botones = document.querySelectorAll(".zone-list button");
  const info = document.querySelector(".zone-info");
  const form = document.getElementById("form-cita");

  function mostrarZona(clave, { mover = false } = {}) {
    const z = zonas[clave];
    if (!z) return;
    svgZonas.forEach((g) => g.classList.toggle("is-active", g.dataset.zone === clave));
    botones.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.zone === clave)));

    const marcada = form.querySelector(`input[name="zona"][value="${z.valor}"]`)?.checked;
    info.innerHTML = `
      <div class="zone-card">
        <h3>${z.titulo}</h3>
        <p class="ayuda">${z.ayuda}</p>
        <p>${z.texto}</p>
        <button type="button" class="btn btn-ghost zone-add" data-valor="${z.valor}">
          ${marcada ? "Añadida a tu cita" : "Añadir a mi cita"}
        </button>
      </div>`;
    if (mover && window.matchMedia("(max-width: 760px)").matches) {
      info.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }

  botones.forEach((b) => b.addEventListener("click", () => mostrarZona(b.dataset.zone)));
  svgZonas.forEach((g) => g.addEventListener("click", () => mostrarZona(g.dataset.zone, { mover: true })));

  info.addEventListener("click", (e) => {
    const btn = e.target.closest(".zone-add");
    if (!btn) return;
    const casilla = form.querySelector(`input[name="zona"][value="${btn.dataset.valor}"]`);
    if (casilla) {
      casilla.checked = true;
      actualizarMensaje();
    }
    btn.textContent = "Añadida a tu cita";
  });

  // Mensaje de cita
  const preview = document.getElementById("preview");
  const wa = document.getElementById("enviar-wa");
  const mail = document.getElementById("enviar-mail");

  function lista(items) {
    if (items.length <= 1) return items.join("");
    return items.slice(0, -1).join(", ") + " y " + items[items.length - 1];
  }

  function actualizarMensaje() {
    const datos = new FormData(form);
    const nombre = (datos.get("nombre") || "").trim();
    const zonasMarcadas = datos.getAll("zona");
    const horario = datos.get("horario") || "cuando haya hueco";
    const nota = (datos.get("nota") || "").trim();

    let texto = nombre ? `Hola Raquel, soy ${nombre}.` : "Hola Raquel.";
    texto += " Me gustaría reservar una sesión de shiatsu";
    texto += horario === "cuando haya hueco" ? ", cuando tengas hueco." : ` ${horario}.`;
    if (zonasMarcadas.length) texto += `\nMe gustaría trabajar ${lista(zonasMarcadas)}.`;
    if (nota) texto += `\n${nota}`;

    preview.textContent = texto;
    wa.href = `https://wa.me/34696663229?text=${encodeURIComponent(texto)}`;
    mail.href = `mailto:tushiatsu@gmail.com?subject=${encodeURIComponent("Cita de shiatsu")}&body=${encodeURIComponent(texto)}`;
  }

  form.addEventListener("input", actualizarMensaje);
  form.addEventListener("submit", (e) => e.preventDefault());
  actualizarMensaje();
})();
