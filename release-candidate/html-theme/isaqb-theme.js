(function () {
  const toc = document.getElementById("toc");
  if (!toc || typeof IntersectionObserver === "undefined") {
    return;
  }

  const linkFor = new Map();
  for (const link of toc.querySelectorAll('a[href^="#"]')) {
    const heading = document.getElementById(link.getAttribute("href").slice(1));
    if (heading) {
      linkFor.set(heading, link);
    }
  }
  if (linkFor.size === 0) {
    return;
  }

  let active = null;
  const observer = new IntersectionObserver(
    (entries) => {
      let top = null;
      for (const entry of entries) {
        if (
          entry.isIntersecting &&
          (top === null ||
            entry.boundingClientRect.top < top.boundingClientRect.top)
        ) {
          top = entry;
        }
      }
      if (!top || top.target === active) {
        return;
      }
      if (active) {
        linkFor.get(active).classList.remove("is-active");
      }
      linkFor.get(top.target).classList.add("is-active");
      active = top.target;
    },
    { rootMargin: "0px 0px -70% 0px", threshold: 0 },
  );

  for (const heading of linkFor.keys()) {
    observer.observe(heading);
  }
})();

(function () {
  const root = document.documentElement;
  const KEY = "isaqb-theme";

  let saved = null;
  try {
    saved = localStorage.getItem(KEY);
  } catch {
    /* storage blocked */
  }
  if (saved === "dark" || saved === "light") {
    root.setAttribute("data-theme", saved);
  }

  const prefersDark =
    window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  function effectiveTheme() {
    const attr = root.getAttribute("data-theme");
    if (attr === "dark" || attr === "light") {
      return attr;
    }
    return prefersDark && prefersDark.matches ? "dark" : "light";
  }

  /**
   * Themed images.
   *
   * An image opted in with the `theme-swap` role/class loads a "-dark" filename
   * variant in dark mode and the original in light mode:
   *
   *   images/logo.svg  <->  images/logo-dark.svg
   */
  const THEMED_IMAGE_SELECTOR = ".theme-swap img, img.theme-swap";

  function darkVariant(src) {
    return src.replace(/(\.[^./?#]+)([?#].*)?$/, "-dark$1$2");
  }

  function applyThemeToImages(theme) {
    for (const image of document.querySelectorAll(THEMED_IMAGE_SELECTOR)) {
      image.dataset.lightSrc ??= image.getAttribute("src");
      const nextSrc =
        theme === "dark"
          ? darkVariant(image.dataset.lightSrc)
          : image.dataset.lightSrc;
      if (image.getAttribute("src") !== nextSrc) {
        image.setAttribute("src", nextSrc);
      }
    }
  }

  const de = (navigator.language || "en").toLowerCase().indexOf("de") === 0;
  const labels = de
    ? {
        toLight: "Zum hellen Design wechseln",
        toDark: "Zum dunklen Design wechseln",
      }
    : { toLight: "Switch to light theme", toDark: "Switch to dark theme" };

  const btn = document.createElement("button");
  btn.id = "theme-toggle";
  btn.type = "button";

  function render() {
    const theme = effectiveTheme();
    const dark = theme === "dark";
    btn.textContent = dark ? "☀" : "☾";
    const label = dark ? labels.toLight : labels.toDark;
    btn.setAttribute("aria-label", label);
    btn.setAttribute("title", label);
    applyThemeToImages(theme);
  }

  btn.addEventListener("click", () => {
    const next = effectiveTheme() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem(KEY, next);
    } catch {
      /* storage blocked */
    }
    render();
  });

  render();
  prefersDark?.addEventListener("change", render);
  document.body.appendChild(btn);
})();
