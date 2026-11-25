// Deterministic helpers. Every frame must be a pure function of time t.
export const ease = {
  linear: (t) => t,
  inOut: (t) => t * t * (3 - 2 * t),
  in: (t) => t * t,
  out: (t) => 1 - (1 - t) * (1 - t),
};

// Seeded RNG (LCG). Never use Math.random() in a scene: frames would differ between renders.
export function makeRng(seed = 1) {
  let s = (seed >>> 0) || 1;
  return () => (s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296;
}

const hermite = (p0, p1, m0, m1, dt, u) => {
  const u2 = u * u, u3 = u2 * u;
  return (2 * u3 - 3 * u2 + 1) * p0 + (u3 - 2 * u2 + u) * dt * m0 + (-2 * u3 + 3 * u2) * p1 + (u3 - u2) * dt * m1;
};

// Camera path through keyframes {t, pos:[x,y,z], look:[x,y,z], fov?}.
// Cubic Hermite with Catmull-Rom tangents: position AND velocity stay continuous across keys,
// so the camera glides through them (one continuous take) instead of stopping at each key.
// First and last keys have zero velocity (soft start / soft stop).
export class Timeline {
  constructor(keys = [], tension = 1) {
    this.k = [...keys].sort((a, b) => a.t - b.t).map((k) => ({ fov: 50, ...k }));
    const n = this.k.length;
    this.m = this.k.map((_, i) => {
      const tang = (get) => {
        const here = get(this.k[i]);
        if (i === 0 || i === n - 1) return Array.isArray(here) ? here.map(() => 0) : 0;
        const a = this.k[i - 1], b = this.k[i + 1], dt = b.t - a.t;
        const va = get(a), vb = get(b);
        return Array.isArray(va) ? va.map((x, j) => (tension * (vb[j] - x)) / dt) : (tension * (vb - va)) / dt;
      };
      return { pos: tang((k) => k.pos), look: tang((k) => k.look), fov: tang((k) => k.fov) };
    });
  }
  sample(t) {
    const k = this.k;
    if (!k.length) return { pos: [0, 1.6, 5], look: [0, 1.4, 0], fov: 50 };
    if (t <= k[0].t) return { pos: [...k[0].pos], look: [...k[0].look], fov: k[0].fov };
    const last = k[k.length - 1];
    if (t >= last.t) return { pos: [...last.pos], look: [...last.look], fov: last.fov };
    let i = 0;
    while (t > k[i + 1].t) i++;
    const a = k[i], b = k[i + 1], dt = b.t - a.t, u = (t - a.t) / dt;
    const vec = (ch) => [0, 1, 2].map((j) => hermite(a[ch][j], b[ch][j], this.m[i][ch][j], this.m[i + 1][ch][j], dt, u));
    return { pos: vec('pos'), look: vec('look'), fov: hermite(a.fov, b.fov, this.m[i].fov, this.m[i + 1].fov, dt, u) };
  }
}
