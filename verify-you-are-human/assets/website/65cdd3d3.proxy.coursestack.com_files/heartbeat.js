<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Challenge starting…</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  :root { --fg:#eaeef2; --bg:#0b1220; --accent:#5eead4; --muted:#94a3b8; }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100svh; display:grid; place-items:center; font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Inter,sans-serif; background:radial-gradient(1200px 800px at 50% 30%,#0f172a 0%,var(--bg) 60%); color:var(--fg); }
  .card { width:min(640px,92vw); padding:28px 24px; background:rgba(15,23,42,.6); border:1px solid rgba(148,163,184,.2); border-radius:16px; backdrop-filter: blur(6px); text-align:center; }
  h1 { margin:0 0 8px; font-size:1.5rem; font-weight:700; letter-spacing:.2px; }
  p { margin:6px 0; color:var(--muted); }
  .row { display:flex; gap:12px; align-items:center; justify-content:center; margin-top:14px;}
  .spinner {
    width:20px; height:20px; border:3px solid transparent; border-top-color:var(--accent);
    border-radius:50%; animation:spin .9s linear infinite;
  }
  @keyframes spin { to { transform:rotate(360deg); } }
  .hint { margin-top:14px; font-size:.95rem; }
  .mono { font-family: ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace; }
  .small { font-size:.85rem; color:#aab2c5; }
</style>
</head>
<body>
  <main class="card" role="main" aria-live="polite">
    <h1>The challenge is not ready yet! <br>Please wait a few more seconds...</h1>
    <div class="row">
      <div class="spinner" aria-hidden="true"></div>
      <p id="status"></p>
    </div>
    <p class="hint">This page should disappear within about a minute once the service finishes starting.</p>
    <p class="small">If you see this for more than a minute, please open a <span class="mono"><b>Technical Support</b></span> ticket in Discord.</p>
  </main>
<script>
  const messages = [
    "",
  ];
  let i = 0;
  setInterval(()=>{
    document.getElementById('status').textContent = messages[i++ % messages.length];
  }, 1200);
  setInterval(()=>{
    fetch(window.location.href, {cache: "no-store"})
      .then(resp => {
        if (resp.ok) {
          window.location.reload();
        }
      })
      .catch(()=>{});
  }, 5000);
</script>
</body>
</html>
