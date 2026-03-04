document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[href^="http"]').forEach(function (link) {
    if (!link.hostname.includes(window.location.hostname)) {
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');
    }
  });
});

// Initialize pan/zoom on Mermaid diagrams after they render.
// mkdocs-mermaid2 triggers rendering asynchronously, so we use a
// MutationObserver to detect when each .mermaid container receives
// its SVG child, then attach panzoom.
document.addEventListener('DOMContentLoaded', function () {
  var containers = document.querySelectorAll('.mermaid');
  if (!containers.length) return;

  containers.forEach(function (container) {
    var observer = new MutationObserver(function (mutations, obs) {
      var svg = container.querySelector('svg');
      if (!svg) return;

      obs.disconnect();

      // Remove fixed width/height so the SVG fills its container.
      svg.removeAttribute('width');
      svg.removeAttribute('height');
      svg.style.width = '100%';
      svg.style.height = 'auto';

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
});
