import * as brush from '../dist/brush.esm.js';

export const total = 5.0; // Total duration in seconds
const canvas = document.getElementById('stage');

// Initialize brush on the canvas
brush.load(canvas);
brush.scaleBrushes(2.5);

function easeOutCubic(x) {
  return 1 - Math.pow(1 - x, 3);
}

// Deterministic drawing function: pure function of time t
window.renderAt = function(t) {
  // Always seed deterministically for every frame
  brush.seed(42);
  brush.noiseSeed(42);
  
  // Clear with warm archival parchment color
  brush.clear("#faf6ee");
  
  const p = Math.min(Math.max(t / total, 0), 1);
  const strokeProgress = easeOutCubic(p);
  
  // 1. Soft watercolor wash in background
  brush.set("watercolor", "#dcd0ba", 3.0);
  brush.setBleed(0.4);
  brush.rect(200, 150, 1520, 780);
  
  // 2. Cross-hatched architectural frame
  if (t > 0.5) {
    const hatchP = Math.min((t - 0.5) / 2.0, 1);
    brush.hatch(14, 45, { rand: 0.15, continuous: true });
    brush.set("cpencil", "#4a453b", 1.2);
    brush.rect(240, 190, 1440 * hatchP, 700);
  }
  
  // 3. Central historical sketch lines (animated flow)
  brush.set("charcoal", "#1e1a17", 2.2);
  brush.setPressure(0.85);
  
  const endX = 300 + 1320 * strokeProgress;
  brush.line(300, 540, endX, 540);
  
  // Archival connecting nodes
  const nodeCount = 5;
  for (let i = 0; i < nodeCount; i++) {
    const nodeT = (i + 1) / (nodeCount + 1) * total;
    if (t >= nodeT) {
      const nx = 300 + (i + 1) * (1320 / (nodeCount + 1));
      const ny = 540 + Math.sin(i * 1.5) * 120;
      
      // Node circle
      brush.set("pen", "#d0312d", 1.8); // Ashu Dalal red accent
      brush.circle(nx, ny, 28);
      
      // Branch line
      brush.set("HB", "#332d28", 1.5);
      brush.line(nx, 540, nx, ny);
    }
  }
  
  // Crucial: flush the standalone canvas
  brush.render();
};

// Expose total length & ready flag
window.total = total;
window.__ready = true;

// Initial render for inspection
window.renderAt(2.5);
