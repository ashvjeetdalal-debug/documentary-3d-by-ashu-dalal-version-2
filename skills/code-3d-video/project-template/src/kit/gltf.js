// Upgrade path to richer characters: load a .glb you have the rights to (put it in assets/) and drive its animation clips
// deterministically (never mixer.update(dt): set clip times from t / distance walked, then mixer.update(0)).
export async function loadGLTFCharacter({ THREE, scene, url, height = null, path = null, pos = [0, 0, 0], yaw = 0,
  clips = { idle: 'idle', walk: 'walk' }, stride = 1.4 }) {
  const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  let gltf;
  try { gltf = await new GLTFLoader().loadAsync(url); }
  catch (e) { throw new Error(`Could not load model "${url}". Put the .glb in assets/ and use "./assets/<file>.glb". ${e && e.message}`); }
  const root = gltf.scene;
  if (height) { const box = new THREE.Box3().setFromObject(root), h = box.max.y - box.min.y; if (h > 0) root.scale.multiplyScalar(height / h); }
  root.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  const holder = new THREE.Group(); holder.add(root); holder.position.set(...pos); holder.rotation.y = yaw; scene.add(holder);
  const mixer = new THREE.AnimationMixer(root);
  const find = (n) => gltf.animations.find((a) => a.name.toLowerCase().includes(String(n).toLowerCase()));
  const act = {};
  for (const [k, n] of Object.entries(clips)) { const c = find(n); if (c) { act[k] = mixer.clipAction(c); act[k].play(); } }
  if (!Object.keys(act).length) console.warn('GLTF has no matching clips. Available:', gltf.animations.map((a) => a.name).join(', '));
  return {
    group: holder, animations: gltf.animations.map((a) => a.name),
    update(t) {
      let moving = false, dist = 0, speed = 0;
      if (path) { const p = path.at(t); holder.position.set(...p.pos); holder.rotation.y = p.yaw; moving = p.moving; dist = p.dist; speed = p.speed; }
      const w = Math.min(1, speed / 0.9);
      if (act.idle) { act.idle.time = t % act.idle.getClip().duration; act.idle.setEffectiveWeight(1 - w); }
      if (act.walk) { act.walk.time = ((dist / stride) % 1) * act.walk.getClip().duration; act.walk.setEffectiveWeight(w); }
      mixer.update(0);
    },
  };
}
