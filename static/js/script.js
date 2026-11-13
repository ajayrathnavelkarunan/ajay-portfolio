(() => {
  const $ = (s, c = document) => c.querySelector(s), $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  $("#yr").textContent = new Date().getFullYear();
  $("#menu").onclick = e => e.currentTarget.setAttribute("aria-expanded", $("#links").classList.toggle("open"));
  $$("a[href^='/']:not([download])").forEach(a => a.addEventListener("click", e => { if (e.metaKey || e.ctrlKey || e.shiftKey || reduce) return; e.preventDefault(); document.body.classList.add("leaving"); setTimeout(() => location.href = a.href, 200); }));
  addEventListener("pageshow", () => document.body.classList.remove("leaving"));
  $$("#links a").forEach(a => a.onclick = () => $("#links").classList.remove("open"));

  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } }), { threshold: .12 });
  $$(".reveal").forEach(el => io.observe(el));

  const t = $("#typed"), words = t ? JSON.parse(t.dataset.words) : []; let w = 0, c = t ? words[0].length : 0, del = true;
  if (t && !reduce) (function tick() {
    c += del ? -1 : 1; t.textContent = words[w].slice(0, c); let d = del ? 40 : 80;
    if (del && c === 0) { del = false; w = (w + 1) % words.length; d = 300; }
    else if (!del && c === words[w].length) { del = true; d = 1800; }
    setTimeout(tick, d);
  })();

  if (!reduce && matchMedia("(hover:hover)").matches) $$(".tilt").forEach(el => {
    el.addEventListener("mousemove", e => { const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5; el.style.transform = `perspective(800px) rotateX(${-y * 6}deg) rotateY(${x * 6}deg) translateY(-4px)`; });
    el.addEventListener("mouseleave", () => el.style.transform = "");
  });

  const cv = $("#bg"), cx = cv.getContext("2d"); let W, H, P = [], run = !reduce;
  const size = () => { W = cv.width = innerWidth; H = cv.height = innerHeight; P = Array.from({ length: Math.min(55, W / 25 | 0) }, () => ({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .3, vy: (Math.random() - .5) * .3 })); };
  size(); addEventListener("resize", size); document.addEventListener("visibilitychange", () => { run = !document.hidden && !reduce; if (run) draw(); });
  function draw() {
    if (!run) return; cx.clearRect(0, 0, W, H);
    P.forEach((p, i) => {
      p.x = (p.x + p.vx + W) % W; p.y = (p.y + p.vy + H) % H;
      cx.fillStyle = "rgba(54,214,231,.7)"; cx.fillRect(p.x, p.y, 2, 2);
      for (let j = i + 1; j < P.length; j++) { const q = P[j], d = Math.hypot(p.x - q.x, p.y - q.y); if (d < 130) { cx.strokeStyle = `rgba(167,139,250,${.18 * (1 - d / 130)})`; cx.beginPath(); cx.moveTo(p.x, p.y); cx.lineTo(q.x, q.y); cx.stroke(); } }
    });
    requestAnimationFrame(draw);
  }
  draw();

  const f = $("#form"), st = $("#status");
  if (f) f.addEventListener("submit", async e => {
    e.preventDefault(); $$(".err").forEach(x => x.textContent = ""); st.className = ""; st.textContent = "Sending...";
    try {
      const r = await fetch("/contact", { method: "POST", body: new FormData(f) }), d = await r.json();
      if (d.ok) { st.className = "ok"; st.textContent = d.message; f.reset(); return; }
      Object.entries(d.errors || {}).forEach(([k, v]) => { const el = $(`.err[data-for="${k}"]`); if (el) el.textContent = v; });
      st.className = "bad"; st.textContent = d.errors && d.errors.form ? d.errors.form : "Please fix the highlighted fields.";
    } catch { st.className = "bad"; st.textContent = "Network error. Please try again."; }
  });
})();
