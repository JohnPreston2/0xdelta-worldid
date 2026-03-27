  const WORLD_APP_ID   = "app_411ec21928d81bebe5be96beefdf732d";
  const WORLD_ACTION   = "access-0xdelta-dashboard";
  const VERIFY_API_URL = "http://34.14.53.149:5050/api/verify-human";
  const SESS_KEY = "0xdelta_human_verified";

  // Charge IDKit et résout quand window.IDKit est dispo
  const idkitReady = new Promise((resolve, reject) => {
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/@worldcoin/idkit-standalone@2.1.2/build/index.global.js';
    s.onload = () => {
      if (window.IDKit) resolve(window.IDKit);
      else reject(new Error('IDKit not found after load'));
    };
    s.onerror = () => reject(new Error('IDKit script failed to load'));
    document.head.appendChild(s);
  });

  function getSession() {
    try { const d = JSON.parse(sessionStorage.getItem(SESS_KEY)); if (!d || Date.now() > d.exp) return null; return d; } catch { return null; }
  }
  function setSession(nullifier, level) {
    sessionStorage.setItem(SESS_KEY, JSON.stringify({ nullifier, level, exp: Date.now() + 24 * 3600 * 1000 }));
  }
  function showVerified(level) {
    document.getElementById("unverified-state").style.display = "none";
    document.getElementById("verified-state").style.display  = "block";
    const labels = { orb: "World ID · Orb Level · Full Access", device: "World ID · Device Level" };
    document.getElementById("verify-level-text").textContent = labels[level] || "World ID Verified";
  }
  function toast(msg, err) {
    const t = document.getElementById("toast");
    t.textContent = msg; t.className = "toast" + (err ? " err" : "") + " show";
    setTimeout(() => t.classList.remove("show"), 4000);
  }

  async function openWorldID() {
    toast("Loading World ID...");
    let IDKit;
    try {
      IDKit = await idkitReady;
    } catch(e) {
      toast("World ID unavailable — opening World App...");
      window.open(`https://worldcoin.org/verify?app_id=${WORLD_APP_ID}&action=${WORLD_ACTION}&return_to=${encodeURIComponent(location.href)}`, "_blank");
      return;
    }
    try {
      IDKit.init({
        app_id:             WORLD_APP_ID,
        action:             WORLD_ACTION,
        verification_level: "orb",
        onSuccess:          onWorldIDSuccess,
        handleVerify:       onWorldIDVerify,
        onError:            e => toast("World ID error: " + (e?.message || e), true)
      });
      IDKit.open();
    } catch(e) { toast("IDKit error: " + e, true); }
  }

  async function onWorldIDVerify(proof) {
    const res  = await fetch(VERIFY_API_URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(proof) });
    const data = await res.json();
    if (!data.success) throw new Error(data.error || "Verification failed");
    setSession(data.nullifier_hash, data.verification_level || "orb");
  }

  function onWorldIDSuccess() {
    const s = getSession();
    showVerified(s?.level || "orb");
    toast("✅ Human verified — full access unlocked!");
  }

  document.addEventListener("DOMContentLoaded", () => { const s = getSession(); if (s) showVerified(s.level); });
