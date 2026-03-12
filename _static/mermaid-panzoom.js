(() => {
  function attachPanZoom(svg) {
    if (!svg || svg.dataset.panzoomAttached === "true") {
      return;
    }

    const container = svg.closest(".mermaid-container-fullscreen");
    if (!container) {
      return;
    }

    svg.dataset.panzoomAttached = "true";

    // Keep panning predictable inside fullscreen modal.
    container.style.overflow = "hidden";
    container.style.touchAction = "none";

    let scale = 1;
    let tx = 0;
    let ty = 0;
    let dragging = false;
    let dragOffsetX = 0;
    let dragOffsetY = 0;

    const minScale = 0.25;
    const maxScale = 6;

    const applyTransform = () => {
      svg.style.transformOrigin = "0 0";
      svg.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
    };

    const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

    applyTransform();
    svg.style.cursor = "grab";

    svg.addEventListener(
      "wheel",
      (event) => {
        event.preventDefault();

        const rect = container.getBoundingClientRect();
        const cx = event.clientX - rect.left;
        const cy = event.clientY - rect.top;

        const factor = event.deltaY < 0 ? 1.12 : 0.88;
        const nextScale = clamp(scale * factor, minScale, maxScale);

        // Zoom around cursor position.
        tx = cx - ((cx - tx) * nextScale) / scale;
        ty = cy - ((cy - ty) * nextScale) / scale;
        scale = nextScale;

        applyTransform();
      },
      { passive: false }
    );

    svg.addEventListener("pointerdown", (event) => {
      if (event.button !== 0) {
        return;
      }
      dragging = true;
      dragOffsetX = event.clientX - tx;
      dragOffsetY = event.clientY - ty;
      svg.style.cursor = "grabbing";
      if (svg.setPointerCapture) {
        svg.setPointerCapture(event.pointerId);
      }
      event.preventDefault();
    });

    svg.addEventListener("pointermove", (event) => {
      if (!dragging) {
        return;
      }
      tx = event.clientX - dragOffsetX;
      ty = event.clientY - dragOffsetY;
      applyTransform();
    });

    const stopDragging = (event) => {
      if (!dragging) {
        return;
      }
      dragging = false;
      svg.style.cursor = "grab";
      if (event && svg.releasePointerCapture) {
        try {
          svg.releasePointerCapture(event.pointerId);
        } catch {
          // No-op: pointer may already be released.
        }
      }
    };

    svg.addEventListener("pointerup", stopDragging);
    svg.addEventListener("pointercancel", stopDragging);
    svg.addEventListener("pointerleave", stopDragging);

    // Double-click to reset view.
    svg.addEventListener("dblclick", (event) => {
      event.preventDefault();
      scale = 1;
      tx = 0;
      ty = 0;
      applyTransform();
    });
  }

  function initFullscreenPanZoom() {
    const installForActiveModal = () => {
      document
        .querySelectorAll(".mermaid-fullscreen-modal.active .mermaid svg")
        .forEach(attachPanZoom);
    };

    const observer = new MutationObserver(() => {
      installForActiveModal();
    });

    observer.observe(document.body, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["class"],
    });

    document.addEventListener("click", (event) => {
      if (!event.target.closest(".mermaid-fullscreen-btn")) {
        return;
      }
      // Wait for extension script to clone and insert the SVG into modal.
      requestAnimationFrame(() => {
        requestAnimationFrame(installForActiveModal);
      });
    });

    installForActiveModal();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initFullscreenPanZoom);
  } else {
    initFullscreenPanZoom();
  }
})();
