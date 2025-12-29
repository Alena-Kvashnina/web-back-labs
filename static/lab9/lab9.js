// static/lab9/lab9.js

async function postJSON(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return await res.json();
}

function setBoxEmpty(btn) {
  btn.classList.add("is-empty");
  btn.disabled = true;
  const lbl = btn.querySelector(".box-empty-label");
  if (lbl) lbl.hidden = false;
}

function openModal(text, giftSrc) {
  const modal = document.getElementById("modal");
  document.getElementById("modalText").textContent = text || "";

  const img = document.getElementById("modalGift");
  if (giftSrc) {
    img.src = "/static/" + giftSrc;
    img.style.display = "block";
  } else {
    img.style.display = "none";
  }

  modal.hidden = false;
}

async function refreshStatus() {
  const data = await postJSON("/lab9/api/status", {});
  if (!data.ok) return;

  document.getElementById("remaining").textContent = data.remaining;
  document.getElementById("openedCount").textContent = data.openedCount;

  const opened = new Set(data.openedGlobal || []);
  document.querySelectorAll(".box").forEach((btn) => {
    const id = Number(btn.dataset.id);
    if (opened.has(id)) setBoxEmpty(btn);
  });
}

// из-за defer можно запускать сразу
refreshStatus();

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const modal = document.getElementById("modal");
    if (modal && !modal.hidden) modal.hidden = true;
  }
});

document.querySelectorAll(".box").forEach((btn) => {
  btn.addEventListener("click", async () => {
    const id = Number(btn.dataset.id);
    const data = await postJSON("/lab9/api/open", { id });

    if (!data.ok && data.limitReached) {
      openModal(data.message || "Можно открыть не больше 3 коробок 🙂", null);
      return;
    }
    if (!data.ok) {
      openModal(data.error || "Ошибка", null);
      return;
    }

    document.getElementById("remaining").textContent = data.remaining;
    document.getElementById("openedCount").textContent = data.openedCount;

    if (data.alreadyOpened) {
      setBoxEmpty(btn);
      return;
    }

    openModal(data.greeting, data.giftImage);
    setBoxEmpty(btn);
  });
});
