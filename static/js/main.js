// Theme toggle
function applyStoredTheme() {
  const stored = localStorage.getItem("theme");
  const html = document.documentElement;
  if (stored === "light") {
    html.setAttribute("data-theme", "light");
  } else {
    html.setAttribute("data-theme", "dark");
  }
}

applyStoredTheme();

document.addEventListener("DOMContentLoaded", () => {
  const html = document.documentElement;
  const modeToggle = document.getElementById("mode-toggle");
  const nav = document.getElementById("main-navbar");
  const navToggle = document.getElementById("nav-toggle");
  const navLinks = document.getElementById("nav-links");

  function getCsrfToken() {
    const name = "csrftoken=";
    const parts = document.cookie.split(";");
    for (let i = 0; i < parts.length; i += 1) {
      const c = parts[i].trim();
      if (c.startsWith(name)) return decodeURIComponent(c.substring(name.length));
    }
    return "";
  }

  function showToast(message) {
    const toast = document.getElementById("toast");
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add("visible");
    setTimeout(() => toast.classList.remove("visible"), 1800);
  }
  window.showToast = showToast;

  if (modeToggle) {
    modeToggle.addEventListener("click", () => {
      const current = html.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      html.setAttribute("data-theme", next);
      localStorage.setItem("theme", next);
    });
  }

  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      navLinks.classList.toggle("open");
    });
  }

  window.addEventListener("scroll", () => {
    if (!nav) return;
    const scrolled = window.scrollY > 10;
    nav.classList.toggle("scrolled", scrolled);

    // Show/hide back to top button
    const backToTopBtn = document.getElementById("back-to-top");
    if (backToTopBtn) {
      backToTopBtn.classList.toggle("show", window.scrollY > 300);
    }
  });

  // Back to top button
  const backToTopBtn = document.getElementById("back-to-top");
  if (!backToTopBtn) {
    const btn = document.createElement("button");
    btn.id = "back-to-top";
    btn.innerHTML = "↑";
    btn.title = "Back to top";
    document.body.appendChild(btn);
    btn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  if (window.gsap) {
    const tl = gsap.timeline();
    tl.from(".glass-nav", { y: -24, opacity: 0, duration: 0.5, ease: "power2.out" })
      .from(".hero-title", { y: 20, opacity: 0, duration: 0.5 }, "-=0.2")
      .from(".hero-subtitle", { y: 15, opacity: 0, duration: 0.4 }, "-=0.3")
      .from(".hero-actions .btn-primary", { scale: 0.9, opacity: 0, duration: 0.3 }, "-=0.2")
      .from(".stat-card", { y: 20, opacity: 0, stagger: 0.1, duration: 0.4 }, "-=0.1");

    // Soft entrance for cards
    if (window.gsap.utils) {
      gsap.utils.toArray(".vendor-card, .category-card, .dashboard-card").forEach((card, index) => {
        gsap.from(card, {
          y: 18,
          opacity: 0,
          duration: 0.35,
          ease: "power2.out",
          delay: 0.1 + index * 0.03,
        });
      });
    }
  }

  // Scroll trigger animations
  window.addEventListener("scroll", () => {
    document.querySelectorAll(".fade-in").forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.8) {
        el.style.opacity = "1";
      }
    });
  });

  // Hero typewriter
  const typeEl = document.querySelector(".hero-typewriter");
  if (typeEl) {
    const fullText = typeEl.getAttribute("data-text") || "";
    let idx = 0;
    function typeNext() {
      if (idx <= fullText.length) {
        typeEl.textContent = fullText.slice(0, idx);
        idx += 1;
        setTimeout(typeNext, 55);
      }
    }
    typeNext();
  }

  // Favourite button functionality
  document.querySelectorAll(".btn-favourite, .btn-favourite-big").forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const vendorId = this.dataset.vendorId;
      const csrfToken = getCsrfToken();

      fetch(`/vendors/${vendorId}/toggle-favourite/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/json"
        }
      })
        .then(r => r.json())
        .then(data => {
          if (data.success) {
            this.textContent = data.is_favourite ? "♥️ Favourite" : "♡ Favourite";
            this.style.color = data.is_favourite ? "#dc2626" : "inherit";
            showToast(data.is_favourite ? "Added to favourites!" : "Removed from favourites");
          }
        })
        .catch(e => console.error("Error:", e));
    });
  });

  // Hero particles
  const particlesHost = document.getElementById("hero-particles");
  if (particlesHost && window.gsap) {
    const total = 40;
    for (let i = 0; i < total; i += 1) {
      const dot = document.createElement("span");
      dot.className = "hero-particle";
      particlesHost.appendChild(dot);
      const startX = Math.random() * 100;
      const startY = Math.random() * 100;
      gsap.set(dot, {
        left: `${startX}%`,
        top: `${startY}%`,
        opacity: 0,
        scale: 0.4 + Math.random() * 0.6,
      });
      gsap.to(dot, {
        opacity: 0.9,
        duration: 1.2,
        delay: Math.random() * 1.5,
        yoyo: true,
        repeat: -1,
        x: `+=${(Math.random() - 0.5) * 60}`,
        y: `+=${(Math.random() - 0.5) * 40}`,
        ease: "sine.inOut",
      });
    }
  }

  // Counters
  document.querySelectorAll(".js-counter").forEach((el) => {
    const parent = el.closest("[data-count]") || el.parentElement;
    if (!parent) return;
    const target = parseInt(parent.dataset.count || "0", 10);
    let current = 0;
    const duration = 900;
    const start = performance.now();
    function tick(now) {
      const progress = Math.min(1, (now - start) / duration);
      current = Math.floor(target * progress);
      el.textContent = current.toLocaleString();
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });

  // Vendor list AJAX
  const vendorListContainer = document.getElementById("vendor-list-container");
  if (vendorListContainer) {
    const searchInput = document.getElementById("search-query");
    const categorySelect = document.getElementById("filter-category");
    const openToggle = document.getElementById("filter-open");
    const ratingSelect = document.getElementById("filter-rating");
    const viewToggle = document.querySelector(".view-toggle");
    const mapContainer = document.getElementById("vendor-map");
    let mapInstance = null;
    let markersLayer = null;

    function buildSkeleton(count) {
      vendorListContainer.innerHTML = "";
      for (let i = 0; i < count; i += 1) {
        const card = document.createElement("div");
        card.className = "skeleton-card";
        card.innerHTML = `
          <div class="skeleton-line" style="width:60%"></div>
          <div class="skeleton-line" style="width:40%"></div>
          <div class="skeleton-line" style="width:80%"></div>
        `;
        vendorListContainer.appendChild(card);
      }
    }

    function renderVendors(data) {
      vendorListContainer.innerHTML = "";
      if (!data.length) {
        vendorListContainer.innerHTML = '<p class="muted-text">No vendors match these filters yet.</p>';
        if (markersLayer) markersLayer.clearLayers();
        return;
      }
      data.forEach((vendor) => {
        const card = document.createElement("article");
        const isOpenNow = vendor.is_open_now;
        const verified = vendor.is_verified;
        card.className = "vendor-card";
        card.innerHTML = `
          <div class="vendor-card-header">
            <h3>${vendor.name}${verified ? " ✅" : ""}</h3>
            <span class="badge ${isOpenNow ? "badge-open" : "badge-closed"}">${isOpenNow ? "Open now" : "Closed"
          }</span>
          </div>
          <p class="vendor-card-address">${vendor.address || ""}</p>
          <p class="vendor-card-category">${vendor.category ? vendor.category.name : ""}</p>
          <p class="review-stars">${vendor.average_rating ? "★".repeat(Math.round(vendor.average_rating)) : ""}</p>
          <div class="share-buttons">
            <button type="button" class="icon-button heart-button" data-vendor-id="${vendor.id}" data-favourited="${vendor.is_favourite ? "1" : "0"}">❤</button>
            <a href="/vendors/${vendor.id}/detail/" class="btn-ghost small">View details</a>
          </div>
        `;
        vendorListContainer.appendChild(card);
      });

      if (mapContainer && window.L) {
        if (!mapInstance) {
          mapInstance = L.map("vendor-map").setView([20, 0], 2);
          L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 19,
            attribution: "&copy; OpenStreetMap",
          }).addTo(mapInstance);
        }
        if (markersLayer) {
          markersLayer.clearLayers();
        } else {
          markersLayer = L.layerGroup().addTo(mapInstance);
        }

        const bounds = [];
        data.forEach((vendor) => {
          if (vendor.latitude && vendor.longitude) {
            const lat = parseFloat(vendor.latitude);
            const lon = parseFloat(vendor.longitude);
            const marker = L.circleMarker([lat, lon], {
              radius: 8,
              color: "#6366f1",
              fillColor: "#6366f1",
              fillOpacity: 0.8,
            }).addTo(markersLayer);
            marker.bindPopup(`<strong>${vendor.name}</strong><br>${vendor.address || ""}`);
            bounds.push([lat, lon]);
          }
        });
        if (bounds.length) {
          mapInstance.fitBounds(bounds, { padding: [24, 24] });
        }
      }
    }

    async function fetchVendors() {
      buildSkeleton(4);
      const params = new URLSearchParams();
      if (searchInput && searchInput.value.trim()) params.set("q", searchInput.value.trim());
      if (categorySelect && categorySelect.value) params.set("category", categorySelect.value);
      if (openToggle && openToggle.dataset.active === "1") params.set("is_open", "1");
      if (ratingSelect && ratingSelect.value) params.set("min_rating", ratingSelect.value);
      try {
        const query = params.toString();
        const res = await fetch(`/vendors/api/search/${query ? `?${query}` : ""}`);
        const data = await res.json();
        renderVendors(data);
      } catch (e) {
        vendorListContainer.innerHTML = '<p class="muted-text">Unable to load vendors right now.</p>';
      }
    }

    if (searchInput) searchInput.addEventListener("input", () => fetchVendors());
    if (categorySelect) categorySelect.addEventListener("change", () => fetchVendors());
    if (ratingSelect) ratingSelect.addEventListener("change", () => fetchVendors());
    if (openToggle) {
      openToggle.addEventListener("click", () => {
        const active = openToggle.dataset.active === "1";
        openToggle.dataset.active = active ? "0" : "1";
        openToggle.classList.toggle("chip-toggle-active", !active);
        fetchVendors();
      });
    }
    if (viewToggle && mapContainer) {
      viewToggle.addEventListener("click", (e) => {
        const btn = e.target.closest("button");
        if (!btn) return;
        viewToggle.querySelectorAll("button").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        if (btn.dataset.view === "map") {
          mapContainer.parentElement.style.display = "block";
        } else {
          mapContainer.parentElement.style.display = "none";
        }
      });
    }

    fetchVendors();
    window.fetchVendors = fetchVendors;

    // Refresh open/closed based on backend every 60s
    setInterval(() => {
      fetchVendors();
    }, 60000);

    // Favourite toggles
    document.addEventListener("click", (e) => {
      const btn = e.target.closest(".heart-button");
      if (!btn) return;
      const vendorId = btn.dataset.vendorId;
      const isActive = btn.dataset.favourited === "1";
      fetch(`/vendors/${vendorId}/favourite/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((res) => {
          if (res.status === 403) {
            showToast("Log in to save vendors");
            return null;
          }
          return res.json();
        })
        .then((data) => {
          if (!data) return;
          const fav = !!data.is_favourite;
          btn.dataset.favourited = fav ? "1" : "0";
          btn.style.color = fav ? "#f97316" : "";
          showToast(fav ? "Added to favourites" : "Removed from favourites");
        })
        .catch(() => {
          showToast("Unable to update favourite");
        });
    });
  }

  // Lightbox
  const lightbox = document.getElementById("lightbox");
  if (lightbox) {
    const img = lightbox.querySelector("img");
    document.querySelectorAll("[data-lightbox-src]").forEach((thumb) => {
      thumb.addEventListener("click", () => {
        img.src = thumb.getAttribute("data-lightbox-src");
        lightbox.classList.add("open");
      });
    });
    lightbox.addEventListener("click", () => {
      lightbox.classList.remove("open");
    });
  }

  // Vendor wizard
  const wizard = document.querySelector(".wizard");
  if (wizard) {
    const panes = wizard.querySelectorAll(".wizard-step-pane");
    const steps = wizard.querySelectorAll(".wizard-step");
    const bar = wizard.querySelector(".wizard-progress-bar");
    const nextBtn = wizard.querySelector("[data-wizard-next]");
    const prevBtn = wizard.querySelector("[data-wizard-prev]");
    const stepCount = panes.length;
    let current = 0;

    function updateStep() {
      panes.forEach((p, i) => p.classList.toggle("active", i === current));
      steps.forEach((s, i) => s.classList.toggle("active", i === current));
      const pct = ((current + 1) / stepCount) * 100;
      if (bar) bar.style.width = `${pct}%`;
      if (prevBtn) prevBtn.disabled = current === 0;
      if (nextBtn) nextBtn.textContent = current === stepCount - 1 ? "Submit" : "Next";
    }

    updateStep();

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        if (current < stepCount - 1) {
          current += 1;
          updateStep();
        } else {
          wizard.closest("form")?.submit();
        }
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        if (current > 0) {
          current -= 1;
          updateStep();
        }
      });
    }
  }

  // QR code
  const qrContainer = document.getElementById("qr-code");
  if (qrContainer && window.QRCode) {
    const url = qrContainer.dataset.url;
    if (url) {
      new QRCode(qrContainer, {
        text: url,
        width: 120,
        height: 120,
        colorDark: "#e5e7eb",
        colorLight: "transparent",
        correctLevel: QRCode.CorrectLevel.H,
      });
    }
  }

  // Simple confetti on success
  const confettiFlag = document.getElementById("confetti-flag");
  if (confettiFlag && window.gsap) {
    const particles = [];
    const colors = ["#6366f1", "#f59e0b", "#22c55e", "#ec4899"];
    for (let i = 0; i < 60; i += 1) {
      const div = document.createElement("div");
      div.style.position = "fixed";
      div.style.width = "8px";
      div.style.height = "14px";
      div.style.borderRadius = "3px";
      div.style.backgroundColor = colors[i % colors.length];
      div.style.top = "-20px";
      div.style.left = `${Math.random() * 100}vw`;
      div.style.zIndex = "60";
      document.body.appendChild(div);
      particles.push(div);
    }
    particles.forEach((p) => {
      gsap.to(p, {
        y: window.innerHeight + 40,
        x: `+=${(Math.random() - 0.5) * 120}`,
        rotation: Math.random() * 360,
        duration: 2 + Math.random(),
        ease: "power2.out",
        onComplete: () => p.remove(),
      });
    });
  }

  // Voice search (Retell)
  const voiceBtn = document.getElementById("voice-search-button");
  if (voiceBtn && window.retellClientJsSdk) {
    const { RetellWebClient } = window.retellClientJsSdk;
    const webClient = new RetellWebClient();
    const searchInput = document.getElementById("search-query");
    let latestTranscript = "";

    webClient.on("update", (update) => {
      if (update && update.transcript) {
        latestTranscript = update.transcript;
      }
    });
    webClient.on("call_ended", () => {
      if (searchInput && latestTranscript) {
        searchInput.value = latestTranscript;
        if (typeof window.fetchVendors === "function") {
          window.fetchVendors();
        }
      }
    });

    voiceBtn.addEventListener("click", async () => {
      try {
        const body = {
          search_context: searchInput ? searchInput.value : "",
        };
        const res = await fetch("/ai/create-web-call/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify(body),
        });
        if (!res.ok) {
          showToast("Unable to start voice search");
          return;
        }
        const data = await res.json();
        await webClient.startCall({
          accessToken: data.access_token,
          sampleRate: 24000,
          emitRawAudioSamples: false,
        });
        showToast("Listening…");
      } catch (e) {
        showToast("Voice search failed");
      }
    });
  }
});

