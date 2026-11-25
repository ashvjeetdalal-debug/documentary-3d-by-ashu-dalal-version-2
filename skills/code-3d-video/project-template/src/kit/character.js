// Articulated 3D mannequin (no external assets): head with expressive face, hair, torso, arms with elbows,
// legs with knees. Walk cycle is driven by distance walked, gestures by the word being spoken, blinking by time.
// Everything is a pure function of t, so renders are repeatable.
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
const hash = (x) => { const s = Math.sin(x * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

function faceTexture(THREE, { blink, open, mood }) {
  const c = document.createElement('canvas'); c.width = c.height = 256;
  const g = c.getContext('2d'); g.lineCap = 'round';
  g.fillStyle = '#16100c'; g.strokeStyle = '#16100c';
  const ex = [88, 168], ey = 112;
  for (const x of ex) {
    if (blink) { g.lineWidth = 7; g.beginPath(); g.moveTo(x - 15, ey + 4); g.lineTo(x + 15, ey + 4); g.stroke(); }
    else {
      g.beginPath(); g.ellipse(x, ey, 13, 18, 0, 0, Math.PI * 2); g.fill();
      g.fillStyle = '#fff'; g.beginPath(); g.arc(x + 4, ey - 6, 4.5, 0, Math.PI * 2); g.fill(); g.fillStyle = '#16100c';
    }
  }
  g.lineWidth = 7;
  const tilt = mood === 'worried' ? -12 : mood === 'angry' ? 14 : 0;           // inner-brow raise / lower
  g.beginPath(); g.moveTo(ex[0] - 20, 76 - tilt * 0.4); g.lineTo(ex[0] + 18, 76 + tilt); g.stroke();
  g.beginPath(); g.moveTo(ex[1] + 20, 76 - tilt * 0.4); g.lineTo(ex[1] - 18, 76 + tilt); g.stroke();
  const my = 188;
  if (open) {
    g.fillStyle = '#4a1a1a'; g.beginPath(); g.ellipse(128, my, 26, mood === 'smile' ? 20 : 17, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = '#c0504d'; g.beginPath(); g.ellipse(128, my + 8, 15, 8, 0, 0, Math.PI); g.fill();
  } else {
    g.beginPath();
    if (mood === 'smile') g.arc(128, my - 14, 30, 0.25 * Math.PI, 0.75 * Math.PI);
    else if (mood === 'worried' || mood === 'angry') g.arc(128, my + 22, 26, 1.25 * Math.PI, 1.75 * Math.PI);
    else { g.moveTo(104, my); g.lineTo(152, my); }
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

export function createCharacter({ THREE, scene, name = 'char', height = 1.75, skin = '#e0ac84', shirt = '#3f6fd8', pants = '#2a2f3a',
  hair = '#2b1d14', shoes = '#15151a', hairStyle = 'short', mood = 'neutral', path = null, pos = [0, 0, 0], yaw = 0,
  stride = 0.72, lookAt = null, blinkOffset = null }) {
  const mat = (color) => new THREE.MeshStandardMaterial({ color, roughness: 0.78, metalness: 0.02 });
  const cap = (r, l, color) => new THREE.Mesh(new THREE.CapsuleGeometry(r, l, 6, 14), mat(color));
  const root = new THREE.Group(); root.name = name;
  const body = new THREE.Group(); root.add(body);                      // bobs and leans
  const hips = new THREE.Group(); hips.position.y = 0.93; body.add(hips);

  const torso = cap(0.16, 0.34, shirt); torso.scale.z = 0.72; torso.position.y = 0.30; hips.add(torso);
  const neck = cap(0.045, 0.06, skin); neck.position.y = 0.58; hips.add(neck);
  const head = new THREE.Group(); head.position.y = 0.72; hips.add(head);
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.13, 28, 20), mat(skin)); skull.scale.set(1, 1.08, 1.02); head.add(skull);
  const faceTex = [0, 1].map((b) => [0, 1].map((o) => faceTexture(THREE, { blink: !!b, open: !!o, mood })));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(0.235, 0.235), new THREE.MeshBasicMaterial({ map: faceTex[0][0], transparent: true, depthWrite: false }));
  face.position.set(0, 0.0, 0.136); head.add(face);
  if (hairStyle !== 'bald') {
    const h = new THREE.Mesh(new THREE.SphereGeometry(0.139, 28, 16, 0, Math.PI * 2, 0, Math.PI * (hairStyle === 'long' ? 0.72 : 0.5)), mat(hair));
    h.position.set(0, 0.014, -0.012); h.scale.set(1, 1.08, 1.04); head.add(h);
  }

  const makeArm = (side) => {
    const sh = new THREE.Group(); sh.position.set(side * 0.215, 0.5, 0); hips.add(sh);
    const up = cap(0.043, 0.22, shirt); up.position.y = -0.17; sh.add(up);
    const el = new THREE.Group(); el.position.y = -0.34; sh.add(el);
    const lo = cap(0.037, 0.2, skin); lo.position.y = -0.15; el.add(lo);
    const hand = new THREE.Mesh(new THREE.SphereGeometry(0.042, 12, 10), mat(skin)); hand.position.y = -0.3; el.add(hand);
    return { sh, el };
  };
  const makeLeg = (side) => {
    const th = new THREE.Group(); th.position.set(side * 0.085, 0, 0); hips.add(th);
    const up = cap(0.068, 0.3, pants); up.position.y = -0.22; th.add(up);
    const kn = new THREE.Group(); kn.position.y = -0.44; th.add(kn);
    const lo = cap(0.055, 0.3, pants); lo.position.y = -0.22; kn.add(lo);
    const foot = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.07, 0.25), mat(shoes)); foot.position.set(0, -0.46, 0.05); kn.add(foot);
    return { th, kn };
  };
  const L = { arm: makeArm(-1), leg: makeLeg(-1) }, R = { arm: makeArm(1), leg: makeLeg(1) };
  root.scale.setScalar(height / 1.75);
  root.traverse((o) => { if (o.isMesh && o !== face) { o.castShadow = true; o.receiveShadow = true; } });
  root.position.set(...pos); root.rotation.y = yaw;
  scene.add(root);

  const off = blinkOffset ?? hash(name.length * 7 + height) * 3;
  let blend = 0;
  return {
    group: root,
    // st = { speaking: bool, word: {w,t0,t1}|null }
    update(t, st = {}) {
      let moving = false, dist = 0, bodyYaw = yaw;
      if (path) {
        const p = path.at(t);
        root.position.set(p.pos[0], p.pos[1], p.pos[2]); root.rotation.y = bodyYaw = p.yaw;
        moving = p.moving; dist = p.dist; blend = clamp(p.speed / 0.9, 0, 1);
      } else blend = 0;
      const ph = (dist / stride) * Math.PI;                      // one step = pi of phase
      const A = 0.62 * blend, s = Math.sin(ph), s2 = Math.sin(ph + Math.PI);
      L.leg.th.rotation.x = -s * A;  L.leg.kn.rotation.x = Math.max(0, -Math.cos(ph)) * 0.95 * blend;
      R.leg.th.rotation.x = -s2 * A; R.leg.kn.rotation.x = Math.max(0, -Math.cos(ph + Math.PI)) * 0.95 * blend;
      L.arm.sh.rotation.x = s * 0.5 * blend;  R.arm.sh.rotation.x = s2 * 0.5 * blend;
      L.arm.el.rotation.x = R.arm.el.rotation.x = -0.18 - 0.2 * blend;
      L.arm.sh.rotation.z = -0.06; R.arm.sh.rotation.z = 0.06;
      body.position.y = Math.abs(s) * 0.035 * blend;
      body.rotation.x = 0.06 * blend;
      hips.rotation.y = s * 0.08 * blend;
      torso.scale.y = 1 + 0.012 * Math.sin(t * 1.9 + off);        // breathing

      let nod = 0;
      if (st.speaking && st.word) {                                // gesture per spoken word
        const w = st.word, prog = clamp((t - w.t0) / Math.max(0.05, w.t1 - w.t0), 0, 1), env = Math.sin(Math.PI * prog);
        const g = hash(w.t0), arm = g < 0.5 ? R.arm : L.arm, k = (1 - blend) * env * (0.35 + 0.65 * hash(w.t0 + 3.3));
        arm.sh.rotation.x -= k * 0.9; arm.el.rotation.x -= k * 0.7; arm.sh.rotation.z += (arm === R.arm ? 1 : -1) * k * 0.25;
        nod = env * 0.07;
      }
      let hy = 0;
      if (lookAt) {
        const target = typeof lookAt === 'function' ? lookAt(t) : lookAt, dx = target[0] - root.position.x, dz = target[2] - root.position.z;
        let d = Math.atan2(dx, dz) - bodyYaw; d = Math.atan2(Math.sin(d), Math.cos(d)); hy = clamp(d, -0.9, 0.9);
      }
      head.rotation.set(nod, hy, 0);
      const blinking = ((t + off) % 3.3) < 0.12 ? 1 : 0;
      const open = st.speaking && Math.floor(t * 10) % 2 === 0 ? 1 : 0;
      face.material.map = faceTex[blinking][open];
    },
  };
}
