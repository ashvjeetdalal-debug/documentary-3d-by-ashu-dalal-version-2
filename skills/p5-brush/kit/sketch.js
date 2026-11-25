import * as brush from '/dist/brush.esm.js';

export const total = 5.0; // Total duration in seconds
const canvas = document.getElementById('stage');
const W = 1920;
const H = 1080;

brush.load(canvas);
brush.scaleBrushes(2.5);
brush.angleMode(brush.DEGREES);

function easeOutCubic(x) {
  return 1 - Math.pow(1 - x, 3);
}

// Deterministic drawing function: pure function of time t
window.renderAt = function(t) {
  brush.seed(42);
  brush.noiseSeed(42);

  brush.clear("#faf6ee");
  brush.push();
  brush.translate(-W / 2, -H / 2);

  const p = Math.min(Math.max(t / total, 0), 1);
  const strokeProgress = easeOutCubic(p);

  // 1. Soft watercolor wash fill in background
  brush.noStroke();
  brush.fill("#dcd0ba", 140);
  brush.fillBleed(0.35);
  brush.fillTexture(0.4, 0.25);
  brush.rect(200, 150, 1520, 780);
  brush.noFill();

  // 2. Cross-hatched architectural frame
  if (t > 0.5) {
    const hatchP = Math.min((t - 0.5) / 2.0, 1);
    brush.hatch(14, 45, { rand: 0.15, continuous: true });
    brush.set("cpencil", "#4a453b", 1.2);
    brush.rect(240, 190, 1440 * hatchP, 700);
    brush.noHatch();
  }

  // 3. Central historical sketch timeline with organic hand wiggle
  brush.wiggle(0.25);
  brush.set("charcoal", "#1e1a17", 2.2);
  const endX = 300 + 1320 * strokeProgress;
  brush.line(300, 540, endX, 540);
  brush.wiggle(0);

  // Archival connecting nodes
  const nodeCount = 5;
  for (let i = 0; i < nodeCount; i++) {
    const nodeT = ((i + 1) / (nodeCount + 1)) * total;
    if (t >= nodeT) {
      const nx = 300 + (i + 1) * (1320 / (nodeCount + 1));
      const ny = 540 + Math.sin(i * 1.5) * 120;

      brush.set("pen", "#d0312d", 2.0); // Ashu Dalal red accent
      brush.circle(nx, ny, 28);

      brush.set("HB", "#332d28", 1.6);
      brush.line(nx, 540, nx, ny);
    }
  }

  brush.pop();
  brush.render(); // Required flush in standalone build
};

window.total = total;
window.__ready = true;
window.renderAt(2.5);
