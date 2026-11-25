// World builders. All geometry is built once; per-frame animation only sets values from t.
const canvasTex = (THREE, w, h, draw) => {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
};
const std = (THREE, o) => new THREE.MeshStandardMaterial({ roughness: 0.85, metalness: 0.03, ...o });
const shadowed = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };

export function box({ THREE, scene, size = [1, 1, 1], color = '#888', pos = [0, 0, 0], rot = [0, 0, 0], roughness = 0.8 }) {
  const m = shadowed(new THREE.Mesh(new THREE.BoxGeometry(...size), std(THREE, { color, roughness })));
  m.position.set(...pos); m.rotation.set(...rot); scene.add(m); return m;
}

// A street running along -z from z=+8 to z=-length, buildings on both sides with seeded lit windows, lamps with flicker.
export function street({ THREE, scene, rng, length = 80, lamps = 5, look = {}, roadWidth = 7 }) {
  const practical = look.practical ?? 0xffb066;
  const ground = shadowed(new THREE.Mesh(new THREE.PlaneGeometry(60, length + 40), std(THREE, { color: 0x1d2028, roughness: 0.5, metalness: 0.1 })));
  ground.rotation.x = -Math.PI / 2; ground.position.z = -length / 2 + 4; scene.add(ground);
  for (const side of [-1, 1]) box({ THREE, scene, size: [2.2, 0.18, length + 30], color: '#2b2e36', pos: [side * (roadWidth / 2 + 1.1), 0.09, -length / 2 + 4] });

  const winTex = () => canvasTex(THREE, 256, 512, (g) => {
    g.fillStyle = '#141925'; g.fillRect(0, 0, 256, 512);
    for (let y = 12; y < 500; y += 36) for (let x = 14; x < 240; x += 34) {
      const lit = rng() > 0.55; g.fillStyle = lit ? (rng() > 0.5 ? '#ffcf7a' : '#ffe9b8') : '#0b0e16'; g.fillRect(x, y, 20, 24);
    }
  });
  const pool = [winTex(), winTex(), winTex(), winTex()];
  for (let i = 0; i * 8.5 < length + 20; i++) for (const side of [-1, 1]) {
    const w = 5 + rng() * 3, h = 9 + rng() * 14, tex = pool[Math.floor(rng() * pool.length)].clone();
    tex.needsUpdate = true; tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(w / 5, h / 10);
    const m = shadowed(new THREE.Mesh(new THREE.BoxGeometry(w, h, 7), std(THREE, { map: tex, emissiveMap: tex, emissive: 0xffffff, emissiveIntensity: 0.5, roughness: 0.9 })));
    m.position.set(side * (roadWidth / 2 + 2.2 + w / 2), h / 2, 8 - i * 8.5); scene.add(m);
  }
  const lights = [];
  const spacing = length / Math.max(1, lamps);
  for (let i = 0; i < Math.max(lamps, 1); i++) {
    const x = (i % 2 ? 1 : -1) * (roadWidth / 2 + 0.4), z = 2 - i * spacing;
    const L = new THREE.PointLight(practical, 26, 15, 1.6); L.position.set(x, 4.3, z); scene.add(L); lights.push(L);
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 12), new THREE.MeshBasicMaterial({ color: 0xffe0b0 })); bulb.position.copy(L.position); scene.add(bulb);
    const pole = shadowed(new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, 4.3, 8), std(THREE, { color: 0x15171c, roughness: 0.6 }))); pole.position.set(x, 2.15, z); scene.add(pole);
  }
  return { lights, update(t) { lights.forEach((l, i) => { l.intensity = 26 * (0.93 + 0.07 * Math.sin(t * 21 + i * 5) * Math.sin(t * 6.7 + i)); }); } };
}

// Room open toward +z (camera side). origin = centre of the floor.
export function room({ THREE, scene, w = 8, d = 10, h = 3.2, origin = [0, 0, 0], wall = '#8d7f6c', floor = '#4a3a2c', ceiling = '#cfc6b8', lampColor = 0xffe2b5, windowGlow = 0x7fa6e8 }) {
  const [ox, oy, oz] = origin, g = new THREE.Group(); g.position.set(ox, oy, oz); scene.add(g);
  const add = (size, pos, color) => { const m = shadowed(new THREE.Mesh(new THREE.BoxGeometry(...size), std(THREE, { color }))); m.position.set(...pos); g.add(m); return m; };
  add([w, 0.1, d], [0, -0.05, 0], floor); add([w, 0.1, d], [0, h + 0.05, 0], ceiling);
  add([w, h, 0.15], [0, h / 2, -d / 2], wall); add([0.15, h, d], [-w / 2, h / 2, 0], wall); add([0.15, h, d], [w / 2, h / 2, 0], wall);
  const win = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.3), new THREE.MeshBasicMaterial({ color: windowGlow })); win.position.set(-w / 4, 1.8, -d / 2 + 0.09); g.add(win);
  const lamp = new THREE.PointLight(lampColor, 22, 14, 1.5); lamp.position.set(0, h - 0.4, 0); g.add(lamp);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(0.12, 12, 12), new THREE.MeshBasicMaterial({ color: 0xfff1d8 })); bulb.position.copy(lamp.position); g.add(bulb);
  return { group: g, lamp, update(t) { lamp.intensity = 22 * (0.97 + 0.03 * Math.sin(t * 11)); } };
}

export function desk({ THREE, scene, pos = [0, 0, 0], size = [1.6, 0.75, 0.8], color = '#5a3d28' }) {
  const g = new THREE.Group(); g.position.set(...pos); scene.add(g);
  const top = shadowed(new THREE.Mesh(new THREE.BoxGeometry(size[0], 0.06, size[2]), std(THREE, { color }))); top.position.y = size[1]; g.add(top);
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
    const leg = shadowed(new THREE.Mesh(new THREE.BoxGeometry(0.06, size[1], 0.06), std(THREE, { color }))); leg.position.set(sx * (size[0] / 2 - 0.05), size[1] / 2, sz * (size[2] / 2 - 0.05)); g.add(leg);
  }
  return g;
}

// Paper with readable text. text: string with \n; or numbers:true for columns of digits (seeded, so identical every render).
export function documentMesh({ THREE, scene, rng, text = '', numbers = false, title = '', w = 0.42, h = 0.56, pos = [0, 1, 0], rot = [0, 0, 0], ink = '#1a1a1a', paper = '#efe9d8' }) {
  const tex = canvasTex(THREE, 768, Math.round(768 * h / w), (g, W, H) => {
    g.fillStyle = paper; g.fillRect(0, 0, W, H); g.fillStyle = ink;
    if (title) { g.font = 'bold 54px "Courier New", monospace'; g.textAlign = 'center'; g.fillText(title, W / 2, 90); }
    g.textAlign = 'left';
    if (numbers) { g.font = '34px "Courier New", monospace'; for (let y = title ? 150 : 70; y < H - 40; y += 46) { let line = ''; for (let c = 0; c < 6; c++) line += String(Math.floor(rng() * 90000) + 10000) + '  '; g.fillText(line, 40, y); } }
    else { g.font = '40px "Courier New", monospace'; text.split('\n').forEach((ln, i) => g.fillText(ln, 56, (title ? 170 : 110) + i * 58)); }
  });
  const m = shadowed(new THREE.Mesh(new THREE.PlaneGeometry(w, h), std(THREE, { map: tex, emissiveMap: tex, emissive: 0xffffff, emissiveIntensity: 0.25, roughness: 0.95, side: THREE.DoubleSide })));
  m.position.set(...pos); m.rotation.set(...rot); scene.add(m); return m;
}

// Picture / screen / poster: draw(ctx, w, h) paints it. Optional frame. glow>0 makes it light up like a screen.
export function picture({ THREE, scene, w = 1.2, h = 0.9, draw, pos = [0, 1.5, 0], rot = [0, 0, 0], frame = '#2a1c12', glow = 0.0 }) {
  const g = new THREE.Group(); g.position.set(...pos); g.rotation.set(...rot); scene.add(g);
  const tex = canvasTex(THREE, 1024, Math.round(1024 * h / w), draw);
  const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), std(THREE, { map: tex, emissiveMap: tex, emissive: 0xffffff, emissiveIntensity: glow, roughness: 0.6 })); face.position.z = 0.03; g.add(face);
  if (frame) { const f = shadowed(new THREE.Mesh(new THREE.BoxGeometry(w + 0.1, h + 0.1, 0.05), std(THREE, { color: frame }))); g.add(f); }
  return g;
}

// Glowing sign with text, e.g. neon or a shop name.
export function sign({ THREE, scene, text, w = 2.4, h = 0.6, pos = [0, 3, 0], rot = [0, 0, 0], color = '#ffd27a', bg = '#140f0a' }) {
  const tex = canvasTex(THREE, 1024, Math.round(1024 * h / w), (g, W, H) => {
    g.fillStyle = bg; g.fillRect(0, 0, W, H); g.fillStyle = color; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.font = `bold ${Math.round(H * 0.55)}px Arial, sans-serif`; g.fillText(text, W / 2, H / 2 + 4);
  });
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, toneMapped: false }));
  m.position.set(...pos); m.rotation.set(...rot); scene.add(m); return m;
}
