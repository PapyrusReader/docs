document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[href^="http"]').forEach(function (link) {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});

// Initialize pan/zoom on Mermaid diagrams after they render.
// Uses Material's document$ observable (fires on every page load including
// SPA navigation via navigation.instant) instead of DOMContentLoaded.
// mkdocs-mermaid2 triggers rendering asynchronously after each page load,
// so a MutationObserver detects SVG insertion and attaches panzoom.
function initMermaidPanzoom() {
  if (typeof panzoom === 'undefined') return;

  var containers = document.querySelectorAll('.mermaid');
  if (!containers.length) return;

  containers.forEach(function (container) {
    // Skip containers that already have panzoom attached.
    if (container.dataset.panzoomReady) return;
    container.dataset.panzoomReady = '1';

    var observer = new MutationObserver(function (mutations, obs) {
      var svg = container.querySelector('svg');
      if (!svg) return;

      obs.disconnect();

      // Remove fixed dimensions so the SVG fills its container.
      svg.removeAttribute('width');
      svg.removeAttribute('height');
      svg.style.width = '100%';
      svg.style.height = 'auto';
      container.style.height = '';

      var instance = panzoom(svg, {
        contain: 'outside',
        maxZoom: 10,
        minZoom: 0.3,
      });

      // Double-click resets zoom and pan.
      svg.addEventListener('dblclick', function () {
        instance.reset();
      });
    });

    observer.observe(container, { childList: true, subtree: true });
  });
}

// document$ is Material's RxJS observable — fires on initial load and on
// every SPA navigation (navigation.instant). Fall back to DOMContentLoaded
// for environments where document$ is not present.
if (typeof document$ !== 'undefined') {
  document$.subscribe(initMermaidPanzoom);
} else {
  document.addEventListener('DOMContentLoaded', initMermaidPanzoom);
}
