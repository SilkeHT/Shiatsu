(() => {
  const zonas = {
    cabeza: {
      titulo: "Cabeza y cuello",
      ayuda: "Serena la mente",
      texto: "Cuando la mente no encuentra descanso, el sueño se vuelve ligero y la nuca se endurece. La presión serena en la base del cráneo invita a soltar y a recuperar una respiración lenta y profunda.",
      valor: "cabeza y cuello",
    },
    hombros: {
      titulo: "Hombros",
      ayuda: "Aporta bienestar",
      texto: "En los hombros se deposita el peso de los días. Al trabajar esta zona y el espacio entre los omóplatos, la carga se disuelve y los brazos recuperan su libertad.",
      valor: "hombros",
    },
    espalda: {
      titulo: "Espalda alta",
      ayuda: "Restablece el equilibrio",
      texto: "A ambos lados de la columna discurre el meridiano de la vejiga, que en la tradición del shiatsu se vincula con todo el cuerpo. Por ello, la espalda es el centro de casi todas las sesiones.",
      valor: "espalda alta",
    },
    lumbar: {
      titulo: "Zona lumbar",
      ayuda: "Favorece la recuperación",
      texto: "Para quien pasa largas horas sentado o de pie. La presión sostenida y los estiramientos suaves devuelven amplitud a la zona baja de la espalda y a la pelvis.",
      valor: "zona lumbar",
    },
    brazos: {
      titulo: "Brazos y manos",
      ayuda: "Renueva la energía",
      texto: "Los meridianos de los brazos culminan en las manos. Trabajarlos alivia la tensión de la labor diaria y deja una sensación de ligereza.",
      valor: "brazos y manos",
    },
    piernas: {
      titulo: "Piernas y pies",
      ayuda: "Activa la circulación",
      texto: "Para piernas cansadas o pesadas. El trabajo en piernas y pies activa la circulación y ayuda a sentirte de nuevo enraizado en la tierra.",
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
        <h3 class="caps">${z.titulo}</h3>
        <p class="ayuda">${z.ayuda}</p>
        <p>${z.texto}</p>
        <button type="button" class="btn btn-ghost zone-add" data-valor="${z.valor}">
          ${marcada ? "Incluida en tu cita" : "Incluir en mi cita"}
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
    btn.textContent = "Incluida en tu cita";
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

    let texto = nombre ? `Hola, Raquel. Soy ${nombre}.` : "Hola, Raquel.";
    texto += ` Me gustaría reservar ${datos.get("tipo") || "una sesión de shiatsu"}`;
    texto += horario === "cuando haya hueco" ? ", cuando tengas disponibilidad." : ` ${horario}.`;
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
