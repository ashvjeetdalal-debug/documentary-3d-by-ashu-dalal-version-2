// Tiny canvas-2D scene used by `npm run selftest` to prove Chrome + ffmpeg + audio work
// before you involve three.js. Not used for real videos.
export async function build({ canvas }) {
  canvas.width = innerWidth; canvas.height = innerHeight;
  const ctx = canvas.getContext('2d');
  return {
    update(t, s) {
      const W = canvas.width, H = canvas.height;
      const g = ctx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, `hsl(${(210 + t * 20) % 360} 60% 18%)`); g.addColorStop(1, '#05070d');
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      const r = Math.min(W, H) * 0.12;
      const x = W / 2 + Math.cos(t * 2) * W * 0.25, y = H * 0.38 + Math.sin(t * 2) * H * 0.08;
      ctx.fillStyle = '#ffd27a'; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
      ctx.fillStyle = '#1a1a1a'; ctx.beginPath();
      ctx.ellipse(x, y + r * 0.35, r * 0.28, s.speaking ? r * 0.2 : r * 0.05, 0, 0, 7); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.font = `700 ${H * 0.025}px sans-serif`; ctx.textAlign = 'center';
      ctx.fillText(`SELFTEST  t=${t.toFixed(2)}s  cam.z=${s.camera.pos[2].toFixed(2)}`, W / 2, H * 0.08);
    },
  };
}
