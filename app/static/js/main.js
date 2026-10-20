// Animación 1: título que se escribe y se borra
const typed = document.getElementById("typed");
if (typed) {
  const words = typed.dataset.words.split(",");
  let w = 0, c = 0, del = false;
  (function tick() {
    const word = words[w];
    typed.textContent = "Aprende " + word.slice(0, c);
    c += del ? -1 : 1;
    let wait = del ? 40 : 90;
    if (!del && c > word.length) { del = true; wait = 1400; }
    else if (del && c < 0) { del = false; w = (w + 1) % words.length; c = 0; wait = 300; }
    setTimeout(tick, wait);
  })();
}

// Animación 2: contadores que suben al entrar en pantalla
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    const n = e.target, goal = +n.dataset.count, t0 = performance.now();
    (function step(t) {
      const p = Math.min((t - t0) / 1500, 1);
      n.textContent = Math.round(goal * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    })(t0);
    io.unobserve(n);
  });
}, { threshold: 0.6 });
document.querySelectorAll("[data-count]").forEach((n) => io.observe(n));

// Formulario: insertar (CTA) o editar -> servidor -> MySQL
const form = document.getElementById("form-lead");
if (form) {
  const msg = document.getElementById("msg");
  form.addEventListener("submit", async (ev) => {
    ev.preventDefault();
    msg.className = ""; msg.textContent = "Enviando…";
    try {
      const res = await fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      const data = await res.json();
      msg.className = data.ok ? "ok" : "err";
      msg.textContent = data.ok ? data.mensaje : data.error;
      if (data.ok && form.dataset.redirect) setTimeout(() => (location.href = form.dataset.redirect), 600);
      else if (data.ok) form.reset();
    } catch {
      msg.className = "err";
      msg.textContent = "Sin conexión. Revisa tu internet e intenta de nuevo.";
    }
  });
}

// Confirmación antes del borrado lógico
document.querySelectorAll("form[data-confirm]").forEach((f) =>
  f.addEventListener("submit", (e) => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));
