// Deterministic movement path for a character: keys [{t, pos:[x,y,z]}], linear (walking) or eased per segment.
// at(t) -> { pos, yaw, speed, moving, dist }  (dist = metres walked so far: drives the walk cycle so feet never slide)
export function makePath(keys, { ease = 'linear' } = {}) {
  const k = [...keys].sort((a, b) => a.t - b.t);
  const e = ease === 'inOut' ? (u) => u * u * (3 - 2 * u) : (u) => u;
  const pos = (t) => {
    if (t <= k[0].t) return [...k[0].pos];
    const L = k[k.length - 1];
    if (t >= L.t) return [...L.pos];
    let i = 0; while (t > k[i + 1].t) i++;
    const u = e((t - k[i].t) / (k[i + 1].t - k[i].t));
    return [0, 1, 2].map((j) => k[i].pos[j] + (k[i + 1].pos[j] - k[i].pos[j]) * u);
  };
  const STEP = 1 / 60, N = Math.ceil((k[k.length - 1].t + 1) / STEP) + 1;
  const cum = new Float64Array(N), yawT = new Float64Array(N);
  let prev = pos(0), yaw = k.length > 1 ? Math.atan2(k[1].pos[0] - k[0].pos[0], k[1].pos[2] - k[0].pos[2]) : 0;
  for (let i = 1; i < N; i++) {
    const p = pos(i * STEP), dx = p[0] - prev[0], dz = p[2] - prev[2], d = Math.hypot(dx, dz);
    cum[i] = cum[i - 1] + d;
    if (d / STEP > 0.15) yaw = Math.atan2(dx, dz);     // hold the last heading while standing still
    yawT[i] = yaw; prev = p;
  }
  yawT[0] = yawT[1] ?? yaw;
  return {
    at(t) {
      const f = Math.min(Math.max(t, 0) / STEP, N - 2), i = Math.floor(f), u = f - i;
      const a = pos(Math.max(0, t - 0.03)), b = pos(t + 0.03);
      const speed = Math.hypot(b[0] - a[0], b[2] - a[2]) / 0.06;
      return { pos: pos(t), yaw: yawT[i] + (yawT[i + 1] - yawT[i]) * u * (Math.abs(yawT[i + 1] - yawT[i]) < Math.PI ? 1 : 0),
               speed, moving: speed > 0.15, dist: cum[i] + (cum[i + 1] - cum[i]) * u };
    },
  };
}
